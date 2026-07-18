#!/usr/bin/env python3
"""Génère le PDF projet ORGANIC EXO à partir de contenu.md.

Usage : python3 build_pdf.py
Sortie : pdf/ORGANIC_EXO_<version>.pdf

Le format source est un sous-ensemble de Markdown :
  # / ## / ###   titres (H1 = nouvelle page, numérotation auto sauf sections listées)
  - / (2 esp.)-  puces (2 niveaux)
  | a | b |      tableaux (1re ligne = en-tête)
  > texte        encadré
  **b** *i* `c`  gras, italique, code ; ^{x} exposant, _{x} indice
  ---            bloc de métadonnées en tête de fichier
"""
import hashlib
import os
import re

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (BaseDocTemplate, Flowable, Frame, HRFlowable,
                                NextPageTemplate, PageBreak, PageTemplate,
                                Paragraph, Spacer, Table, TableStyle)
from reportlab.platypus.tableofcontents import TableOfContents

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "contenu.md")
OUTDIR = os.path.join(HERE, "pdf")

CHARCOAL = colors.HexColor("#232323")
INK = colors.HexColor("#1A1A1A")
COPPER = colors.HexColor("#B4682F")
COPPER_DARK = colors.HexColor("#8C4E1F")
SAND = colors.HexColor("#F4EDDE")
SAND_LINE = colors.HexColor("#D8C9A8")
GREY = colors.HexColor("#6B6B6B")

UNNUMBERED_H1 = {"Mode d'emploi du document", "Journal des révisions", "Références",
                 "Annexe A — Intégrer les MCP pas à pas",
                 "Annexe B — Lettre type sablière (à personnaliser)"}

PAGE_W, PAGE_H = A4
MARG_L = MARG_R = 18 * mm
MARG_T = 20 * mm
MARG_B = 18 * mm
FRAME_W = PAGE_W - MARG_L - MARG_R

# ---------------------------------------------------------------- sanitisation
# Les polices base-14 sont en WinAnsi : on rabat les glyphes hors CP1252.
SAFE = {"≥": ">=", "≤": "<=", "→": "->", "←": "<-",
        "≈": "~", "Δ": "delta ", "✓": "[OK]", "✔": "[OK]",
        "−": "-", "‑": "-", " ": " ", " ": " "}


def sanitize(t):
    for k, v in SAFE.items():
        t = t.replace(k, v)
    return "".join(c if c.encode("cp1252", "ignore") else "?" for c in t)


MARKERS = {"[VERROUILLÉ]": "#8C4E1F", "[EN ÉTUDE]": "#2F6F8F",
           "[REJETÉ]": "#7A7A7A", "[A DÉCIDER]": "#A93226",
           "[EN ÉTUDE - priorité 1]": "#2F6F8F", "[EN ÉTUDE - phase 3]": "#2F6F8F",
           "[VERROUILLÉ - MVP]": "#8C4E1F"}


def inline(t):
    """Markdown allégé -> balisage Paragraph de reportlab."""
    t = sanitize(t)
    t = t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    t = re.sub(r"`([^`]+)`", r'<font face="Courier" size="8">\1</font>', t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"\*([^*\n]+)\*", r"<i>\1</i>", t)
    t = re.sub(r"\^\{([^}]*)\}", r"<super>\1</super>", t)
    t = re.sub(r"_\{([^}]*)\}", r"<sub>\1</sub>", t)
    t = t.replace(" -&gt; ", " › ")   # flèches -> chevron typographique
    for m, c in MARKERS.items():
        t = t.replace(m, '<font color="%s"><b>%s</b></font>' % (c, m))
    return t


