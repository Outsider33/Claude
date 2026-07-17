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
from reportlab.platypus import (BaseDocTemplate, Frame, HRFlowable, NextPageTemplate,
                                PageBreak, PageTemplate, Paragraph, Spacer, Table,
                                TableStyle)
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

UNNUMBERED_H1 = {"Mode d'emploi du document", "Journal des révisions", "Références"}

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
    return [p * scale for p in pts]


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


def build_callout(text, s):
    p = Paragraph(inline(text), s["Callout"])
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
            n_h2 += 1
            txt = strip[3:]
            num = "%d.%d" % (n_h1, n_h2) if n_h1 else ""
            label = ('<font color="#B4682F">%s</font>&nbsp;&nbsp;%s' % (num, inline(txt))) if num else inline(txt)
            story.append(Paragraph(label, s["H2"]))
            i += 1
        elif strip.startswith("# "):
            txt = strip[2:]
            if not first_h1:
                story.append(PageBreak())
            first_h1 = False
            if txt in UNNUMBERED_H1:
                label = inline(txt)
            else:
                n_h1 += 1
                n_h2 = 0
                label = '<font color="#B4682F">%d</font>&nbsp;&nbsp;%s' % (n_h1, inline(txt))
            story.append(Paragraph(label, s["H1"]))
            story.append(HRFlowable(width="100%", thickness=1.4, color=COPPER,
                                    spaceBefore=1, spaceAfter=9))
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
        elif strip.startswith("> "):
            buf = []
            while i < len(lines) and lines[i].strip().startswith("> "):
                buf.append(lines[i].strip()[2:])
                i += 1
            story.append(build_callout(" ".join(buf), s))
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
class ProjectDoc(BaseDocTemplate):
    def afterFlowable(self, fl):
        if isinstance(fl, Paragraph) and fl.style.name in ("H1", "H2"):
            text = fl.getPlainText()
            if text in ("Sommaire",):
                return
            level = 0 if fl.style.name == "H1" else 1
            key = hashlib.md5((text + str(self.page)).encode()).hexdigest()[:10]
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(text, key, level, level == 0)
            self.notify("TOCEntry", (level, text, self.page))


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
    canvas.setStrokeColor(COPPER)
    canvas.setLineWidth(0.8)
    canvas.line(MARG_L, PAGE_H - 13 * mm, PAGE_W - MARG_R, PAGE_H - 13 * mm)
    canvas.setFillColor(GREY)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(MARG_L, PAGE_H - 11 * mm,
                      sanitize("%s — %s" % (doc.meta.get("titre", ""),
                                            doc.meta.get("sous-titre", ""))))
    canvas.drawRightString(PAGE_W - MARG_R, PAGE_H - 11 * mm,
                           sanitize(doc.meta.get("version", "")))
    canvas.setStrokeColor(SAND_LINE)
    canvas.setLineWidth(0.6)
    canvas.line(MARG_L, 12.5 * mm, PAGE_W - MARG_R, 12.5 * mm)
    canvas.setFillColor(GREY)
    canvas.drawString(MARG_L, 8.5 * mm,
                      sanitize("Référentiel technique — %s" % doc.meta.get("date", "")))
    canvas.drawRightString(PAGE_W - MARG_R, 8.5 * mm, "Page %d" % canvas.getPageNumber())
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
             Paragraph("Sommaire", s["TocTitle"]),
             HRFlowable(width="100%", thickness=1.4, color=COPPER,
                        spaceBefore=1, spaceAfter=10),
             toc]
    story += parse_story(body_lines, s)
    doc.multiBuild(story)
    print("OK :", out)


if __name__ == "__main__":
    main()
