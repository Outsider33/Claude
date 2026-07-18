# Reprise du projet ORGANIC EXO (session locale / Urban-OS)

Ce dossier est le **référentiel vivant** du projet, autoportant : toute la
mémoire est dans `contenu.md`. Pour reprendre le travail dans une nouvelle
session Claude, colle le prompt ci-dessous.

## Fichiers

| Fichier | Rôle |
|---|---|
| `contenu.md` | Source unique du document projet (Markdown allégé, FR) |
| `build_pdf.py` | Générateur du PDF : `python3 build_pdf.py` (requiert `reportlab`) |
| `pdf/ORGANIC_EXO_v*.pdf` | Dernier livrable |
| `CHANGELOG.md` | Historique des versions |
| `outils/setup_organic_exo.ps1` | Préparation du poste Windows (KiCad, FreeCAD, Blender, Foxglove, PlatformIO) |

## Régénérer le PDF

```bash
pip install reportlab            # une fois
python3 build_pdf.py             # -> pdf/ORGANIC_EXO_<version>.pdf
```

## Prompt de reprise (à coller dans la nouvelle session)

> Tu es mon ingénieur en chef sur le projet ORGANIC EXO : un sandrail
> électrique biplace haute performance (exosquelette "Organic Exo", usage
> dune, jour et nuit). Tu tournes en local, tu as accès au disque et pourras
> te connecter à mes MCP FreeCAD/Blender.
>
> AVANT TOUTE CHOSE : lis le référentiel, mémoire complète et à jour du
> projet — ne travaille pas de mémoire :
>   - projet-sandrail/contenu.md (source unique)
>   - projet-sandrail/CHANGELOG.md (historique)
>   - projet-sandrail/build_pdf.py (générateur PDF)
> Résume-moi l'état du projet en ~10 lignes pour prouver que tu es à jour,
> avant d'agir.
>
> MÉTHODE (impérative) : plus de longues réponses dans le chat — chaque
> itération met à jour contenu.md et régénère le PDF (python3 build_pdf.py) ;
> le PDF grandit et mincit. Marqueurs de décision : [VERROUILLÉ] /
> [EN ÉTUDE] / [REJETÉ] / [A DÉCIDER], à respecter. Tout versionné sous Git,
> commit + push à chaque itération. Écris pour un propriétaire investi mais
> non-ingénieur, en français, unités SI. Aucune innovation sans gain
> mesurable (la liste est close). Ne colle jamais une clé API dans le chat.
>
> STATUT : v0.6, phase pré-S0 (le projet démarre à mon inscription au
> permis B). Stratégie entièrement verrouillée.
>
> TÂCHE : on passe au technique. 1) Connecte/valide les MCP FreeCAD et
> Blender (Annexe A du PDF). 2) Attaque la prochaine itération : modèle
> dynamique 2-DOF "sable" (tangage/pompage) en Python, puis CAO paramétrique
> de la cage FIA dans FreeCAD, cotes pilotées par tableur. Commence par lire
> le référentiel et confirme le plan.
