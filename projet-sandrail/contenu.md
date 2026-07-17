---
titre: ORGANIC EXO
sous-titre: Sandrail électrique biplace haute performance
version: v0.2
date: 17 juillet 2026
statut: Phase concept - architecture verrouillée, innovations en étude
---

# Mode d'emploi du document

Ce document est le **référentiel vivant** du projet. Il remplace les réponses en chat : chaque itération le fait grandir (nouvelles études) et mincir (synthèse des points tranchés, suppression du superflu). La source (`contenu.md`) est versionnée sous Git ; le PDF est régénéré à chaque révision.

Chaque élément de décision porte un marqueur d'état :

- **[VERROUILLÉ]** : décision actée, ne sera rouverte que sur fait nouveau majeur.
- **[EN ÉTUDE]** : piste active, protocole d'essai ou d'analyse défini.
- **[REJETÉ]** : écarté, avec motif conservé pour mémoire.
- **[A DÉCIDER]** : arbitrage attendu du propriétaire du projet (voir §8).

> Convention : unités SI, virgule décimale française. Les chiffres de dimensionnement restent des ordres de grandeur d'avant-projet, à valider par calcul détaillé (FEA) et essais instrumentés.

# Fiche projet et décisions verrouillées

## Cahier des charges figé

| Paramètre | Valeur | État |
| Configuration | Sandrail biplace, exosquelette tubulaire apparent | [VERROUILLÉ] |
| Masse en ordre de marche (GVW) | 1 150 kg (à vide ~980 kg + 2 occupants) | [VERROUILLÉ] |
| Batterie | 45 kWh, ~400 V, cellules 21700 type Molicel P45B (5C+), ~300 kg installée | [VERROUILLÉ] |
| Motorisation | 2 moteurs arrière indépendants, ~2 × 150 kW crête, réduction ~4:1, vectorisation de couple | [VERROUILLÉ] |
| Empattement / voies | 3 050 mm / ~1 950 mm | [VERROUILLÉ] |
| Débattements | 480 mm AV / 530 mm AR, amortisseurs bypass | [VERROUILLÉ] |
| Pneumatiques | Paddles 33" AR, skis/rib AV | [VERROUILLÉ] |
| Répartition des masses | 43/57 AV/AR en charge, CG <= 530 mm | [VERROUILLÉ] |
| Châssis | Hybride : quille-batterie structurelle aluminium + exosquelette tubulaire | [VERROUILLÉ] |
| Rigidité torsionnelle cible | >= 3 000 Nm/deg | [VERROUILLÉ] |
| Cas de charge dimensionnant | Réception à plat 2 m : 8 g de calcul, 12 g ultime | [VERROUILLÉ] |
| Thermique | Deux boucles liquides + chiller batterie 4 kW, ambiance 45 °C, poussière fine | [VERROUILLÉ] |
| Langage esthétique | « Organic Exo » (Pagani × Ferrari) — voir §3 | [VERROUILLÉ] |
| Usage | Terrain privé, domaines fermés, compétition future éventuelle — pas de route ouverte | [VERROUILLÉ] |

## Décisions nouvelles de cette itération