# ------------------------------------------------------------------- styles
def make_styles():
    s = {}
    s["Body"] = ParagraphStyle("Body", fontName="Helvetica", fontSize=9.5,
                               leading=13.8, textColor=INK, alignment=TA_JUSTIFY,
                               spaceAfter=5)
    s["H1"] = ParagraphStyle("H1", fontName="Helvetica-Bold", fontSize=19,
                             leading=23, textColor=CHARCOAL, spaceBefore=2,
                             spaceAfter=3)
    s["H2"] = ParagraphStyle("H2", fontName="Helvetica-Bold", fontSize=13,
                             leading=16.5, textColor=CHARCOAL, spaceBefore=11,
                             spaceAfter=4)
    s["H3"] = ParagraphStyle("H3", fontName="Helvetica-Bold", fontSize=10.5,
                             leading=14, textColor=COPPER_DARK, spaceBefore=9,
                             spaceAfter=3)
    s["Bullet"] = ParagraphStyle("Bullet", parent=s["Body"], leftIndent=14,
                                 bulletIndent=4, spaceAfter=3)
    s["Bullet2"] = ParagraphStyle("Bullet2", parent=s["Body"], leftIndent=26,
                                  bulletIndent=16, spaceAfter=2.5)
    s["Callout"] = ParagraphStyle("Callout", parent=s["Body"], fontSize=9,
                                  leading=13, textColor=CHARCOAL, alignment=TA_LEFT,
                                  spaceAfter=0)
    s["Cell"] = ParagraphStyle("Cell", parent=s["Body"], fontSize=8.4,
                               leading=11.2, alignment=TA_LEFT, spaceAfter=0)
    s["CellHead"] = ParagraphStyle("CellHead", parent=s["Cell"],
                                   fontName="Helvetica-Bold",
                                   textColor=colors.white)
    s["TOC0"] = ParagraphStyle("TOC0", fontName="Helvetica-Bold", fontSize=10.5,
                               leading=17, textColor=CHARCOAL)
    s["TOC1"] = ParagraphStyle("TOC1", fontName="Helvetica", fontSize=9,
                               leading=13.5, textColor=INK, leftIndent=14)
    s["TocTitle"] = ParagraphStyle("TocTitle", parent=s["H1"], spaceAfter=10)
    return s


# ------------------------------------------------------------------- parsing
def parse_meta(lines):
    meta, i = {}, 0
    if lines and lines[0].strip() == "---":
        i = 1
        while i < len(lines) and lines[i].strip() != "---":
            if ":" in lines[i]:
                k, v = lines[i].split(":", 1)
                meta[k.strip()] = v.strip()
            i += 1
        i += 1
    return meta, lines[i:]


def col_widths(rows, ncols):
    # Largeur estimée en points (~4,9 pt/caractère à 8,4 pt) + marges de cellule,
    # puis mise à l'échelle sur la largeur utile : les colonnes courtes (marqueurs
    # d'état, numéros) gardent assez de place pour ne pas couper un mot.
    lens = [max(len(r[c]) for r in rows) for c in range(ncols)]
    pts = [min(l, 55) * 4.9 + 16 for l in lens]
    scale = FRAME_W / float(sum(pts))
    w = [p * scale for p in pts]
    # plancher : aucune colonne sous ~18 mm, sinon les mots se coupent lettre
    # à lettre ; on reprend l'excédent sur les colonnes larges au prorata
    minw = 52.0
    if ncols > 1 and min(w) < minw:
        w = [max(x, minw) for x in w]
        excess = sum(w) - FRAME_W
        wide = [i for i, x in enumerate(w) if x > minw]
        wide_total = sum(w[i] - minw for i in wide)
        if wide and wide_total > 0:
            for i in wide:
                w[i] -= excess * (w[i] - minw) / wide_total
    return w


def build_table(rows, s):
    ncols = max(len(r) for r in rows)
    rows = [r + [""] * (ncols - len(r)) for r in rows]
    data = [[Paragraph(inline(c), s["CellHead"]) for c in rows[0]]]
    for r in rows[1:]:
        data.append([Paragraph(inline(c), s["Cell"]) for c in r])
    t = Table(data, colWidths=col_widths(rows, ncols), repeatRows=1)
    style = [("BACKGROUND", (0, 0), (-1, 0), CHARCOAL),
             ("LINEBELOW", (0, 0), (-1, 0), 0.8, COPPER),
             ("GRID", (0, 1), (-1, -1), 0.35, SAND_LINE),
             ("VALIGN", (0, 0), (-1, -1), "TOP"),
             ("TOPPADDING", (0, 0), (-1, -1), 3.5),
             ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
             ("LEFTPADDING", (0, 0), (-1, -1), 5),
             ("RIGHTPADDING", (0, 0), (-1, -1), 5)]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style.append(("BACKGROUND", (0, i), (-1, i), SAND))
    t.setStyle(TableStyle(style))
    t.spaceAfter = 7
    t.spaceBefore = 2
    return t


def build_callout(paras, s):
    # un seul encadré, paragraphes séparés par une ligne vide
    markup = "<br/><br/>".join(inline(p) for p in paras)
    p = Paragraph(markup, s["Callout"])
    t = Table([[p]], colWidths=[FRAME_W - 4])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), SAND),
                           ("LINEBEFORE", (0, 0), (0, -1), 2.2, COPPER),
                           ("TOPPADDING", (0, 0), (-1, -1), 6),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                           ("LEFTPADDING", (0, 0), (-1, -1), 9),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 8)]))
    t.spaceBefore, t.spaceAfter = 4, 7
    return t


