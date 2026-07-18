---
titre: ORGANIC EXO
sous-titre: Sandrail électrique biplace haute performance
version: v0.3
date: 17 juillet 2026
statut: Budget acté (30 k EUR) - chaîne de traction en arbitrage A/B
---

# Mode d'emploi du document

Ce document est le **référentiel vivant** du projet. Il remplace les réponses en chat : chaque itération le fait grandir (nouvelles études) et mincir (synthèse des points tranchés, suppression du superflu). La source (`contenu.md`) est versionnée sous Git ; le PDF est régénéré à chaque révision.

Chaque élément de décision porte un marqueur d'état :

- **[VERROUILLÉ]** : décision actée, ne sera rouverte que sur fait nouveau majeur.
- **[EN ÉTUDE]** : piste active, protocole d'essai ou d'analyse défini.
- **[REJETÉ]** : écarté, avec motif conservé pour mémoire.
- **[A DÉCIDER]** : arbitrage attendu du propriétaire du projet (voir §11).

> Convention : unités SI, virgule décimale française. Les chiffres de dimensionnement restent des ordres de grandeur d'avant-projet, à valider par calcul détaillé (FEA) et essais instrumentés. Ce document est écrit pour un propriétaire investi mais non-ingénieur : chaque concept technique est expliqué au moment où il sert.

# Fiche projet et décisions verrouillées

## Cahier des charges figé

| Paramètre | Valeur | État |
| Configuration | Sandrail biplace, exosquelette tubulaire apparent | [VERROUILLÉ] |
| Budget global | **30 000 EUR** (étalement possible sur 2 ans, voir §10) | [VERROUILLÉ] |
| Masse en ordre de marche (GVW) | 1 150 kg (à vide ~980 kg + 2 occupants) | [VERROUILLÉ] |
| Usage | Terrain fermé, **jour et nuit**, plaisir d'abord ; compétition possible sans reconstruction | [VERROUILLÉ] |
| Empattement / voies | 3 050 mm / ~1 950 mm | [VERROUILLÉ] |
| Débattements | 480 mm AV / 530 mm AR, amortisseurs bypass | [VERROUILLÉ] |
| Pneumatiques | Paddles 33" AR, skis/rib AV | [VERROUILLÉ] |
| Répartition des masses | 43/57 AV/AR en charge, CG <= 530 mm | [VERROUILLÉ] |
| Châssis | Hybride : quille-batterie structurelle aluminium + cellule de sécurité acier CDS cotes FIA + exosquelette 4130 | [VERROUILLÉ] |
| Rigidité torsionnelle cible | >= 3 000 Nm/deg | [VERROUILLÉ] |
| Cas de charge dimensionnant | Réception à plat 2 m : 8 g de calcul, 12 g ultime | [VERROUILLÉ] |
| Architecture traction cible | 2 moteurs AR indépendants, vectorisation de couple | [VERROUILLÉ] (réalisation phasée, voir §7.2) |
| Chaîne de traction V1 | Scénario A (Tesla réemployé) vs B (twin EMRAX) — reco : A | [A DÉCIDER] |
| Batterie | ~45 kWh, ~350-400 V ; cellules selon scénario (voir §7.2) | [A DÉCIDER] |
| Thermique | Deux boucles liquides + chiller batterie 4 kW, ambiance 45 °C, poussière fine | [VERROUILLÉ] |
| Langage esthétique | « Organic Exo » + signature lumineuse nocturne (§3) | [VERROUILLÉ] |
| Interface | Pacenotes audio + bandeau LED + HUD léger + haptique volant ; data station copilote amovible | [VERROUILLÉ] |
| Compétition | Hors championnat ; **convertible FIA en < 6 mois**, aller-retour jour d'événement < 1 journée | [VERROUILLÉ] |
| Lieu de développement | Sablière privée région bordelaise (convention à trouver) | [EN ÉTUDE] |
| Expéditions dunes | Tunisie via Sousse (Douz / Ksar Ghilane), base familiale | [EN ÉTUDE] |
| Drone photogrammétrique | Budgété (~900 EUR, classe DJI Mini 4 Pro) | [VERROUILLÉ] |

## Décisions actées cette itération (retours propriétaire)

1. **Budget 30 000 EUR** : acté. Conséquence majeure : la chaîne twin-EMRAX neuve (~18 k EUR à elle seule) sort du périmètre V1 ; arbitrage A/B au §7.2, budget ventilé honnête au §10.
2. **Pratique de nuit** : nouvelle exigence — éclairage signature (§3.5), interface en mode nuit (§5), créneau thermique favorable (§9.5).
3. **Interface** : bandeau LED validé ; HUD validé tant qu'il ne pénalise pas (poids/complexité/attention) ; retour haptique validé ; le « côté data » est déporté vers une **data station copilote** amovible (§5.2) — le cockpit pilote reste zéro écran.
4. **FIA** : « FIA-ready » confirmé avec une règle nouvelle — la conversion compétition doit se faire en **moins d'une journée** de préparation (§6.5), et le véhicule reste convertible en < 6 mois vers un engagement sérieux.
5. **Lieux et logistique** : Bordeaux = base ; le Pilat est **exclu d'office** (interdit — voir §9.1, point réglementaire important) ; développement en sablière privée, expéditions Tunisie (§9).
6. **Études nouvelles demandées** : trajectoires historiques et prospective (§4.3), biomimétisme évalué en profondeur (§8), « un moteur, ça s'améliore ? » (§7.4), pertinence des aimants (§7.5), outillage MCP (§11.3).

# Synthèse de l'architecture (acquis des itérations 1-2)

Cette section condense les fondations pour que le document soit autoportant.

## Structure