1. **Cellule de sécurité en acier carbone CDS aux cotes FIA**, exosquelette 4130 autour — voir §6.2. C'est un amendement structurant de l'itération 1 (l'arceau principal en 44,5 × 2,4 ne passait pas les minima FIA).
2. **Pas d'homologation route pour ce véhicule** : la voie L7e-B2 est mathématiquement incompatible (15 kW / 450 kg) — voir §6.4.
3. **Priorisation des prototypes low-cost** : télémétrie suspension (n°2), nœuds génératifs polymère (n°4), estimation d'état RTK (n°8) — voir §4.
4. **Restitution AR par paliers** : pacenotes audio synthétiques d'abord, LED périphériques ensuite, HUD optique en phase 3 — aucun écran au cockpit — voir §5.
5. **Chaîne énergie confirmée** : NMC 21700 + 2 moteurs à flux axial (référence EMRAX 268 LC) ; hydrogène, prolongateur thermique et moteurs-roue rejetés — voir §7.

# Synthèse de l'architecture (acquis de l'itération 1)

Cette section condense le diagnostic initial pour que le document soit autoportant. Le détail des calculs reste disponible dans l'historique v0.1.

## Structure

Le cas dimensionnant est la réception à plat après un saut de 2 m : vitesse d'impact v = (2gh)^{1/2} soit ~6,3 m/s, ~22,6 kJ à absorber. Avec ~0,48 m de course utile (débattement + pneu), la décélération moyenne vaut ~4,2 g ; avec l'amortissement progressif des bypass on retient **8 g de calcul, 12 g ultime**. En réception cabrée, chaque tour d'amortisseur arrière voit ~32 kN, dimensionné à **~47 kN (coefficient 1,5)**.

Principes verrouillés :

- **Triangulation totale** : un tube 44,5 × 2,4 mm travaille en traction/compression (~145 kN axial) ; il ne casse qu'en flexion. Donc tout point d'ancrage (suspension, amortisseur, harnais) atterrit à moins de ~25 mm d'un nœud triangulé ; aucun quadrilatère non contreventé dans un chemin d'effort.
- **Quille-batterie structurelle** : le caisson batterie (6061/7075 boulonné-collé) court entre et derrière les sièges — plancher, lest et caisson de torsion à la fois, ~1/3 de la rigidité châssis. L'exosquelette l'enveloppe.
- **8 grappes de nœuds principales** : cloison AV skis, tours d'amortisseurs AV liées à l'arceau de planche de bord, reprises de triangles inférieurs aux coins AV de la quille, jonction montant A × quille, pieds d'arceau principal × coins AR de quille (grappe la plus chargée), barre de harnais, tours AR en treillis double-K vers le sommet d'arceau, pivots de bras tirés + berceau moteurs en queue de quille.
- **Tubes** : primaires 44,5 × 2,4 ; diagonales 38,1 × 1,6 ; reprises de suspension 44,5 × 3,0 ; TIG. (Amendé au §6.2 pour la cellule de sécurité.)
- **Nœuds génératifs imprimés** (Ti-6Al-4V ou Scalmalloy, HIP, interfaces usinées) aux jonctions les plus chargées : -30 à -40 % de masse vs goussets mécano-soudés, et pièces d'orfèvrerie visibles (§3).

## Masses et motricité

Cible **43/57 AV/AR en charge, CG <= 530 mm** (modèle de masses : ~500 mm avec la quille batterie à ~300 mm du sol).

- Poussée maximale en propulsion : a/g = µ · f_{R} / (1 - µ · h/L). Avec µ paddle 0,7-0,9, f_{R} = 0,57, h/L = 0,174 : **0,45-0,6 g d'accélération soutenue dans le sable meuble** — limitée par la motricité, pas par la puissance.
- Le seuil de cabrage (~2,5 g) est inatteignable : le couple instantané ne fera jamais boucler la voiture. Le vrai sujet est un **contrôle de traction à consigne de glissement sable** : les paddles poussent au maximum à 20-35 % de glissement (contre 5-10 % sur bitume).
- Pourquoi pas 65 % AR comme les sandrails classiques : perte d'appui AV dans les bols, lacet pendulaire. Pourquoi pas moins : les paddles ont besoin de charge, et un nez léger fait déjauger les skis au lieu de labourer.
- **Contrôle d'assiette en vol** : les masses tournantes AR (~6 kg·m²) freinées depuis 80 km/h transfèrent ~330 N·m·s contre I_{tangage} ~1 150 kg·m², soit **~16°/s d'autorité à piquer** ; un coup de couple pleine charge donne l'autorité à cabrer. Règles logicielles : régénération coupée en aérien sauf commande d'assiette, rampe de couple limitée à la lèvre du saut. Rapport k²/(ab) ~0,85.

## Thermique (45 °C, poussière fine)

Budget : ~90 kW mécaniques soutenus -> moteurs ~5,5 kW + onduleurs SiC ~2 kW + pertes I²R batterie ~3,3 kW, soit **~12 kW continus**, transitoires 25-30 kW tamponnés par l'inertie thermique.

- **Boucle A (traction, 65 °C max)** : moteurs + onduleurs, eau glycolée. Écart à l'ambiante ~20 K seulement -> UA ~0,5-0,6 kW/K : **0,30-0,35 m² de surface de radiateur** et 1 800-2 000 CFM de ventilateurs étanches à forte pression statique, montés haut sur le pont arrière — jamais dans le nez (sablage, ensevelissement).
- **Boucle B (batterie, fenêtre 25-40 °C)** : impossible de radier sous l'ambiante -> **chiller frigorifique 4 kW obligatoire** (compresseur électrique ~1,5 kW, condenseur dédié), plaques froides fond + inter-modules à ~25 L/min, delta cellule-cellule < 4 K. **Pré-refroidissement du pack à 22-25 °C avant session** : les 15 K de marge absorbent ~1,25 kWh, soit ~20 minutes à fond avant que le chiller n'ait à gagner le duel.
- **Durcissement poussière** : ailettes grossières 8-10 FPI derrière des pré-grilles inox amovibles, cycles d'inversion des ventilateurs (purge), prises d'air au-dessus de la ligne de caisse, pack IP67, connecteurs IP69K, reniflards Gore, moteurs liquides entièrement fermés (jamais de rotor ventilé ouvert), électronique tropicalisée derrière pré-filtre cyclonique, sabots UHMW/céramique sur tubes bas et bords d'attaque des radiateurs.

# Design lock : le langage « Organic Exo »

**[VERROUILLÉ]** — Direction B de l'itération 1, confirmée. L'ingénierie *est* le design : rien n'est caché, tout ce qui se voit travaille.

## Vocabulaire formel

- **Épine dorsale continue** : une ligne structurelle fluide qui court du sommet de l'arceau jusqu'à la queue, jamais interrompue — c'est la signature de profil.
- **Nœuds génératifs exposés** : les jonctions imprimées topologiquement optimisées sont des pièces d'orfèvrerie apparentes, finition brute de HIP + interfaces polies.
- **Ligne de tension latérale** unique, tendue façon Ferrari, matérialisée par la lisse haute des flancs — pas de surfaces enveloppantes.
- **Quatre bypass dressés en tuyaux d'orgue** sur le pont arrière : les amortisseurs sont la cathédrale mécanique du véhicule.
- **Visserie usinée apparente** : têtes fraisées inox/titane calibrées, alignées — la boulonnerie participe au dessin.

## Matières et finitions

| Zone | Matière / finition |
| Tubes exosquelette | Titane torché (irisations bleu-bronze) ou 4130 verni satin selon coût |
| Quille batterie | Carbone mat / aluminium usiné brut |
| Nœuds génératifs | Ti / Scalmalloy brut, interfaces usinées brillantes |
| Accents | Cuivre bruni (échangeurs, durites gainées inox) |

## Interdits (garde-fous esthétiques)

- Aucune carrosserie enveloppante, aucun capot plein.
- **Aucun écran au cockpit** — contrainte fondatrice du §5.
- Pas de plastiques peints, pas de faux carbone, pas d'autocollant fonctionnel non justifié.

## Conséquences d'ingénierie

Les nœuds deviennent des surfaces de classe A : tolérances de fonderie/impression serrées, ébavurage soigné. Le câblage HT chemine **dans** les tubes ou dans la quille (gaines orange visibles uniquement aux entrées/sorties réglementaires — voir §6.3). Les radiateurs sont dessinés comme des éléments graphiques assumés, pas dissimulés.

# Dix innovations transversales (hors automobile)

Filtre appliqué : chaque concept doit être **prototypable à l'atelier** (impression 3D polymère, ESP32/Teensy/Raspberry Pi, essais de terrain instrumentés) avant tout engagement de fabrication métal. ROI = gain attendu / (coût + risque du proto).

## Tableau de synthèse

| N° | Origine | Concept adapté | Coût proto | ROI |
| 1 | Coupe de l'América (AC75) | Contrôle d'assiette prédictif (feedforward) | ~250 € | Élevé |
| 2 | VTT descente | Télémétrie suspension par histogrammes | ~300 € | **Très élevé** |
| 3 | Drone FPV racing | Blackbox haute fréquence + méthode de tuning PID | ~150 € | Élevé |
| 4 | Aérospatial | Nœuds génératifs validés en polymère d'abord | ~400 € | **Très élevé** |
| 5 | Robotique molle | Siège à « jamming » granulaire moulé au pilote | ~80 € | Moyen-élevé |
| 6 | Biomimétisme | Banc à tambour pour géométrie de pales de paddle | ~350 € | Élevé |
| 7 | Voile hauturière / alpinisme | Gréement textile Dyneema (sangles, manilles) | ~150 € | Moyen |
| 8 | Formula Student Driverless | Glissement vrai par RTK-GNSS + EKF | ~450 € | **Très élevé** |
| 9 | Datacenters / McMurtry | Essai d'immersion diélectrique d'un module | ~600 € | Moyen |
| 10 | Alpinisme / ultra-endurance | Monitoring physiologique pilote + gilet à froid | ~300 € | Élevé |

**[EN ÉTUDE - priorité 1]** : n° 2, 4 et 8 — trois bancs, ~1 150 € au total, qui dé-risquent respectivement le réglage châssis, les pièces structurelles les plus chères, et la fonction de performance n°1 (traction sable).

## Détail des concepts

### 1. Contrôle d'assiette prédictif (AC75, Coupe de l'América)

Les AC75 tiennent leur vol grâce à une boucle rapide alimentée par capteurs d'altitude et centrale inertielle, avec anticipation (feedforward) plutôt que simple réaction. Adaptation : capteurs de distance au sol (ToF/ultrason durcis) au nez + IMU -> pré-armement des solénoïdes de bypass semi-actifs avant la compression, gestion de l'assiette d'atterrissage couplée au contrôle de couple en aérien (§2). **Proto** : ESP32 + BNO085 + 2 × VL53L1X sur un VTT de descente ou une mule RC 1/5, comparaison passif vs pré-armé sur bosse calibrée.

### 2. Télémétrie suspension par histogrammes (VTT DH)

Le VTT de descente a démocratisé une méthode de pro : potentiomètres linéaires à 500-1 000 Hz sur chaque amortisseur, puis **histogrammes de vitesse de tige** — la forme de l'histogramme dit objectivement où manquent compression ou détente, fin ou fort débit. C'est exactement la méthode de réglage des bypass. **Proto** : 4 potentiomètres linéaires 200 mm (~35 €/pièce) + ESP32 + carte SD, dépouillement Python (je fournis l'outil). Utilisable dès la mule, puis à vie sur le véhicule.

### 3. Blackbox et méthode de tuning FPV (drone racing)

Betaflight a montré qu'une boucle de pilotage se règle en **rejouant des logs haute fréquence** (blackbox), pas en devinant. Notre contrôle de traction et la vectorisation de couple seront développés pareil : Teensy 4.1, logs 2 kHz (consignes, glissements, couples, courants), rejeu et analyse offline. Bonus : liaison vidéo numérique type FPV pour la vue stand pendant les essais. **Proto** : firmware + outil de rejeu avant même que le véhicule existe, validé sur banc à rouleau sable (n°6).

### 4. Nœuds génératifs : polymère d'abord (aérospatial)

Méthodologie aérospatiale : topologie optimisée -> **impression polymère (FDM/SLS, échelle 1:2 puis 1:1)** -> essais à rupture sur presse d'atelier avec capteur de force -> corrélation du modèle FEA -> seulement ensuite, impression métal ou moulage. On achète de la confiance à 15 € la pièce au lieu de 1 500 €. **Proto** : les 3 nœuds les plus chargés (tours AR, pieds d'arceau, reprise de triangle), 3 exemplaires chacun, rupture documentée. Le facteur d'échelle polymère->métal est calibré par la corrélation FEA, pas supposé.

### 5. Siège à jamming granulaire (robotique molle)

Le « jamming » : un sac de granulés devient rigide sous vide, épousant la forme qu'il enserrait. Adaptation : coussin d'assise et dossier **moulés au pilote** (comme les sièges moulés de monoplace, mais re-moulables en 5 minutes pour changer de pilote), meilleure transmission des G, moins de points chauds. **Proto** : sac TPU étanche + billes EPS + pompe à vide manuelle, essai sur siège baquet existant.

### 6. Géométrie de pales bio-inspirée (biomimétisme)

Le serpent sidewinder et les lézards des sables exploitent des angles d'attaque et des textures qui maximisent la poussée dans un milieu granulaire qui se dérobe. Le paddle est notre unique point de contact moteur : angle, cambrure, espacement et texture des pales méritent mieux que le catalogue. **Proto** : banc à tambour rotatif rempli du sable cible + couple-mètre, pales imprimées interchangeables vissées sur un pneu support ; mesure poussée/couple/enfouissement à glissement contrôlé.

### 7. Gréement textile Dyneema (voile / alpinisme)

Sangles de limitation de débattement, manilles textiles, arrêtoirs : le Dyneema fait le travail de l'acier à -80 % de masse, sans fatigue vibratoire ni foudroyage d'arête. Points d'attention : UV et abrasion au sable -> gaines sacrificielles. **Proto** : chèvre d'atelier + dynamomètre, essais de rupture neuf / après 50 h d'exposition sable-UV, protocole de remplacement calendaire.

### 8. Glissement vrai par RTK-GNSS + EKF (Formula Student Driverless)

Le contrôle de traction sable a besoin du **glissement réel**, donc de la vitesse sol vraie — que l'odométrie ne donne pas quand tout patine. Solution éprouvée en FS Driverless : GNSS RTK (u-blox ZED-F9P, correction locale par base fixe) fusionné IMU dans un EKF ; vitesse Doppler précise au cm/s, 10 Hz GNSS + 100 Hz inertiel. **Proto** : base + rover (~450 €), validation en voiture de série sur piste, puis intégration comme capteur maître du TC. Réutilisé tel quel par le système AR (§5).

### 9. Immersion diélectrique d'un module batterie (datacenters, hypercars)

Alternative aux plaques froides si le delta cellule-cellule dérive à 45 °C : immersion monophasique (huile diélectrique), uniformité thermique excellente et propagation d'emballement retardée, au prix de la masse de fluide et de l'étanchéité. **Proto** : un module sacrifiable instrumenté (thermocouples), bac inox, cyclage charge/décharge comparatif plaque froide vs immersion. Décision sur données, pas sur mode.

### 10. Le pilote comme premier composant thermique (alpinisme / ultra)

À 45 °C, le premier élément qui « derate » est le pilote : jugement, temps de réaction, constance. Les sports d'ultra-endurance ont les outils : capteur de température centrale (type CORE), variabilité cardiaque, gilets à matériaux à changement de phase, protocoles d'hydratation pesée. **Proto** : monitoring systématique pendant les essais, corrélation performance/température centrale, seuils d'alerte intégrés à la télémétrie (et plus tard aux pacenotes audio : « pause thermique »).

# Interface pilote-machine et système AR topographique

**Contrainte fondatrice (design lock §3) : zéro écran au cockpit.** Le système restitue une information de pilotage minimale, au bon moment, ou se tait.

## Architecture en quatre couches

### Couche 1 — Acquisition : drone compagnon

- Drone photogrammétrique grand public (classe DJI Mini 4 Pro) : vol en double grille à 60-80 m, recouvrement 80/70, GSD 2-3 cm/px. Suffisant pour une ligne de course dans les dunes ; LiDAR inutile en phase 1.
- Géoréférencement : 4-6 cibles au sol (GCP) levées au RTK — la même base ZED-F9P que l'innovation n°8.
- Un scan avant session (10-15 min de vol pour ~1 km²). Le terrain dunaire bouge en jours/semaines, pas en minutes : **le « temps réel » du système, c'est la position du véhicule, pas le scan**.

### Couche 2 — Traitement : mesh 3D

- Photogrammétrie open source **WebODM** sur portable de terrain (GPU) : nuage dense -> mesh -> MNT/orthophoto en 30-60 min.
- Post-traitement Python (Open3D/PDAL) : pentes, dévers, courbures, détection de lèvres et cuvettes ; plus tard, classification des zones molles par texture/albédo.

### Couche 3 — Ligne de course

- Solveur de trajectoire à courbure minimale pondérée par un **coût terrain** : dévers latéral, mollesse estimée, visibilité de lèvre, marge d'atterrissage. Implémentation Python/CasADi, recalcul segment par segment.
- Sortie : polyligne géoréférencée + métadonnées par segment (vitesse conseillée, avertissements) — consommée par la couche 4.

### Couche 4 — Restitution au pilote, par paliers

**Palier A [VERROUILLÉ - MVP] : pacenotes audio synthétiques.** Le rallye a validé le concept depuis 60 ans : un copilote qui parle bat un écran qu'on n'a pas le temps de lire. Génération automatique des notes depuis le mesh + la ligne (« droite 4 ouvre, lèvre aveugle 80, mou à la sortie »), déclenchées par la position RTK, voix dans le casque. Coût matériel : ~0 € (le RTK existe déjà). Latence : nulle. Poussière : sans objet.

**Palier B [EN ÉTUDE] : bandeau LED périphérique.** Un ruban LED discret dans le halo du cockpit (vision périphérique) : écart latéral à la ligne (glissement du point lumineux), alerte compression/lèvre (impulsion couleur). ESP32 + ruban, ~60 €. Zéro accommodation visuelle, lisible en plein soleil, cohérent avec le design lock (la LED est une lumière, pas un écran).

**Palier C [EN ÉTUDE - phase 3] : HUD optique minimal.** Deux options : combiner monoculaire sur visière (micro-OLED 0,71" + optique, DIY exigeant : luminosité plein désert difficile) ou lunettes waveguide grand public pilotables en BLE (classe Even Realities G1 / Vuzix Z100 : symbologie fixe écran — 3 chevrons de ligne + delta de vitesse, jamais de rendu 3D). Le « world-locked » AR complet est explicitement **hors périmètre** : latence, vibrations, poussière sur l'optique et lumière du désert le condamnent en phase actuelle.

**[REJETÉ]** : écrans cockpit (design lock), scan drone temps réel en vol d'accompagnement (complexité liaison + réglementation drone + ROI faible : le terrain ne change pas pendant la session).

## Les cinq transferts retenus pour l'interface

1. **Pacenotes synthétiques** (rallye WRC) — l'information de pilotage est temporelle, pas spatiale.
2. **Photogrammétrie drone** (topographie minière) — le mesh centimétrique à coût dérisoire.
3. **Localisation RTK + EKF** (Formula Student Driverless) — le tronc commun TC + AR.
4. **Waveguides grand public** (AR consumer) — si HUD il y a, il sera acheté, pas développé.
5. **Retour haptique volant** (sim racing, inversé) — vibreurs dans le moyeu : alerte lèvre/ligne quand l'audio est saturé. Proto ESP32 + ERM, ~40 €. [EN ÉTUDE]

# Conformité FIA et usage hors compétition

## Positionnement réglementaire : lucidité d'abord

Les catégories cross-country FIA pertinentes sont **T3** (prototypes légers, Annexe J art. 286) et **T4** (SSV de série, art. 286A). État des lieux honnête :

- **Il n'existe pas aujourd'hui de classe T3/T4 100 % électrique ouverte en championnat** (W2RC). Les programmes électriques/hydrogène courent en démonstration ou catégories expérimentales (Dakar Future / Mission 1000).
- **T3 interdit les aides au pilotage** (contrôle de traction, ABS). Notre TC à consigne de glissement est central au concept : en l'état, le véhicule ne serait pas conforme T3 même thermique. Conséquence gelée : **mode « TC off » câblé physiquement** prévu dès la VCU, pour ne fermer aucune porte.
- Stratégie retenue **[VERROUILLÉ]** : construire **« FIA-ready, pas FIA-bound »** — cellule de sécurité et sécurité HT au niveau de l'esprit des textes FIA, dossier technique tenu à jour (certificats matière, qualification soudeur, CAO de la cage), pour pouvoir candidater vite si une classe électrique ouvre, et passer les contrôles techniques d'événements privés (Maroc, UAE) qui s'alignent sur la FIA.

> Les numéros d'articles et valeurs ci-dessous sont établis sur l'Annexe J en vigueur (édition 2026 consultée via fia.com) ; toute cote sera re-vérifiée sur le texte de l'année au moment du dépôt — l'Annexe J évolue chaque année.

## Ce qui se fige dès le dessin du châssis (invariants art. 283 - équipement de sécurité cross-country)

**Amendement majeur de l'itération 1.** Les minima FIA pour l'armature de sécurité imposent pour l'arceau principal du tube **50 × 2,0 mm ou 45 × 2,5 mm**, en **acier au carbone non allié, étiré à froid, sans soudure** (résistance mini 350 N/mm²). Notre primaire d'itération 1 (44,5 × 2,4, 4130 chromoly) est doublement non conforme pour la cage : cote insuffisante **et** acier allié (le chromoly ne passe que via des homologations nationales spécifiques).

**Décision [VERROUILLÉ]** : architecture à deux niveaux de structure —

1. **Cellule de sécurité** (arceau principal, arceaux/montants avant, entretoises diagonales et de toit, jambes de force arrière, renforts de portière) : acier carbone CDS type E355 aux cotes FIA (50 × 2,0 principal ; 38 × 2,5 ou 40 × 2,0 autres éléments), pieds d'arceau sur platines et goussets réglementaires, dégagement casque respecté.
2. **Exosquelette périphérique** (épine dorsale, lisses esthétiques-structurelles, supports d'échangeurs, cadres de skis) : 4130 autorisé, puisqu'il n'est pas l'armature de sécurité.

Autres invariants intégrés dès la CAO (coût nul maintenant, reconstruction sinon) :

- **Ancrages harnais 6 points** aux angles réglementaires, sur nœuds (harnais norme FIA 8853-2016).
- **Sièges norme FIA 8862** et leurs supports aux points prescrits (pas de siège « à côté » des points).
- **Extincteur** : système plombé + fixations métalliques prescrites, déclencheurs intérieur/extérieur.
- **Coupe-circuit général** : intérieur accessible aux deux occupants harnachés + commande extérieure signalée.
- Anneaux de remorquage AV/AR signalés, filets/portes tubulaires, dégagements de secours chronométrables (évacuation < 7 s visée).

## Spécifique haute tension (esprit FIA véhicules électriques + socle ECE R100)

À intégrer dès la CAO du pack et du câblage :

- **Caisson batterie = structure anti-intrusion** avec zone d'écrasement sacrificielle >= 50 mm sur tout le pourtour, fixations dimensionnées aux g ultimes (12 g vertical, 20 g longitudinal en crash réglementaire).
- **Ségrégation HT** : cheminements hors zones de déformation, gaine orange normalisée aux traversées visibles, connecteurs à **interlock HVIL** sur toute la boucle, pas de HT dans l'habitacle.
- **IMD** (surveillance d'isolement) permanent, **sectionneur de service** manœuvrable sans outil, **voyant d'état sécurité** (vert/rouge) visible des secours, équipotentialité de toutes les masses (< 0,1 ohm), IP67 pack / IP69K connecteurs.
- Signalétique de secours normalisée + **fiche d'intervention** (comme l'exigent les organisateurs) rédigée dès la V1.
- Habilitation électrique de l'intervenant pack (B2XL ou équivalent) : contrainte d'organisation d'atelier, pas de châssis — mais notée ici pour mémoire.

## Usage hors compétition : la réponse réglementaire route

Question posée : « être autorisé à le conduire hors compétition ». Analyse des trois voies (France/UE) :

| Voie | Exigence clé | Verdict |
| Réception à titre isolé (RTI, DREAL) en catégorie voiture | Conformité quasi-série : crash, CEM, freinage réglementaire, bruit, éclairage e-marqué... | Irréaliste pour un prototype amateur (coûts d'essais prohibitifs) — **[REJETÉ]** |
| Quadricycle lourd **L7e-B2** (règl. UE 168/2013) | **<= 15 kW net, <= 450 kg à vide (hors batteries), <= 90 km/h** + actes délégués 3/2014, 44/2014, 134/2014 | Incompatible par construction : 300 kW crête, ~680 kg hors pack. Une variante bridée à 15 kW n'a aucun sens projet — **[REJETÉ]** |
| Usage fermé : terrains privés, domaines, événements | Autorisation du propriétaire/organisateur, assurance RC circuit, licence FFSA/UFOLEP selon cadre | **[VERROUILLÉ]** — c'est le cadre du projet |

Conséquences pratiques verrouillées : transport sur **remorque** (prévoir PTAC attelage ~1,6 t : véhicule ~980 kg + remorque), assurance RC terrain/circuit dès les premiers essais, repérage de terrains de dunes autorisés (domaines privés FR/ES, Merzouga/Erg Chebbi au Maroc, événements UAE avec contrôle technique propre). Si un usage route devient un vrai besoin un jour : acheter un SSV homologué du commerce — hors périmètre de ce projet.

# Énergie et motorisation : étude complète

## Sources d'énergie candidates

| Source | Densité / rendement | Verdict projet |
| **Li-ion NMC/NCA 21700** (P45B) | 250-300 Wh/kg cellule ; 5C+ ; chaîne batterie->roue ~85-90 % | **[VERROUILLÉ]** — référence du projet |
| Li-ion LFP | 160-210 Wh/kg ; très sûre, cyclage long | +100 kg au pack à énergie égale : pénalise CG et masse — [REJETÉ] pour la traction, **retenue pour le tampon statique de recharge** |
| LTO | 70-90 Wh/kg ; charge en ~10 min ; robustesse extrême | Densité rédhibitoire — [REJETÉ] |
| Sodium-ion | ~160 Wh/kg ; bon marché ; docile au froid/chaud | Masse — [REJETÉ] traction ; candidate future du tampon statique |
| Semi-solide / tout-solide | 350-500 Wh/kg annoncés | Pas d'offre fiable en petite série à date — **veille active**, le caisson quille est dessiné pour un repack futur |
| Supercondensateurs | Puissance seulement | Inutile : les P45B couvrent déjà 5C — [REJETÉ] |
| **Pile à combustible H2 (PEM)** | Système 45-55 % ; H2->roue ~40-50 % ; plein en 5 min | Stockage 700 bar + poussière fine + condenseur à 45 °C + logistique H2 au désert : [REJETÉ] pour cette plateforme ; veille sur les programmes H2 du Dakar |
| Prolongateur thermique (essence/rotatif) | ~30-35 % ; essence->roue ~25-30 % | Contraire à l'ADN du projet (bruit, chaleur, complexité) — [REJETÉ] |
| Solaire embarqué | ~300 W crête sur 1,5 m² exploitable | Négligeable en traction ; **retenu en auxiliaire** : maintien du froid pack et télémétrie au bivouac |
| Récupération au freinage | 5-15 % récupérés hors-piste | **[VERROUILLÉ]** — déjà spécifiée, coupée en aérien sauf commande d'assiette |

## Logistique de recharge terrain [EN ÉTUDE]

Remorque énergie : champ solaire pliable 4-5 kWc + **tampon stationnaire LFP ~20 kWh** + chargeur AC 11-22 kW. Ordres de grandeur : recharger 45 kWh au solaire seul prend 1,5-2 jours — le tampon (chargé la nuit ou en continu) ramène la recharge véhicule à ~2-4 h. Secours : groupe HVO ou borne CCS mobile 50 kW quand la logistique le permet. Dimensionnement précis à la prochaine itération selon le lieu d'essais retenu (§8).

## Technologies de moteurs : panorama et rendements

| Technologie | Rendement pic / cycle | Densité | Lecture projet |
| **PMSM flux axial** (EMRAX, Phi-Power ; YASA = OEM seulement) | 96-98 % / 92-96 % | 8-10 kW/kg | **Référence** : couple massique inégalé, refroidissement liquide intégrable boucle A |
| PMSM flux radial (Cascadia iM225, unités Tesla réemployées) | ~96 % / 90-94 % | 3-5 kW/kg | Plan B économique éprouvé (Tesla SDU d'occasion), plus lourd |
| Asynchrone (induction) | 92-94 % / 88-92 % | 2-4 kW/kg | Rustique, sans aimants, mais lourd et moins efficient : pertes = chaleur à évacuer à 45 °C — écarté |
| Réluctance commutée | 90-95 % | 3-5 kW/kg | Sans terres rares, très robuste, mais ondulation de couple + quasi aucune offre petite série — veille |
| Moteurs-roue (Elaphe) | ~94 % | Intégrée | **[REJETÉ] net** : masse non suspendue rédhibitoire avec 480-530 mm de débattement |

**Sélection [VERROUILLÉ]** : 2 × **EMRAX 268 LC** (refroidissement liquide, ~20 kg pièce, ~200 kW / 500 Nm crête, ~100-110 kW continu chacun) + onduleurs SiC (classe Cascadia CM/PM), réducteurs droits ~4:1. Vérification de cohérence : 2 × ~107 kW continus = ~214 kW disponibles en continu pour un besoin soutenu de ~90 kW — la marge thermique est confortable, la crête (jusqu'à ~2 × 200 kW brefs, bridée à 2 × 150 kW par la VCU en V1) reste un rafale-budget géré par le contrôle thermique. Le derating des aimants est surveillé par sondes bobinage + rotor estimé.

## Rôle de Claude dans le projet

Ce que je prends en charge, itération après itération :

- **Calcul et architecture** : notes de calcul (comme ce document), modèles dynamiques Python (le modèle 2-DOF tangage/pompage « sable » est le livrable proposé de la prochaine itération), mise en données FEA (CalculiX/PrePoMax) et dépouillement.
- **CAO paramétrique scriptée** : géométrie de cage et de quille en CadQuery/FreeCAD Python — la cage FIA se régénère quand une cote change.
- **Logiciel embarqué** : firmware TC/VCU (Teensy, C/C++), outil blackbox + rejeu, dashboards télémétrie, solveur de ligne de course, générateur de pacenotes.
- **Sourcing et dossiers** : BOM comparatives chiffrées, veille réglementaire FIA (alerte si une classe électrique ouvre), dossier technique « FIA-ready », protocoles d'essais des dix innovations et dépouillement des résultats.
- **Ce document** : tenue du référentiel versionné (Git) et régénération du PDF à chaque itération.

Ce que je ne remplace pas : les essais physiques, le soudeur qualifié (la cage exige un dossier de qualification), le bureau de contrôle éventuel, et la responsabilité sécurité HT en atelier.

# Feuille de route et décisions attendues

## Phases

| Phase | Contenu | Sortie |
| P0 — Validation numérique (en cours) | Modèle dynamique 2-DOF sable, CAO cage FIA paramétrique, FEA quille | Géométrie figée pour mule |
| P1 — Bancs low-cost | Innovations n° 2, 4, 8 (puis 1, 3, 6 selon budget) | Données de dimensionnement réelles |
| P2 — Mule | Châssis simplifié 1 moteur, TC v1, télémétrie complète | Validation TC + suspensions |
| P3 — Châssis définitif | Cellule FIA + exosquelette + nœuds métal | Véhicule roulant |
| P4 — Interface | Pacenotes (palier A), LED (palier B), physio pilote | Système complet |

## Décisions attendues [A DÉCIDER]

1. **Enveloppe budgétaire globale** — elle arbitre EMRAX neuf (~2 × 9 k€ avec onduleurs) vs chaîne Tesla réemployée (~5-7 k€ totaux, +40 kg).
2. **Validation du trio d'innovations prioritaires** (n° 2, 4, 8) ou autre sélection.
3. **Lieu d'essais principal** (dunes françaises privées / Espagne / Maroc) — il dimensionne la logistique énergie du §7.
4. **Drone** : un appareil photogrammétrique est-il déjà disponible, ou à budgéter (~800 €) ?
5. **Compatibilité T3 stricte** : faut-il sanctuariser le mode « TC off » homologable, ou assumer un véhicule 100 % hors championnat ?
6. **Prochaine itération proposée** : modèle dynamique 2-DOF + CAO paramétrique de la cage FIA. Valider ou réorienter.

# Journal des révisions

| Version | Date | Contenu |
| v0.1 | Itération 1 (chat, Claude desktop) | Diagnostic initial : structure, masses/traction, thermique, deux directions de style |
| v0.2 | 17 juillet 2026 | Premier PDF de référence. Verrouillage « Organic Exo » ; synthèse autoportante de v0.1 ; 10 innovations transversales priorisées ; architecture AR 4 couches par paliers ; conformité FIA (amendement cellule acier CDS aux cotes art. 283, stratégie « FIA-ready ») ; rejet motivé des voies route (RTI, L7e-B2) ; étude énergie/moteurs complète et sélection EMRAX ; feuille de route P0-P4. Minci : la prose de l'itération 1 est remplacée par la synthèse du §2 |

# Références

- FIA — Annexe J, textes officiels (dont art. 286A éd. 2026) : www.fia.com/regulation/category/100
- Catégorie T3 (synthèse) : en.wikipedia.org/wiki/Group_T3
- Règlement (UE) n° 168/2013 (catégories L, dont L7e-B2) : eur-lex.europa.eu (CELEX 32013R0168)
- Classification quadricycles UE (synthèse) : en.wikipedia.org/wiki/Quadricycle_(EU_vehicle_classification)
- Données constructeurs citées (EMRAX, Molicel, u-blox, WebODM) : fiches techniques publiques des fabricants — à re-confirmer au devis.