def parse_story(lines, s):
    story = []
    n_h1 = 0
    n_h2 = 0
    h1_numbered = False
    i = 0
    first_h1 = True
    while i < len(lines):
        line = lines[i].rstrip("\n")
        strip = line.strip()
        if not strip:
            i += 1
            continue
        if strip.startswith("### "):
            story.append(Paragraph(inline(strip[4:]), s["H3"]))
            i += 1
        elif strip.startswith("## "):
            txt = strip[3:]
            if h1_numbered:
                n_h2 += 1
                num = "%d.%d" % (n_h1, n_h2)
                label = '<font color="#B4682F">%s</font>&nbsp;&nbsp;%s' % (num, inline(txt))
            else:
                label = inline(txt)
            story.append(Paragraph(label, s["H2"]))
            i += 1
        elif strip.startswith("# "):
            txt = sanitize(strip[2:])
            if not first_h1:
                story.append(PageBreak())
            first_h1 = False
            if txt in UNNUMBERED_H1:
                num, toc = None, txt
                h1_numbered = False
            else:
                n_h1 += 1
                n_h2 = 0
                num, toc = n_h1, "%d  %s" % (n_h1, txt)
                h1_numbered = True
            story.append(SectionBanner(num, txt, toc))
            story.append(Spacer(1, 7 * mm))
            i += 1
        elif strip.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
                    rows.append(cells)
                i += 1
            if rows:
                story.append(build_table(rows, s))
        elif strip.startswith(">"):
            buf = [[]]
            while i < len(lines) and lines[i].strip().startswith(">"):
                t = lines[i].strip()
                if t == ">":
                    buf.append([])
                else:
                    buf[-1].append(t[2:] if t.startswith("> ") else t[1:].lstrip())
                i += 1
            paras = [" ".join(b) for b in buf if b]
            if paras:
                story.append(build_callout(paras, s))
        elif strip == "---":
            story.append(HRFlowable(width="100%", thickness=0.6, color=SAND_LINE,
                                    spaceBefore=6, spaceAfter=6))
            i += 1
        elif line.startswith("  - "):
            story.append(Paragraph(inline(line[4:]), s["Bullet2"],
                                   bulletText="–"))
            i += 1
        elif strip.startswith("- "):
            story.append(Paragraph(inline(strip[2:]), s["Bullet"],
                                   bulletText="•"))
            i += 1
        elif re.match(r"^\d+\.\s", strip):
            story.append(Paragraph(inline(strip), s["Bullet"]))
            i += 1
        else:
            buf = [strip]
            i += 1
            while i < len(lines):
                nxt = lines[i].strip()
                if (not nxt or nxt.startswith(("#", "|", "- ", "> ", "---"))
                        or lines[i].startswith("  - ") or re.match(r"^\d+\.\s", nxt)):
                    break
                buf.append(nxt)
                i += 1
            story.append(Paragraph(inline(" ".join(buf)), s["Body"]))
    return story


# ------------------------------------------------------------------ gabarits
def draw_spine(canvas, ox, oy, his, los, pairs, radius, width):
    """Motif signature : épine dorsale triangulée à nœuds (repris de la couverture)."""
    canvas.setLineWidth(width)

    def pt(p):
        return (ox + p[0] * mm, oy + p[1] * mm)

    def seg(a, b):
        (x1, y1), (x2, y2) = pt(a), pt(b)
        canvas.line(x1, y1, x2, y2)

    for a, b in zip(his, his[1:]):
        seg(a, b)
    for a, b in zip(los, los[1:]):
        seg(a, b)
    for hi, lo in pairs:
        seg(his[hi], los[lo])
    for p in his + los:
        x, y = pt(p)
        canvas.circle(x, y, radius, stroke=0, fill=1)