Le cas dimensionnant est la réception à plat après un saut de 2 m : vitesse d'impact v = (2gh)^{1/2} soit ~6,3 m/s, ~22,6 kJ à absorber. Avec ~0,48 m de course utile (débattement + pneu), la décélération moyenne vaut ~4,2 g ; avec l'amortissement progressif des bypass on retient **8 g de calcul, 12 g ultime**. En réception cabrée, chaque tour d'amortisseur arrière voit ~32 kN, dimensionné à **~47 kN (coefficient 1,5)**.

Principes verrouillés :

- **Triangulation totale** : un tube travaille en traction/compression ; il ne casse qu'en flexion. Tout point d'ancrage atterrit à moins de ~25 mm d'un nœud triangulé ; aucun quadrilatère non contreventé dans un chemin d'effort.
- **Deux niveaux de structure** : cellule de sécurité en acier carbone CDS aux cotes FIA (arceau principal 50 × 2,0 mm — voir §6.2) + exosquelette 4130 (primaires 44,5 × 2,4, diagonales 38,1 × 1,6, reprises 44,5 × 3,0).
- **Quille-batterie structurelle** (6061/7075 boulonné-collé) entre et derrière les sièges : plancher, lest et caisson de torsion, ~1/3 de la rigidité châssis.
- **8 grappes de nœuds principales**, les plus chargées en pièces génératives imprimées (validation polymère d'abord, §4.2).

## Masses et motricité

Cible **43/57 AV/AR en charge, CG <= 530 mm**. Poussée maximale en propulsion : a/g = µ · f_{R} / (1 - µ · h/L) : avec µ paddle 0,7-0,9, **0,45-0,6 g d'accélération soutenue dans le sable** — limitée par la motricité, pas par la puissance. Le seuil de cabrage (~2,5 g) est inatteignable. Le vrai levier de performance est un **contrôle de traction à consigne de glissement sable** (les paddles poussent au maximum à 20-35 % de glissement). En vol : ~16°/s d'autorité à piquer par freinage des masses tournantes, autorité à cabrer par impulsion de couple ; régénération coupée en aérien sauf commande d'assiette.

## Thermique (45 °C, poussière fine)

**~12 kW continus** à évacuer (moteurs + onduleurs + pertes batterie). Boucle A (traction, 65 °C max) : 0,30-0,35 m² de radiateur + ventilateurs haute pression sur le pont AR. Boucle B (batterie, 25-40 °C) : **chiller frigorifique 4 kW obligatoire** (on ne radie pas sous l'ambiante), plaques froides, delta cellule < 4 K, **pré-refroidissement à 22-25 °C avant session** (~20 min de marge à fond). Durcissement : ailettes 8-10 FPI + pré-grilles, prises d'air hautes, IP67/IP69K, moteurs fermés, sabots UHMW.

# Design lock : le langage « Organic Exo »

**[VERROUILLÉ]** — L'ingénierie *est* le design : rien n'est caché, tout ce qui se voit travaille.

## Vocabulaire formel

- **Épine dorsale continue** de l'arceau à la queue — la signature de profil.
- **Nœuds génératifs exposés**, pièces d'orfèvrerie apparentes.
- **Ligne de tension latérale** unique, tendue façon Ferrari.
- **Quatre bypass dressés en tuyaux d'orgue** sur le pont arrière.
- **Visserie usinée apparente**, alignée, calibrée.

## Matières et finitions

| Zone | Matière / finition |
| Tubes exosquelette | Titane torché (irisations) ou 4130 verni satin selon coût |
| Quille batterie | Carbone mat / aluminium usiné brut |
| Nœuds génératifs | Ti / Scalmalloy brut, interfaces usinées brillantes |
| Accents | Cuivre bruni (échangeurs, durites gainées inox) |

## Interdits (garde-fous esthétiques)

- Aucune carrosserie enveloppante, aucun capot plein.
- **Aucun écran côté pilote** (amendé : data station copilote amovible autorisée, §5.2).
- Pas de plastiques peints, pas de faux carbone.

## Conséquences d'ingénierie

Nœuds = surfaces de classe A. Câblage HT dans les tubes ou la quille. Radiateurs assumés comme éléments graphiques.

## Signature lumineuse nocturne [VERROUILLÉ - nouveau]

La pratique de nuit devient une exigence — et une opportunité de design : de nuit, le véhicule EST sa lumière.

- **Ligne LED continue le long de l'épine dorsale** (feux de position/signature) : l'épine se dessine dans le noir — c'est l'équivalent nocturne de la silhouette Organic Exo.
- **Barre LED avant haute** sur l'arceau : combinaison portée (2 spots longue portée) + nappe large pour le relief proche ; montée haute pour limiter les ombres rasantes trompeuses dans les creux.
- **Feux arrière signature** + éclairage de travail AR commutable (récupération, manœuvres au bivouac).
- **Éclairage cockpit rouge à intensité asservie** (préserve la vision nocturne, tradition aéronautique).
- Budget électrique éclairage : ~250 W — négligeable pour le pack (< 1 % par heure).

# Innovations transversales : acquis, trajectoires, prospective

## État des dix concepts (synthèse et arbitrages rendus)

| N° | Concept | Statut |
| 1 | Contrôle d'assiette prédictif (AC75) | [EN ÉTUDE] file P1-bis |
| 2 | Télémétrie suspension par histogrammes (VTT DH) | **[VERROUILLÉ]** trio prioritaire |
| 3 | Blackbox + méthode tuning FPV | [EN ÉTUDE] file P1-bis (couplé VCU) |
| 4 | Nœuds génératifs polymère d'abord (aérospatial) | **[VERROUILLÉ]** trio prioritaire |
| 5 | Siège jamming granulaire (robotique molle) | [EN ÉTUDE] backlog |
| 6 | Banc à tambour pales de paddle (biomimétisme) | [EN ÉTUDE] file P1-bis, voir §8 |
| 7 | Gréement textile Dyneema | [EN ÉTUDE] backlog |
| 8 | Glissement vrai RTK-GNSS + EKF (FS Driverless) | **[VERROUILLÉ]** trio prioritaire |
| 9 | Immersion diélectrique module batterie | [EN ÉTUDE] backlog (si plaques froides insuffisantes) |
| 10 | Monitoring physiologique pilote | **[VERROUILLÉ]** (validé, protocole aux premiers essais) |

Le trio prioritaire (n° 2, 4, 8 — ~1 150 EUR de bancs) dé-risque le réglage châssis, les pièces structurelles les plus chères et la fonction de performance n°1 (traction sable). Les protocoles détaillés sont dans le référentiel v0.2 (historique Git) ; ils seront réinjectés ici au lancement de chaque banc.

## Protocoles actifs du trio prioritaire

- **n°2 — Télémétrie histogrammes** : 4 potentiomètres linéaires 200 mm + ESP32 + SD à 1 kHz ; les histogrammes de vitesse de tige disent objectivement où manquent compression/détente. Utilisable du VTT de validation jusqu'au véhicule final.
- **n°4 — Nœuds polymère d'abord** : impression FDM/SLS des 3 nœuds les plus chargés (échelle 1:2 puis 1:1), essais à rupture sur presse + capteur de force, corrélation FEA, puis seulement métal. La confiance s'achète à 15 EUR la pièce au lieu de 1 500.
- **n°8 — RTK + EKF** : base + rover u-blox ZED-F9P (~450 EUR), vitesse sol vraie au cm/s fusionnée IMU -> glissement réel pour le TC sable. Réutilisé tel quel par le système AR (§5) et la logistique de scan (§9).

## Trajectoires : d'où viennent ces technologies, où elles vont [nouveau]

Demande propriétaire : regarder l'histoire et se placer dans le futur. Lecture par domaine — chaque ligne se lit « passé -> présent -> horizon 2030 -> notre placement ».

| Domaine | Hier | Aujourd'hui | Horizon 2030 | Notre placement |
| Suspension | Essieux rigides, ressorts à lames ; bypass nés en Baja années 90 | Semi-actif électronique haut de gamme (rallye-raid usine) | Prédictif : la suspension lit le terrain devant (vision/mesh) avant l'impact | Notre feedforward ToF (n°1) est exactement cette trajectoire, en version accessible |
| Batteries | Plomb ; NiMH ; 18650 (Tesla 2008) | 21700/4680, 250-300 Wh/kg, prix -8 %/an | Semi-solide puis solide, 350-450 Wh/kg en volume vers 2028-2030 | Quille **repackable par conception** : on changera de chimie sans toucher au châssis |
| Moteurs | Courant continu à balais ; induction (années 90) | PMSM radial partout, flux axial en pointe | Flux axial banalisé ; montée du sans-terres-rares (réluctance assistée) | Berceau moteur **agnostique** : mono aujourd'hui, twin demain, autre techno après-demain |
| Matériaux | Acier doux ; CrMo ; carbone hors de prix | Impression métal en série restreinte, coût -15-20 %/an | Nœuds topologiques imprimés = pratique standard des petites séries | Méthode polymère-d'abord (n°4) : on est prêts à imprimer métal quand le prix tombe |
| Contrôle | Mécanique pur ; premières ECU | Vectorisation de couple, véhicule défini par logiciel | La valeur migre vers le firmware et les données ; l'openinverter des drives Tesla est déjà là | VCU **open et versionnée** : chaque session enrichit un actif logiciel qui prend de la valeur |
| Interface | Jauges ; puis écrans partout (2010s) | Reflux vers le minimal : HUD, voix, haptique | AR légère mature (waveguides), assistants vocaux embarqués | Pari audio-d'abord déjà aligné ; le HUD s'achètera mûr au lieu de se développer fragile |

**Position stratégique du projet** : les tubes durent vingt ans ; tout le reste s'upgrade. ORGANIC EXO est conçu comme une **plateforme** — châssis intemporel, énergie interchangeable, intelligence logicielle croissante. C'est ainsi qu'un projet personnel à 30 k EUR reste pertinent face à des machines d'usine : pas en gagnant la course aux specs, mais en étant upgradable là où elles sont figées.

# Interface pilote-machine et système AR topographique

**Contrainte : zéro écran côté pilote.** Le système restitue une information minimale au bon moment, ou se tait. Architecture 4 couches inchangée (drone -> mesh WebODM -> ligne de course -> restitution) ; cette itération acte les paliers et ajoute le mode nuit et le poste copilote.

## Paliers de restitution — tous validés [VERROUILLÉ]

- **Palier A — Pacenotes audio synthétiques** (MVP) : notes générées du mesh + ligne, déclenchées par position RTK, voix dans le casque. Coût ~0, latence nulle, insensible à la poussière.
- **Palier B — Bandeau LED périphérique** : ruban discret dans le halo (écart à la ligne, alertes compression/lèvre). ESP32, ~60 EUR. **Mode nuit** : intensité asservie à la luminosité ambiante, palette décalée vers le rouge — le bandeau ne doit jamais éblouir ni tuer la vision nocturne.
- **Palier C — HUD léger** : lunettes waveguide grand public pilotables BLE (classe Even Realities G1 / Vuzix Z100), symbologie fixe minimale : 3 chevrons de ligne + delta vitesse + 2 alertes. Conditions posées par le propriétaire respectées : ~40 g, zéro câble, le pilote peut les enlever sans rien perdre de vital (l'audio reste maître). Bonus nuit : la lisibilité optique est *meilleure* de nuit qu'en plein soleil — le HUD prend tout son sens en session nocturne.
- **Palier D — Retour haptique volant** : vibreurs dans le moyeu (alerte lèvre/ligne quand l'audio sature). ESP32 + ERM, ~40 EUR.

## Data station copilote [VERROUILLÉ - nouveau]

Le goût du propriétaire pour le « futuriste data » trouve sa place **à droite** : le copilote est le poste data du véhicule.

- **Tablette durcie amovible** (fixation à came côté copilote, invisible du pilote, retirée = cockpit pur — le design lock est respecté).
- Flux : carte mesh temps réel avec position RTK, télémétrie live (températures, glissements, budget batterie), état des systèmes, replay des segments.
- Le copilote **pilote les pacenotes** : il peut enrichir/corriger les notes à la volée (bouton « marquer ce point »), passer en mode dictée manuelle sur section inconnue — exactement le rôle du copilote de rallye, augmenté.
- En solo : la tablette reste au camp, le système tourne en autonome sur les notes générées.

## Mode nuit du système [nouveau]

- Le scan drone se fait **de jour** (meilleure photogrammétrie) ; la session de nuit exploite le mesh du jour — le RTK ne voit pas la nuit, donc rien ne change pour le guidage. C'est même le cas d'usage où le système AR a le plus de valeur : le terrain que les yeux ne lisent plus, le mesh le connaît.
- Pacenotes enrichies de nuit : annonces plus précoces (vitesse de lecture du terrain réduite), vocabulaire dédié (« crête invisible », « creux noir »).
- Exigence sécurité : périmètre convenu, balise lumineuse véhicule (l'épine LED, §3.5), point GPS de ralliement, jamais seul en session nocturne dunes.

# Conformité FIA et usage hors compétition

## Positionnement : « FIA-ready, pas FIA-bound » [VERROUILLÉ]

Catégories cross-country pertinentes : **T3** (prototypes légers, Annexe J art. 286) et T4 (SSV série, art. 286A). Pas de classe 100 % électrique ouverte en championnat à ce jour ; les programmes électriques/H2 courent en catégories expérimentales (Dakar Future). T3 interdit les aides au pilotage : notre TC est central au concept -> **mode « TC off » câblé physiquement** dès la VCU. Stratégie confirmée par le propriétaire : véhicule personnel d'abord, mais **aucune reconstruction** si l'envie de s'engager vient — d'où les deux règles de conception ci-dessous (§6.5).

## Cellule de sécurité : invariants figés dès la CAO (art. 283)

- Arceau principal **50 × 2,0 mm ou 45 × 2,5 mm**, acier carbone non allié étiré à froid sans soudure (>= 350 N/mm²) ; autres éléments 38 × 2,5 ou 40 × 2,0. Le chromoly reste cantonné à l'exosquelette non-sécurité.
- Pieds d'arceau sur platines + goussets réglementaires, dégagement casque, ancrages harnais 6 points (norme 8853-2016) sur nœuds, sièges norme 8862 aux points prescrits.
- Extincteur plombé + déclencheurs int/ext, coupe-circuit intérieur double + extérieur signalé, anneaux de remorquage, évacuation < 7 s.

## Sécurité haute tension (esprit FIA + socle ECE R100)

Caisson batterie anti-intrusion (zone d'écrasement >= 50 mm, tenue 20 g longitudinal), ségrégation HT hors zones de déformation, gaine orange aux traversées, HVIL sur toute la boucle, IMD permanent, sectionneur sans outil, voyant d'état visible des secours, équipotentialité < 0,1 ohm, IP67/IP69K, fiche d'intervention secours rédigée dès la V1.

## Usage route : tranché

RTI irréaliste, L7e-B2 incompatible par construction (15 kW / 450 kg / 90 km/h) — **[REJETÉ]** définitif. Cadre d'usage : terrains fermés + remorque (logistique complète au §9).

## Conversion compétition : < 1 journée [VERROUILLÉ - nouveau]

Règle de conception issue du retour propriétaire (« pas un mois de démontage pour une journée d'événement ») : tout écart entre configuration plaisir et configuration contrôle technique doit se résorber en **une journée d'atelier maximum, outillage à main**. Concrètement :

- **Conforme en permanence** (aucun démontage) : cellule de sécurité, ancrages, extincteur, coupe-circuits, HT, sièges/harnais — la sécurité n'a pas de « mode ».
- **Basculable jour J** : TC/vectorisation -> interrupteur « TC off » scellable ; data station copilote -> retirée ; HUD -> retiré ; éclairage additionnel non réglementaire -> déposable par connecteurs rapides (4 fixations à came par élément).
- **Dossier prêt en permanence** : certificats matière, qualification soudeur, CAO de la cage, fiche secours — un classeur à jour, pas une chasse aux documents.
- Révision périodique : à chaque évolution du véhicule, la question « est-ce que ça casse la journée de conversion ? » est posée dans ce document avant réalisation.

L'engagement « convertible en < 6 mois » vers un programme sérieux (si envie durable) est couvert par la même logique : rien dans l'architecture ne nécessite de re-châssis.

# Énergie et motorisation

## Acquis (v0.2, inchangés)

Sources d'énergie : NMC 21700 retenu pour la traction ; LFP retenu pour le tampon statique de recharge ; H2, prolongateur thermique, LTO, Na-ion (traction), supercondensateurs et moteurs-roue **[REJETÉS]** avec motifs conservés en historique. Récupération au freinage confirmée. Panorama des technologies moteurs : flux axial = référence performance (96-98 % pic), radial PMSM = plan B éprouvé, induction/réluctance = écartés ou en veille.

## Chaîne de traction V1 : l'arbitrage budget [A DÉCIDER - reco : A]

Le budget de 30 k EUR rend le twin-EMRAX neuf (~18 k EUR moteurs + onduleurs) incompatible avec une V1 complète. Deux scénarios honnêtes :

| Critère | **Scénario A — Tesla réemployé (reco)** | Scénario B — Twin EMRAX (concept d'origine) |
| Moteur(s) | 1 × Rear Drive Unit Model 3 d'occasion (~200 kW crête, ~500 Nm roue via son réducteur intégré, diff inclus) | 2 × EMRAX 268 LC + 2 onduleurs SiC + 2 réducteurs |
| Contrôle | Contrôleur aftermarket (EV Controls T2-C, Ingenext) ou openinverter — écosystème mûr et documenté | Contrôle natif complet, vectorisation vraie |
| Coût chaîne complète | ~5 500-7 000 EUR | ~18 000-20 000 EUR |
| Vectorisation de couple | Non (diff mécanique) — TC global conservé, correction lacet par freinage différentiel léger (méthode SSV/AMG) | Oui, gauche/droite indépendante |
| Masse chaîne | ~90 kg (unité complète) | ~75 kg (2 moteurs + réducteurs) |
| Contrôle d'assiette en vol | Conservé (couple et frein globaux) | Conservé, plus fin |
| Perfs sable estimées | ~85-90 % du concept (la motricité sature avant la puissance : 200 kW suffisent largement à 1 150 kg) | 100 % du concept |
| Évolutivité | Le berceau AR est dessiné **dès la V1** pour recevoir le twin : upgrade A -> B sans toucher au châssis | — |

**Recommandation motivée** : scénario A. Dans le sable, on est limités par la motricité (0,45-0,6 g) bien avant les 200 kW du RDU ; la vectorisation apporte du raffinement, pas la performance de base. A permet de rouler dans le budget, d'apprendre avec la télémétrie, et de financer B plus tard par étalement — le châssis n'aura pas à changer. C'est le « monstre pragmatique » : monstrueux au bon endroit (rapport poids/puissance ~5,7 kg/kW, meilleur qu'un SSV turbo usine), upgradable partout ailleurs.

Batterie associée (scénario A) : pack DIY ~96s en cellules 21700 courantes (classe Samsung 50S : ~19,4 Wh/cellule, ~25 A continu) — ~45-50 kWh pour ~8-9 k EUR avec BMS et boîtier, ~240 kg. Les P45B (double du prix) restent l'option B ou un repack futur : la quille s'en moque, elle est dessinée pour ça.

## Recharge terrain

Chargeur embarqué 6,6 kW (prise industrielle 32 A : campings, fermes, ateliers) = ~7 h pour un plein — la nuit y pourvoit. Remorque énergie solaire + tampon LFP : reportée en V2 (budget), location de génératrice sur site d'expédition en attendant. Détail logistique par site au §9.

## « Un moteur, ça s'améliore ? » [nouveau - pédagogie]

Question du propriétaire. Réponse courte : **oui, mais pas là où on croit.**

Comment ça marche, en cinq lignes : un moteur électrique, c'est un jeu d'électroaimants (le stator) qui créent un champ magnétique tournant, et des aimants permanents (le rotor) qui courent après ce champ. L'onduleur est le chef d'orchestre : il décide, 20 000 fois par seconde, combien de courant envoyer dans quelle bobine. Le couple, c'est du courant bien placé ; la vitesse, c'est la fréquence du champ.

Où va l'énergie perdue : pertes cuivre (le courant chauffe les bobines — dominantes à fort couple), pertes fer (aimanter/désaimanter la tôle — dominantes à haute vitesse), pertes mécaniques (roulements, brassage d'huile), pertes onduleur (commutations). Total : 3-8 % selon le point de fonctionnement. Un moteur moderne est déjà à 96-97 % au meilleur point : **il ne reste presque rien à gagner en rendement crête** — les industriels dépensent des millions pour un demi-point.

Les quatre leviers réels, classés par retour sur investissement pour nous :

1. **Le logiciel de contrôle (gratuit, gain majeur)** : stratégie de couple (MTPA — « le plus de couple par ampère »), défluxage propre à haute vitesse, rampes, et surtout notre TC à glissement : sur le sable, un contrôle intelligent fait gagner 10-20 % d'« efficacité de mission » (distance/kWh, temps au tour) là où le rendement moteur ne bouge que d'un point. C'est NOTRE terrain de jeu, et il s'améliore à chaque session par les logs.
2. **Le refroidissement (le vrai tuning matériel)** : un moteur ne s'use pas en puissance, il s'étouffe en chaleur. Améliorer le circuit (débit, plaques, huile de réducteur) ne change pas le rendement mais **la durée pendant laquelle la crête est disponible** — fonctionnellement, c'est un moteur plus gros. Accessible à l'atelier, mesurable par télémétrie.
3. **La transmission** (1-3 % de pertes) : denture, qualité d'huile, alignements. Gains modestes, fiabilité surtout.
4. **Le hardware interne** (rebobinage, aimants, entrefer) : territoire industriel, outillage spécialisé, ROI quasi nul en amateur — on n'y touche pas, on choisit bien le moteur au départ.

Conclusion pour le projet : le « monstre d'efficacité » se construit dans le firmware et la thermique. Et c'est une excellente nouvelle : ce sont les deux domaines où un propriétaire investi + une IA font mieux qu'un catalogue.

## Les aimants dans le projet : réponse à la curiosité [nouveau]

- **Sustentation magnétique (maglev)** : non — physiquement inapplicable. La lévitation demande soit un rail actif (train), soit une surface conductrice défilante, et des puissances énormes ; le sable n'offre ni l'un ni l'autre, et un véhicule sustenté n'aurait aucune réaction latérale pour tourner. Verdict : [REJETÉ], mais la question était légitime — c'est exactement le genre d'idée qu'il faut oser poser puis chiffrer.
- **Amortisseurs magnétorhéologiques** (fluide qui durcit dans un champ magnétique, réponse ~1 ms — Ferrari/GM « MagneRide ») : sérieux, mais inexistants en course 500 mm, fluide cher et sensible à la température. [EN ÉTUDE] lointaine ; nos bypass à solénoïdes font le travail.
- **Amortissement par courants de Foucault** (aimant + conducteur, freinage sans contact ni usure) : force trop faible aux basses vitesses de tige. Anecdotique ici.
- **Là où les aimants servent vraiment, dès la V1** : capteurs à effet Hall (pédale, direction, vitesses roue — fiables dans la poussière car sans contact), **accouplements magnétiques des pompes** de refroidissement (zéro joint tournant = zéro fuite, et la pompe décroche au lieu de casser si elle bloque), fixations rapides magnétiques + goupille mécanique pour les panneaux déposables (conversion FIA < 1 jour, §6.5). Et rappel plaisant : nos moteurs *sont* déjà la plus belle application d'aimants du véhicule — les flux axiaux utilisent des arrangements type Halbach pour concentrer le champ où il travaille.

# Biomimétisme : le bestiaire du désert, évalué [nouveau]

Demande propriétaire : regarder ce que font les animaux et la nature, et évaluer la pertinence. Méthode d'évaluation — le biomimétisme fonctionne quand **le problème physique est analogue** (milieu granulaire, chaleur, structure légère), pas quand on copie une forme parce qu'elle est belle. Chaque entrée est notée : Haute / Moyenne / Anecdotique.

## Tableau d'évaluation

| Source naturelle | Principe | Transfert projet | Pertinence |
| Fennec (oreilles) | Radiateurs à grand rapport surface/volume, placés dans le flux | Échangeurs fins à grande surface montés hauts dans l'air propre — valide notre choix pont AR | **Haute** (déjà alignée) |
| Fourmi argentée du Sahara | Poils triangulaires réfléchissant l'infrarouge : elle sort à midi quand tout meurt | Revêtements céramiques réfléchissants IR sur caisson batterie et surfaces exposées : -5 à -10 °C de charge solaire passive | **Haute** — essai peinture IR sur le caisson, ~80 EUR |
| Termitière | Ventilation passive par tirage thermique (cheminées) | Carénage d'extraction au-dessus des radiateurs : l'air chaud aspire l'air frais sans ventilateur à l'arrêt — refroidissement bivouac gratuit | **Haute** — dessin du carénage AR en ce sens |
| Chameau | Inertie thermique + hyperthermie contrôlée : il « stocke du frais » la nuit et laisse monter sa température le jour dans une fenêtre maîtrisée | C'est exactement notre pré-refroidissement pack (§2.3) : le chiller « bosse thermique » avant session — analogie qui valide la stratégie et donne le vocabulaire | **Haute** (conceptuelle) |
| Sidewinder + scinque des sables | Locomotion en milieu granulaire : angle d'attaque optimal, surfaces basse friction | Géométrie des pales de paddle (banc n°6) + revêtements anti-abrasion | **Haute** (banc déjà défini) |
| Kangourou / autruche | Tendons = ressorts stockant l'énergie de chaque foulée (course quasi gratuite) | Lecture énergétique de la suspension : la détente des bypass restitue au lieu de dissiper — piste : lames composites d'appoint stockantes | **Moyenne** — étude après télémétrie n°2 |
| Arbres (méthode Mattheck) | Croissance à contrainte constante : jamais de concentration de contrainte | Règle de dessin des goussets et congés (rayons « racinaires ») — déjà l'esprit des nœuds génératifs, formalisé | **Moyenne** (règle CAO adoptée) |
| Scarabée de Namibie | Collecte d'eau du brouillard par surfaces alternées | Récupération d'eau au bivouac côtier — hors périmètre véhicule | Anecdotique |
| Gecko | Adhésion sèche par forces de van der Waals | Inopérant sur sable (poussière neutralise) | Anecdotique |
| Ailes de rapace | Surfaces portantes adaptatives | Aéro négligeable à nos vitesses hors appui — rien à chercher | Anecdotique |

## Ce qu'on en retire concrètement

Trois actions entrent au backlog : **peinture réfléchissante IR du caisson** (essai comparatif thermocouples, ~80 EUR), **carénage-cheminée d'extraction** au-dessus des radiateurs AR (dessiné avec la boucle A), **règle Mattheck** dans le cahier de dessin des nœuds. La leçon de fond : le désert a déjà résolu nos deux problèmes majeurs — la chaleur et le sable — et la sélection naturelle a éliminé les mauvaises réponses depuis des millions d'années. Chaque nouveau sous-système passera par la question : « qui, dans le vivant, a déjà ce problème ? »

# Logistique terrain

Base : **Bordeaux**. Attaches familiales : **Sousse (Tunisie)** et **Urumqi (Chine)**. Véhicule non homologué route -> tout déplacement se fait sur remorque (§6.4).

## Le point réglementaire qui change le plan : le Pilat est exclu

La dune du Pilat est un site classé (Grand Site de France) : circulation et stationnement de véhicules à moteur interdits, sans exception pour les loisirs. Plus largement, l'article **L.362-1 du code de l'environnement** (loi « Lalonde », 1991) interdit la circulation des véhicules à moteur **hors voies ouvertes à la circulation publique** sur tout le territoire : plages, dunes littorales, forêts domaniales — aucune dune naturelle française n'est légalement praticable. Amendes lourdes, confiscation possible, et un impact désastreux pour l'image du projet. **Le Pilat ne sera jamais notre terrain de jeu — et c'est non négociable.** [VERROUILLÉ]

## La solution développement : sablières privées [EN ÉTUDE - priorité]

Sur terrain **privé**, avec l'accord écrit du propriétaire/exploitant, la pratique est légale (hors espaces protégés). La région bordelaise est riche en **sablières et carrières de sable** (bassin d'Arcachon-Landes : exploitation du sable des Landes) :

- Cible : une sablière en fin d'exploitation ou zone morte d'exploitation, convention d'occupation précaire + assurance RC circuit (via licence UFOLEP/FFSA ou assurance dédiée).
- Arguments pour l'exploitant : véhicule électrique **silencieux** (pas de nuisance voisinage — atout décisif vs moto-cross), zéro hydrocarbure sur site, créneaux hors activité, indemnité d'occupation.
- Rayon de recherche : < 1 h de Bordeaux. Le silence du véhicule ouvre aussi la porte à des créneaux nocturnes (§9.5) qu'aucun engin thermique ne peut négocier.
- Action : lettre type + liste des exploitants girondins à la prochaine itération si validé.

Terrains complémentaires : pistes 4x4/off-road privées (journées d'essais châssis, pas de dunes mais du relief), et événements sable organisés (dunes contrôlées, rare en France).

## Les expéditions dunes : Tunisie d'abord [EN ÉTUDE - reco forte]

| Critère | **Tunisie (via Sousse)** | Maroc (Merzouga) | Chine (Urumqi/Kumtag) |
| Accès dunes | Douz / Ksar Ghilane (Grand Erg Oriental), ~300 km de Sousse (~4 h) | Erg Chebbi, ~2 700 km de route via Espagne + ferry détroit | Kumtag (Shanshan) à ~400 km d'Urumqi |
| Trajet depuis Bordeaux | Route -> Marseille (650 km) puis **ferry Marseille-Tunis ~22 h** (CTN / Corsica Linea), véhicule tracteur + remorque embarqués | 2 jours de route + ferry Algésiras-Tanger | Vol ; le véhicule ne suit pas (voir ci-dessous) |
| Coût logistique estimé (AR) | Ferry véhicule + remorque + cabine : ~900-1 800 EUR selon saison (réserver 3-4 mois avant) + carburant/péages ~350 EUR | ~1 200-1 800 EUR (carburant, ferries, hôtels étapes) | Prohibitif pour le véhicule |
| Douane matériel | Admission temporaire du matériel sportif à déclarer à l'entrée ; **base familiale à Sousse = garant local, stockage, base arrière** — avantage décisif | Admission temporaire classique, éprouvée par les raids | Import temporaire d'un véhicule en Chine : quasi impossible (permis spéciaux, escorte) — **[REJETÉ] pour le véhicule** ; Kumtag se visite en SSV de location |
| Verdict | **Destination expédition n°1** : 1-2 sessions/an, 10-15 jours | Événements/raids ponctuels, phase ultérieure | Voyage familial + repérage, sans le véhicule |

Points d'attention Tunisie : période octobre-avril (été intenable, même pour le chiller), autorisation de circulation dans les zones désertiques auprès des autorités locales (les agences de Douz savent faire), recharge : réseau électrique correct à Douz (prise 32 A à organiser avec un hôtel/garage — le chargeur 6,6 kW fait le plein en une nuit), génératrice de location en secours pour Ksar Ghilane.

## Traction et remorque : le dossier pratique

- **Remorque** : porte-engin PTAC 1 500-1 600 kg (véhicule ~980 kg + arrimage), plateau basculant ou rampes, bâche intégrale (poussière routière, discrétion, arrimage du matériel). Occasion : ~2 500-3 500 EUR. Treuil électrique 12 V d'embarquement (~300 EUR) — le buggy monte tout seul, sans rouler sur route publique.
- **Permis** : remorque > 750 kg -> selon le PTAC du tracteur : ensemble <= 4 250 kg = **formation B96** (7 h, sans examen) ; au-delà = **permis BE**. Avec un tracteur PTAC 2 500 kg + remorque 1 600 kg = 4 100 kg -> B96 suffit. A vérifier selon le véhicule tracteur retenu. [A DÉCIDER : véhicule tracteur disponible ?]
- **Charge en déplacement** : prise industrielle 32 A (adaptateurs P17), campings et ateliers en route ; le pack voyage à 30-50 % de charge (stockage et sécurité).
- **Assurance** : RC terrain/circuit pour la pratique + assurance transport pour la remorque et son chargement.

## L'avantage nocturne [nouveau]

La pratique de nuit n'est pas qu'un plaisir — c'est un multiplicateur logistique : en sablière, des créneaux nocturnes silencieux (véhicule électrique) sont négociables là où le jour est réservé à l'exploitation ; au désert tunisien, la nuit d'octobre est à 15-20 °C — **le chiller respire, la crête devient disponible en continu** : les sessions performance se feront de nuit, au frais, sur le mesh scanné au couchant. Le véhicule électrique est nativement l'engin du désert nocturne : silence, lumière embarquée, thermique favorable.

# Budget : ventilation des 30 000 EUR

Scénario A (traction Tesla réemployée), chiffrage honnête, prix 2026 :

| Poste | Détail | Estimation |
| Chaîne de traction | RDU Model 3 occasion + contrôleur aftermarket + câblage moteur | 6 000 EUR |
| Batterie | Pack DIY ~45 kWh 21700 (classe 50S) + BMS + boîtier intégré quille | 9 000 EUR |
| Châssis | Tubes CDS (cellule) + 4130 (exosquelette) + quille alu + visserie + soudure | 4 000 EUR |
| Suspension | Bras (fabrication) + 4 bypass 2.5" occasion (King/Fox) + potentiomètres | 5 000 EUR |
| Roulant | Direction, freins double circuit, moyeux, jantes + paddles + skis | 3 000 EUR |
| Haute tension | Contacteurs, pyrofuse, IMD, chargeur 6,6 kW, DC-DC, connectique | 2 200 EUR |
| Thermique | Radiateurs, pompes (accouplement magnétique), chiller adapté, durites | 1 500 EUR |
| VCU & télémétrie | Teensy/ESP32, RTK base+rover, IMU, capteurs, blackbox | 1 200 EUR |
| Sécurité | Sièges (8862 compatibles), harnais 8853, extincteur, coupe-circuits | 2 000 EUR |
| Éclairage nuit | Barre LED, épine LED, cockpit rouge asservi | 500 EUR |
| Drone | Classe DJI Mini 4 Pro + batteries + GCP | 900 EUR |
| **Sous-total véhicule** | | **35 300 EUR** |

**Lecture franche : le véhicule seul dépasse de ~5 300 EUR l'enveloppe**, avant remorque (~2 800 EUR) et bancs low-cost (~1 200 EUR). Trois manières de tenir les 30 k EUR, cumulables :

1. **Étalement (reco)** : l'enveloppe 30 k EUR couvre P0-P3 (véhicule roulant en configuration essais : pack 30 kWh provisoire à 6 000 EUR au lieu de 9 000, bypass occasion négociés, sièges occasion) ; le pack définitif 45 kWh, la remorque grand format et les paliers interface C/D glissent en année 2 (~8-9 k EUR différés). Le calendrier P0-P4 (§11) est déjà phasé ainsi.
2. **Dégraissage ciblé** : bypass chinois rebuildés (-1 200), jantes acier (-400), drone reporté après le premier mesh sous-traité (-900). Douloureux mais réversible.
3. **Recettes** : revente de la capacité de scan (le combo drone + WebODM intéresse exploitants de carrières et domaines — précisément nos interlocuteurs sablière), contenu du build (la construction documentée d'un sandrail électrique Organic Exo est un objet médiatique rare). Non budgété, tout gain accélère.

Le scénario B (twin EMRAX + pack P45B) reste chiffré pour mémoire : +18-20 k EUR par rapport à A, activable plus tard sans re-châssis.

# Feuille de route, décisions, outillage

## Phases (mises à jour budget/logistique)

| Phase | Contenu | Budget cumulé | Sortie |
| P0 — Numérique (en cours) | Modèle dynamique 2-DOF sable, CAO cage paramétrique, FEA quille | ~0 EUR | Géométrie figée |
| P1 — Bancs | Trio n° 2, 4, 8 + démarches sablière | ~1 200 EUR | Données réelles + terrain sécurisé |
| P2 — Mule | Châssis simplifié, RDU Tesla, pack provisoire 30 kWh, TC v1 | ~18 k EUR | Validation traction + suspension |
| P3 — Véhicule | Cellule FIA + exosquelette + quille définitive + éclairage nuit | ~30 k EUR | ORGANIC EXO roulant |
| P4 — Année 2 | Pack 45 kWh, interface C/D, remorque expédition, première Tunisie | +10-12 k EUR | Programme complet |

## Décisions attendues [A DÉCIDER]

1. **Scénario A validé ?** (traction Tesla réemployée V1, twin EMRAX en upgrade) — reco : oui.
2. **Véhicule tracteur** : en possédez-vous un (PTAC ?) — détermine B96 vs BE et le choix remorque.
3. **Étalement budgétaire** (option 1 du §10) validé ? — sinon indiquer les coupes préférées.
4. **Démarche sablière** : je prépare lettre type + liste d'exploitants girondins à la prochaine itération ?
5. **Fenêtre Tunisie visée** (octobre-novembre 2027 réaliste après P3) — pour caler le rétroplanning.

## Outillage logiciel : connexions MCP recommandées [nouveau]

Réponse à la question posée. Par ordre d'utilité immédiate pour que je travaille directement dans vos outils :

1. **FreeCAD MCP** (serveur `neka-nat/freecad-mcp` ou équivalent) — la priorité : CAO paramétrique open source ; je modélise la cage FIA, la quille et les bras directement, cotes pilotées par tableur — la géométrie se régénère quand une cote change. Gratuit.
2. **Blender MCP** — pour le design : rendus du langage Organic Exo, études de la signature lumineuse nocturne, visuels du projet. Gratuit.
3. **KiCad MCP** (phase P2) — schémas électriques BT/HT, faisceau, VCU.
4. Déjà en place : **GitHub** (ce référentiel), génération de documents (ce PDF), recherche web (veille FIA/fournisseurs).
5. Non nécessaire : les suites FEA lourdes s'exécutent en local par scripts (CalculiX/PrePoMax) que je fournis — pas besoin de MCP dédié.

Installation côté Claude Desktop/Code : ajouter le serveur dans la configuration MCP ; je fournirai le pas-à-pas à la demande.

# Journal des révisions

| Version | Date | Contenu |
| v0.1 | Itération 1 (chat, Claude desktop) | Diagnostic initial : structure, masses/traction, thermique, deux directions de style |
| v0.2 | 17 juillet 2026 | Premier PDF de référence : design lock Organic Exo, 10 innovations, architecture AR, conformité FIA (cellule CDS art. 283), rejet des voies route, étude énergie/moteurs, feuille de route |
| v0.2.1 | 17 juillet 2026 | Révision de mise en page : l'intérieur adopte l'identité de la couverture |
| v0.3 | 17 juillet 2026 | Itération majeure sur retours propriétaire. Budget 30 k EUR acté -> arbitrage chaîne de traction A/B (reco : Tesla réemployé) + budget ventilé honnête ; exigence nuit (signature lumineuse, interface mode nuit, avantage thermique) ; paliers interface tous validés + data station copilote ; règle conversion FIA < 1 journée ; trajectoires historiques et prospective ; biomimétisme évalué (bestiaire noté) ; pédagogie « un moteur ça s'améliore » et aimants ; logistique complète Bordeaux/sablières/Tunisie (Pilat exclu — L.362-1) ; outillage MCP. Minci : détail des 10 innovations replié sur le trio actif |

# Références

- FIA — Annexe J, textes officiels : www.fia.com/regulation/category/100
- Règlement (UE) n° 168/2013 (catégories L) : eur-lex.europa.eu (CELEX 32013R0168)
- Code de l'environnement art. L.362-1 (circulation motorisée en espaces naturels) : legifrance.gouv.fr
- Ferries Marseille-Tunis (CTN / Corsica Linea) : corsicalinea.com, directferries.fr
- Écosystème Tesla drive units réemployées : openinverter.org, evwest.com, westside-ev.com, ingenext.ca
- Serveurs MCP CAO : github.com/neka-nat/freecad-mcp (FreeCAD), Blender MCP
- Données constructeurs (EMRAX, Molicel, Samsung SDI, u-blox, WebODM) : fiches techniques publiques — à re-confirmer au devis.
