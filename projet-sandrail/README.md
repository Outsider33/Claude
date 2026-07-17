# Projet ORGANIC EXO — Sandrail électrique biplace

Référentiel technique **vivant** du projet. La règle de travail : plus de réponses
longues en chat — chaque itération met à jour ce dossier et régénère le PDF, qui
grandit (nouvelles études) et mincit (synthèse des points tranchés).

## Contenu

| Fichier | Rôle |
|---|---|
| `contenu.md` | Source unique du document (Markdown allégé, en français) |
| `build_pdf.py` | Générateur PDF (reportlab) : couverture, sommaire, tableaux, encadrés |
| `pdf/ORGANIC_EXO_<version>.pdf` | Livrable de l'itération |
| `CHANGELOG.md` | Journal des révisions (miroir du §Journal du document) |

## Régénérer le PDF

```bash
pip install reportlab
python3 build_pdf.py
```

## Protocole d'itération

1. Éditer `contenu.md` (mettre à jour les marqueurs d'état : VERROUILLÉ / EN ÉTUDE / REJETÉ / A DÉCIDER).
2. Incrémenter `version:` et `date:` dans l'en-tête de `contenu.md`.
3. Ajouter l'entrée au §Journal des révisions et à `CHANGELOG.md`.
4. `python3 build_pdf.py`, commit du tout (source + PDF).