class SectionBanner(Flowable):
    """Bandeau de tête de section : anthracite, numéro cuivre, motif triangulé.

    Porte l'identité de la couverture à l'intérieur du document. `toc_text`
    à None = pas d'entrée au sommaire (cas du Sommaire lui-même).
    """

    HEIGHT = 24 * mm

    def __init__(self, number, title, toc_text):
        Flowable.__init__(self)
        self.number, self.title, self.toc_text = number, title, toc_text
        self.width, self.height = FRAME_W, self.HEIGHT

    def wrap(self, aw, ah):
        return self.width, self.height

    def _fit_title(self, maxw):
        for size in (16, 14.5, 13, 11.5):
            words, lines, cur = self.title.split(), [], ""
            ok = True
            for w in words:
                t = (cur + " " + w).strip()
                if self.canv.stringWidth(t, "Helvetica-Bold", size) <= maxw or not cur:
                    cur = t
                else:
                    lines.append(cur)
                    cur = w
            lines.append(cur)
            for l in lines:
                if self.canv.stringWidth(l, "Helvetica-Bold", size) > maxw:
                    ok = False
            if ok and len(lines) <= 2:
                return lines, size
        return lines[:2], 11.5

    def draw(self):
        c = self.canv
        c.saveState()
        c.setFillColor(CHARCOAL)
        c.rect(0, 0, self.width, self.height, stroke=0, fill=1)
        c.setFillColor(COPPER)
        c.rect(0, 0, self.width, 1.1 * mm, stroke=0, fill=1)
        # motif en fond de zone droite, estompé
        c.setStrokeColor(COPPER)
        c.setFillColor(COPPER)
        try:
            c.setStrokeAlpha(0.5)
            c.setFillAlpha(0.5)
        except AttributeError:
            pass
        his = [(0, 13), (12, 17.5), (25, 19.5), (39, 18.5), (51, 14)]
        los = [(6, 6.5), (19, 8), (33, 8.5), (47, 6)]
        pairs = [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2), (3, 2), (3, 3), (4, 3)]
        draw_spine(c, self.width - 58 * mm, 0, his, los, pairs, 1.1 * mm, 0.9)
        try:
            c.setStrokeAlpha(1)
            c.setFillAlpha(1)
        except AttributeError:
            pass
        x_title = 7 * mm
        if self.number:
            c.setFillColor(COPPER)
            c.setFont("Helvetica-Bold", 30)
            c.drawString(7 * mm, 6.8 * mm, str(self.number))
            x_title = 20 * mm
        lines, size = self._fit_title(self.width - x_title - 62 * mm)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", size)
        if len(lines) == 1:
            c.drawString(x_title, (self.height - size) / 2.0 + 1.5, lines[0])
        else:
            c.drawString(x_title, self.height / 2.0 + 2.5, lines[0])
            c.drawString(x_title, self.height / 2.0 - size - 0.5, lines[1])
        c.restoreState()


class ProjectDoc(BaseDocTemplate):
    def _register(self, text, level):
        key = hashlib.md5((text + str(self.page)).encode()).hexdigest()[:10]
        self.canv.bookmarkPage(key)
        self.canv.addOutlineEntry(text, key, level, level == 0)
        self.notify("TOCEntry", (level, text, self.page))

    def afterFlowable(self, fl):
        if isinstance(fl, SectionBanner):
            if fl.toc_text:
                self._register(fl.toc_text, 0)
        elif isinstance(fl, Paragraph) and fl.style.name == "H2":
            self._register(fl.getPlainText(), 1)


def draw_cover(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(CHARCOAL)
    canvas.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    # motif exosquelette : épine dorsale triangulée, trait cuivre
    nodes = [(22, 168), (52, 186), (86, 197), (122, 199), (154, 190),
             (176, 172), (188, 150)]
    lows = [(34, 148), (72, 152), (112, 156), (150, 152), (180, 136)]
    canvas.setStrokeColor(COPPER)
    canvas.setLineWidth(1.1)

    def seg(a, b):
        canvas.line(a[0] * mm, a[1] * mm, b[0] * mm, b[1] * mm)

    for a, b in zip(nodes, nodes[1:]):
        seg(a, b)
    for a, b in zip(lows, lows[1:]):
        seg(a, b)
    pairs = [(0, 0), (1, 0), (1, 1), (2, 1), (3, 1), (3, 2), (4, 2), (4, 3),
             (5, 3), (5, 4), (6, 4)]
    for hi, lo in pairs:
        seg(nodes[hi], lows[lo])
    canvas.setFillColor(COPPER)
    for x, y in nodes + lows:
        canvas.circle(x * mm, y * mm, 1.5 * mm, stroke=0, fill=1)

    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 46)
    canvas.drawString(22 * mm, 116 * mm, sanitize(doc.meta.get("titre", "PROJET")))
    canvas.setFillColor(COPPER)
    canvas.setFont("Helvetica", 15)
    canvas.drawString(22.5 * mm, 105 * mm, sanitize(doc.meta.get("sous-titre", "")))
    canvas.setStrokeColor(COPPER)
    canvas.setLineWidth(1.6)
    canvas.line(22 * mm, 98 * mm, 128 * mm, 98 * mm)

    canvas.setFillColor(colors.HexColor("#CFCFCF"))
    canvas.setFont("Helvetica", 10.5)
    canvas.drawString(22.5 * mm, 88 * mm, "Document projet de référence — vivant, versionné")
    y = 50
    for label, key in (("Version", "version"), ("Date", "date"), ("Statut", "statut")):
        canvas.setFillColor(COPPER)
        canvas.setFont("Helvetica-Bold", 9.5)
        canvas.drawString(22.5 * mm, y * mm, label.upper())
        canvas.setFillColor(colors.white)
        canvas.setFont("Helvetica", 10.5)
        canvas.drawString(48 * mm, y * mm, sanitize(doc.meta.get(key, "—")))
        y -= 8
    canvas.setFillColor(colors.HexColor("#8A8A8A"))
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(22.5 * mm, 16 * mm,
                      "Source : projet-sandrail/contenu.md — régénéré à chaque itération (build_pdf.py)")
    canvas.restoreState()


def draw_body(canvas, doc):
    canvas.saveState()
    # en-tête : motif signature, titre courant, version, filet cuivre
    canvas.setStrokeColor(COPPER)
    canvas.setFillColor(COPPER)
    his = [(0, 0.3), (3.6, 1.8), (7.4, 2.5), (11, 1.6)]
    los = [(1.8, -1.7), (5.5, -1.2), (9.2, -1.9)]
    pairs = [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2), (3, 2)]
    draw_spine(canvas, MARG_L, PAGE_H - 10.6 * mm, his, los, pairs, 0.55 * mm, 0.7)
    canvas.setFillColor(GREY)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(MARG_L + 16 * mm, PAGE_H - 11.4 * mm,
                      sanitize("%s — %s" % (doc.meta.get("titre", ""),
                                            doc.meta.get("sous-titre", ""))))
    canvas.setFillColor(COPPER)
    canvas.setFont("Helvetica-Bold", 7.5)
    canvas.drawRightString(PAGE_W - MARG_R, PAGE_H - 11.4 * mm,
                           sanitize(doc.meta.get("version", "")))
    canvas.setStrokeColor(COPPER)
    canvas.setLineWidth(0.8)
    canvas.line(MARG_L, PAGE_H - 13.6 * mm, PAGE_W - MARG_R, PAGE_H - 13.6 * mm)
    # pied : filet cuivre, mention, pavé anthracite de pagination
    canvas.line(MARG_L, 13.2 * mm, PAGE_W - MARG_R, 13.2 * mm)
    canvas.setFillColor(GREY)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(MARG_L, 8.8 * mm,
                      sanitize("Référentiel technique — %s" % doc.meta.get("date", "")))
    tab_w, tab_h = 13 * mm, 6.4 * mm
    x = PAGE_W - MARG_R - tab_w
    canvas.setFillColor(CHARCOAL)
    canvas.rect(x, 6.2 * mm, tab_w, tab_h, stroke=0, fill=1)
    canvas.setFillColor(COPPER)
    canvas.rect(x, 6.2 * mm, 1.1 * mm, tab_h, stroke=0, fill=1)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 8)
    canvas.drawCentredString(x + tab_w / 2 + 0.5 * mm, 8.4 * mm,
                             "%d" % canvas.getPageNumber())
    canvas.restoreState()


def main():
    with open(SRC, encoding="utf-8") as f:
        lines = f.read().splitlines()
    meta, body_lines = parse_meta(lines)
    s = make_styles()

    os.makedirs(OUTDIR, exist_ok=True)
    out = os.path.join(OUTDIR, "ORGANIC_EXO_%s.pdf" % meta.get("version", "v0"))

    doc = ProjectDoc(out, pagesize=A4, leftMargin=MARG_L, rightMargin=MARG_R,
                     topMargin=MARG_T, bottomMargin=MARG_B,
                     title="%s %s" % (meta.get("titre", ""), meta.get("version", "")),
                     author="Projet ORGANIC EXO")
    doc.meta = meta
    cover_frame = Frame(0, 0, PAGE_W, PAGE_H, id="cover")
    body_frame = Frame(MARG_L, MARG_B, FRAME_W, PAGE_H - MARG_T - MARG_B, id="body")
    doc.addPageTemplates([PageTemplate(id="Cover", frames=[cover_frame],
                                       onPage=draw_cover),
                          PageTemplate(id="Body", frames=[body_frame],
                                       onPage=draw_body)])

    toc = TableOfContents()
    toc.levelStyles = [s["TOC0"], s["TOC1"]]
    toc.dotsMinLevel = 0

    story = [NextPageTemplate("Body"), Spacer(1, 1), PageBreak(),
             SectionBanner(None, "Sommaire", None),
             Spacer(1, 7 * mm),
             toc]
    story += parse_story(body_lines, s)
    doc.multiBuild(story)
    print("OK :", out)


if __name__ == "__main__":
    main()
