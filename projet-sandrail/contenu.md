---
titre: ORGANIC EXO
sous-titre: Sandrail électrique biplace haute performance
version: v0.5
date: 17 juillet 2026
statut: UAE seul horizon extérieur - sous-jalons à rythme libre - guides MCP en annexes
---

# Mode d'emploi du document

Ce document est le **référentiel vivant** du projet. Il remplace les réponses en chat : chaque itération le fait grandir (nouvelles études) et mincir (synthèse des points tranchés). La source (`contenu.md`) est versionnée sous Git ; le PDF est régénéré à chaque révision.

Chaque élément de décision porte un marqueur d'état :

- **[VERROUILLÉ]** : décision actée, ne sera rouverte que sur fait nouveau majeur.
- **[EN ÉTUDE]** : piste active, protocole d'essai ou d'analyse défini.
- **[REJETÉ]** : écarté, avec motif conservé pour mémoire.
- **[A DÉCIDER]** : arbitrage attendu du propriétaire du projet (voir §11).

> Convention : unités SI, virgule décimale française. Les chiffres restent des ordres de grandeur d'avant-projet, à valider par calcul détaillé et essais. Document écrit pour un propriétaire investi mais non-ingénieur : chaque concept est expliqué au moment où il sert.

# Fiche projet et décisions verrouillées

## Cahier des charges figé

| Paramètre | Valeur | État |
| Configuration | Sandrail biplace (le second siège : un ami à former, un jour), exosquelette apparent | [VERROUILLÉ] |
| Budget | Trajectoire ~78-83 k EUR en **sous-jalons déclenchés par l'épargne** (rythme libre, §10), plafond 100 k | [VERROUILLÉ] |
| Masse en ordre de marche (GVW) | 1 150 kg (à vide ~980 kg + 2 occupants) | [VERROUILLÉ] |
| Usage | Terrain fermé, jour **et nuit** (balisage lumineux §9.5), plaisir d'abord | [VERROUILLÉ] |
| Empattement / voies | 3 050 mm / ~1 950 mm | [VERROUILLÉ] |
| Débattements | 480 mm AV / 530 mm AR, amortisseurs bypass | [VERROUILLÉ] |
| Pneumatiques | Paddles 33" AR, skis/rib AV + **gestion de pression embarquée** (§4.4) | [VERROUILLÉ] |
| Répartition des masses | 43/57 AV/AR en charge, CG <= 530 mm | [VERROUILLÉ] |
| Châssis | Quille-batterie structurelle alu + cellule de sécurité acier CDS cotes FIA + exosquelette 4130 | [VERROUILLÉ] |
| Rigidité torsionnelle cible | >= 3 000 Nm/deg | [VERROUILLÉ] |
| Cas de charge dimensionnant | Réception à plat 2 m : 8 g de calcul, 12 g ultime | [VERROUILLÉ] |
| Traction | **2 × EMRAX 268 LC + onduleurs SiC** (véhicule final) ; mule an 1 = mono-EMRAX ; « le meilleur moteur, pas le moins cher » | [VERROUILLÉ] |
| Batterie | **Molicel P45B 21700, pack modulaire en tranches** : ~16 kWh (mule) -> ~45 kWh (final), la quille grandit avec les apports | [VERROUILLÉ] |
| Thermique | Deux boucles + chiller 4 kW, ambiance 45 °C, poussière fine | [VERROUILLÉ] |
| Esthétique | « Organic Exo » + signature lumineuse nocturne | [VERROUILLÉ] |
| Interface | Pacenotes + LED + HUD léger + haptique + data station copilote + **musique dockable** (§5.4) | [VERROUILLÉ] |
| Compétition | Hors championnat ; convertible **< 12 mois** vers un engagement sérieux ; conversion jour J < 1 journée | [VERROUILLÉ] |
| Innovations | **Liste close** (§4.4) : rien n'entre sans gain mesurable (vitesse, autonomie, sécurité) | [VERROUILLÉ] |
| Lieu de développement | Sablière privée Gironde + **stockage sur site** (pas de véhicule tracteur : §9.4) | [EN ÉTUDE - contacts §9.2] |
| Expéditions | **UAE uniquement** (conteneur, CPD, hiver) ; Maghreb rejeté ; piste « Gobi » = construction locale, étude lointaine (§9.3) | [VERROUILLÉ] |
| Permis | **B d'abord** (délai critique, à lancer maintenant) puis B96 (7 h) — sous-jalon S0 (§9.4) | [VERROUILLÉ] |
| Infrastructure numérique | Serveur Vultr (Corée) = camp de base télémétrie/meshes/CI (§11.4) | [VERROUILLÉ] |

## Décisions actées cette itération (retours propriétaire)

1. **Expéditions tranchées** : non à la Chine (import véhicule) et **non au Maghreb** (Maroc, Tunisie et assimilés) — **full UAE en conteneur**, « le plus élégant et le moins risqué » (§9.3). L'idée du propriétaire pour la Chine est retournée dans le bon sens : ne pas amener le buggy, mais **en construire un sur place** un jour — la piste « Gobi » (beau-oncle à la sécurité d'un centre de loisirs du désert) est consignée comme étude lointaine.
2. **Sous-jalons ralentis** : 37 k sur un an était trop gros — le budget passe en **sous-jalons S0-S9 déclenchés par l'épargne**, sans calendrier imposé (§10). Chaque sous-jalon est utile seul et n'engage pas le suivant.
3. **Permis** : le propriétaire n'a pas encore le permis B — parcours acté : **B immédiatement** (délai critique du projet), puis B96 (§9.4).
4. **Sablière** : démarche confirmée — la **lettre type est prête en Annexe B**, envoi sur feu vert après personnalisation.
5. **MCP** : guide d'intégration pas à pas demandé et livré en **Annexe A** (FreeCAD MCP, Blender MCP ; note Docker — utile pour le serveur de Corée et WebODM, pas nécessaire pour les MCP eux-mêmes).

Acquis v0.4 maintenus sans changement : twin EMRAX (mule mono-EMRAX), pack P45B en tranches, balisage nuit, dock enceinte, convertibilité 12 mois, innovations et biomimétisme clos, réponse « FIA-ready = ~15 kg, non-pénalité nette » (§6.6).

# Synthèse de l'architecture (acquis des itérations 1-2)

## Structure

Cas dimensionnant : réception à plat après 2 m — v = (2gh)^{1/2} ~ 6,3 m/s, ~22,6 kJ ; ~0,48 m de course utile -> 4,2 g moyens, **8 g de calcul, 12 g ultime** ; tours d'amortisseur AR dimensionnés ~47 kN (coef 1,5). Principes : **triangulation totale** (tout ancrage à < 25 mm d'un nœud ; aucun quadrilatère non contreventé dans un chemin d'effort) ; **deux niveaux de structure** (cellule de sécurité CDS cotes FIA — arceau principal 50 × 2,0 — + exosquelette 4130) ; **quille-batterie structurelle** 6061/7075 (~1/3 de la rigidité) ; **8 grappes de nœuds**, les plus chargées en pièces génératives (polymère d'abord, §4.2).

## Masses et motricité

**43/57 AV/AR, CG <= 530 mm.** Poussée max : a/g = µ · f_{R} / (1 - µ · h/L) -> **0,45-0,6 g soutenus dans le sable** : limité par la motricité, pas la puissance. Levier n°1 : **TC à consigne de glissement sable** (optimum paddle à 20-35 %). En vol : ~16°/s d'autorité à piquer (freinage des masses tournantes), cabrage par impulsion de couple ; régén coupée en aérien sauf commande d'assiette.

## Thermique (45 °C, poussière fine)

**~12 kW continus.** Boucle A traction (65 °C max) : 0,30-0,35 m² de radiateur, ventilateurs haute pression sur le pont AR. Boucle B batterie (25-40 °C) : **chiller 4 kW obligatoire**, plaques froides, delta cellule < 4 K, **pré-refroidissement à 22-25 °C** (~20 min de marge à fond). Durcissement : ailettes 8-10 FPI + pré-grilles, prises hautes, IP67/IP69K, moteurs fermés, sabots UHMW.

# Design lock : le langage « Organic Exo »

**[VERROUILLÉ]** — L'ingénierie *est* le design.

## Vocabulaire formel

- **Épine dorsale continue** de l'arceau à la queue.
- **Nœuds génératifs exposés**, pièces d'orfèvrerie.
- **Ligne de tension latérale** unique, tendue façon Ferrari.
- **Quatre bypass en tuyaux d'orgue** sur le pont arrière.
- **Visserie usinée apparente**, alignée.

## Matières et finitions

| Zone | Matière / finition |
| Tubes exosquelette | Titane torché (jalon 3) ou 4130 verni satin (jalons 1-2) |
| Quille batterie | Carbone mat / aluminium usiné brut |
| Nœuds génératifs | Ti / Scalmalloy brut, interfaces usinées |
| Accents | Cuivre bruni (échangeurs, durites gainées) |

## Interdits (garde-fous)

Aucune carrosserie enveloppante ; **aucun écran côté pilote** (data station copilote amovible autorisée, §5.2) ; pas de plastiques peints ni faux carbone. Et depuis la clôture des innovations (§4.4) : **aucun ajout qui ne se paie en performance** — le monstre est épuré et continu, pas un sapin de Noël.

## Conséquences d'ingénierie

Nœuds = surfaces de classe A ; câblage HT dans tubes/quille ; radiateurs assumés graphiquement.

## Signature lumineuse nocturne

- **Ligne LED continue le long de l'épine dorsale** : de nuit, le véhicule EST sa silhouette.
- **Barre LED avant haute** (2 spots longue portée + nappe large), montée haute contre les ombres rasantes trompeuses.
- Feux AR signature + éclairage de travail commutable ; cockpit **rouge asservi** (vision nocturne préservée).
- Budget électrique ~250 W, négligeable. Le balisage du terrain, lui, est au §9.5.

# Innovations transversales : acquis, trajectoires, clôture

## État des concepts (arbitrages rendus)

| N° | Concept | Statut |
| 1 | Contrôle d'assiette prédictif (AC75) | [EN ÉTUDE] file P1-bis |
| 2 | Télémétrie suspension par histogrammes (VTT DH) | **[VERROUILLÉ]** trio prioritaire |
| 3 | Blackbox + méthode tuning FPV | [EN ÉTUDE] couplé VCU |
| 4 | Nœuds génératifs polymère d'abord (aérospatial) | **[VERROUILLÉ]** trio prioritaire |
| 5 | Siège jamming granulaire | [EN ÉTUDE] backlog |
| 6 | Banc à tambour pales de paddle | [EN ÉTUDE] file P1-bis |
| 7 | Gréement textile Dyneema | [EN ÉTUDE] backlog |
| 8 | Glissement vrai RTK-GNSS + EKF (FS Driverless) | **[VERROUILLÉ]** trio prioritaire |
| 9 | Immersion diélectrique module | [EN ÉTUDE] backlog conditionnel |
| 10 | Monitoring physiologique pilote | **[VERROUILLÉ]** |
| 11 | Gestion de pression pneus embarquée (trophy trucks) | **[VERROUILLÉ]** — ajout final, §4.4 |
| 12 | VCU de secours « rentre au camp » (spatial) | **[VERROUILLÉ]** — ajout final, §4.4 |
| 13 | Commandes volant type F1 | **[VERROUILLÉ]** — ajout final, §4.4 |

## Protocoles actifs du trio prioritaire

- **n°2 — Histogrammes** : 4 potentiomètres linéaires + ESP32 à 1 kHz ; les histogrammes de vitesse de tige disent objectivement où manquent compression/détente.
- **n°4 — Nœuds polymère d'abord** : impression des 3 nœuds les plus chargés, essais à rupture + corrélation FEA, puis métal. La confiance à 15 EUR la pièce au lieu de 1 500.
- **n°8 — RTK + EKF** : vitesse sol vraie au cm/s -> glissement réel pour le TC. Réutilisé par l'AR, le balisage (§9.5) et la logistique de scan.

## Trajectoires : d'où viennent ces technologies, où elles vont

| Domaine | Hier | Aujourd'hui | Horizon 2030 | Notre placement |
| Suspension | Essieux rigides ; bypass nés en Baja 90's | Semi-actif haut de gamme usine | Prédictif : lire le terrain avant l'impact | Notre feedforward ToF est cette trajectoire, en accessible |
| Batteries | Plomb ; NiMH ; 18650 (2008) | 21700/4680, prix -8 %/an | Semi-solide/solide 350-450 Wh/kg vers 2028-30 | Quille **repackable** : on changera de chimie sans toucher au châssis |
| Moteurs | Balais ; induction 90's | PMSM partout, flux axial en pointe | Flux axial banalisé ; sans-terres-rares monte | Berceau **agnostique** : mono -> twin -> techno suivante |
| Matériaux | Acier doux ; CrMo ; carbone hors de prix | Impression métal petite série, -15-20 %/an | Nœuds imprimés = standard | Polymère d'abord : prêts quand le prix tombe |
| Contrôle | Mécanique ; premières ECU | Vectorisation, véhicule défini par logiciel | La valeur migre vers firmware et données | VCU **open versionnée** : chaque session enrichit un actif |
| Interface | Jauges ; puis écrans partout | Reflux vers minimal : HUD, voix, haptique | AR légère mature | Pari audio-d'abord déjà aligné |

**Position stratégique** : les tubes durent vingt ans, tout le reste s'upgrade. ORGANIC EXO est une **plateforme** — châssis intemporel, énergie interchangeable, intelligence logicielle croissante. Le propriétaire anticipe des compétitions électriques : quand elles ouvriront, la plateforme sera prête (< 12 mois, §6.5) et le pilote aura appris dune après dune, guidé par la ligne et le copilote digital.

## Trois ajouts finaux, puis liste close [VERROUILLÉ]

Dernier balayage demandé (spatial, F1, sports moteurs, nature) avec le filtre « gain tangible ou rien » :

- **11. Gestion de pression embarquée** (trophy trucks / overlanding) : la pression des paddles est LA variable de grip la plus négligée — le sable froid du matin et la dune sèche de l'après-midi ne demandent pas la même. Compresseur + électrovannes + presets au volant (« matin / midi / dune sèche »), mesure par capteurs TPMS. Gain immédiat mesurable au chrono et à l'échauffement pneu. ~450 EUR.
- **12. VCU de secours « rentre au camp »** (redondance dissimilaire, aérospatial) : micro-contrôleur totalement indépendant de la VCU principale, chemin de couple minimal bridé à 15 km/h, activation par bouton gardé. Dans le désert, la panne électronique ne doit jamais signifier la nuit sur place. C'est l'« assurance-vie » version électronique. ~120 EUR.
- **13. Commandes volant type F1** : molette de consigne de glissement TC (12 crans), sélecteur de modes (Dune / Duel / Nuit / Rentre), paddle de régén forte. Le réglage se fait en roulant, les yeux sur la dune — exploitation, pas gadget. ~250 EUR.

**Clôture** : la liste d'innovations est **close**. Critère d'entrée désormais : démontrer un gain mesurable sur vitesse de dune, autonomie de session ou sécurité — sinon refus, quel que soit le charme de l'idée. Un monstre épuré et continu, qui rugit de puissance : rien d'amorphe, rien de décoratif.

# Interface pilote-machine et système AR topographique

**Zéro écran côté pilote.** Architecture 4 couches inchangée (drone -> mesh WebODM -> ligne -> restitution).

## Paliers de restitution — tous validés [VERROUILLÉ]

- **A — Pacenotes audio synthétiques** (MVP) : notes générées du mesh, déclenchées par RTK, voix casque. Coût ~0, latence nulle.
- **B — Bandeau LED périphérique** : écart à la ligne, alertes. **Mode nuit** : intensité asservie, palette décalée rouge.
- **C — HUD léger** : lunettes waveguide BLE (~40 g, zéro câble), symbologie minimale (3 chevrons, delta vitesse, 2 alertes). Meilleur de nuit qu'en plein soleil.
- **D — Haptique volant** : vibreurs moyeu (alerte lèvre/ligne quand l'audio sature).

## Data station copilote [VERROUILLÉ]

Tablette durcie **amovible** côté copilote (invisible du pilote ; retirée = cockpit pur) : carte mesh + position, télémétrie live, budget batterie, replay. Le copilote pilote les pacenotes (marquage de points, dictée sur section inconnue) — le rôle du copilote de rallye, augmenté. C'est aussi le poste de formation : le jour où un ami embarque (la raison des deux places), il apprend le terrain sur la data station avant de prendre le volant. En solo, la tablette reste au camp.

## Mode nuit du système

Scan drone **de jour**, session de nuit sur le mesh du jour — le RTK ne voit pas la nuit, rien ne change pour le guidage ; c'est là que le système vaut le plus (le terrain que les yeux ne lisent plus, le mesh le connaît). Pacenotes nocturnes : annonces plus précoces, vocabulaire dédié (« crête invisible », « creux noir »). Sécurité : jamais seul de nuit, périmètre convenu, l'épine LED comme balise, point de ralliement GPS. Le balisage lumineux du parcours (§9.5) complète le dispositif.

## Musique embarquée : le dock enceinte [VERROUILLÉ - nouveau]

Le véhicule est silencieux — la musique devient possible là où un thermique la couvrirait. Réponse à la demande :

- **Dock à came sur la traverse arrière-sièges** : l'enceinte (classe sono mobile 12 V, IP65, ~4 kg) se pose en 10 secondes, se verrouille, se branche en une prise (12 V + ligne audio). Pas envie ? Elle reste au camp, le dock disparaît visuellement — cohérent avec le design lock.
- **Priorité vitale garantie** : mixeur audio dans la VCU — toute pacenote ou alerte **duck** la musique (–18 dB instantané). La musique est une passagère, jamais un pilote.
- Au camp, le même dock existe sur l'établi/remorque : une seule enceinte pour les deux vies. ~400 EUR.

# Conformité FIA et usage hors compétition

## Positionnement : « FIA-ready, pas FIA-bound » [VERROUILLÉ]

T3 (art. 286) / T4 (art. 286A) ; pas de classe 100 % électrique ouverte à ce jour — le propriétaire parie qu'elles viendront : la plateforme sera prête. T3 interdit les aides -> **mode « TC off » câblé** conservé. Philosophie d'engagement actée : la compétition, si elle vient, sera la mise en pratique du loisir appris dune après dune — pas une reconstruction.

## Cellule de sécurité : invariants figés (art. 283)

Arceau principal **50 × 2,0 ou 45 × 2,5 mm** acier carbone CDS (>= 350 N/mm²) ; autres éléments 38 × 2,5 / 40 × 2,0 ; chromoly cantonné à l'exosquelette. Pieds + goussets réglementaires, dégagement casque, harnais 6 points (8853-2016) sur nœuds, sièges 8862, extincteur plombé, coupe-circuits int/ext, évacuation < 7 s.

## Sécurité haute tension (esprit FIA + ECE R100)

Caisson anti-intrusion (>= 50 mm d'écrasement, 20 g longitudinal), HT hors zones de déformation, HVIL partout, IMD, sectionneur sans outil, voyant secours, équipotentialité < 0,1 ohm, IP67/IP69K, fiche d'intervention rédigée dès la V1.

## Usage route : tranché

RTI irréaliste, L7e-B2 incompatible — **[REJETÉ]** définitif. Terrains fermés + transport (§9.4).

## Conversion compétition : < 1 journée, convertibilité < 12 mois [VERROUILLÉ - amendé]

La fenêtre de convertibilité passe de 6 à **12 mois** (retour propriétaire : plus de liberté pour faire vivre le modèle personnel). Le reste tient : conforme en permanence (cellule, ancrages, HT — la sécurité n'a pas de « mode ») ; basculable jour J (TC off scellable, data station et HUD retirés, éclairage additionnel déposé par connecteurs rapides) ; **dossier prêt en permanence** — requalifié par le propriétaire : ce n'est pas un surplus administratif, c'est son assurance-vie. Rouler vite dans des dunes reste dangereux ; le classeur (certificats matière, qualification soudeur, CAO de cage, fiche secours) est la preuve que la machine mérite la confiance qu'on lui fait à 100 km/h au sommet d'une crête.

## « Le FIA-ready pénalise-t-il la performance ? » [nouveau - réponse chiffrée]

Question du propriétaire. Réponse : **~15 kg et 2-3 mm de CG — et il en rend plus qu'il n'en prend.**

- La cellule aux cotes FIA (E355 CDS, 50 × 2,0 = 2,37 kg/m) pèse plus lourd qu'une cage 4130 optimisée à l'extrême (44,5 × 1,6 = 1,69 kg/m, permise par la meilleure limite élastique du chromoly). Sur ~22 m d'éléments de cage : **+15 kg environ**, en hauteur, soit +2-3 mm de centre de gravité. C'est ~1,3 % de la masse : imperceptible au chrono dans le sable, où la motricité sature bien avant.
- En échange : la cage FIA est **plus rigide** (sections supérieures) — et la rigidité châssis, elle, se sent à chaque appui : la précision de conduite s'améliore ; les bypass travaillent au lieu de tordre le cadre ; la cible >= 3 000 Nm/deg devient plus facile.
- Et l'essentiel, dit avec les mots du propriétaire : à 12 g ultimes, ces 15 kg sont ceux qui décident si l'on ressort du châssis en marchant. **Verdict : non-pénalité nette — c'est le meilleur échange masse/valeur de tout le véhicule.**

# Énergie et motorisation

## Acquis (inchangés)

NMC 21700 traction, LFP tampon statique ; H2, prolongateur, LTO, Na-ion traction, supercondensateurs, moteurs-roue : [REJETÉS], motifs en historique. Récupération au freinage confirmée. Flux axial = référence (96-98 % pic).

## Chaîne de traction : re-verrouillée par le budget élargi [VERROUILLÉ]

« Pour le moteur, je veux ce qui se fait de mieux » + trajectoire budgétaire multi-année -> l'arbitrage v0.3 est levé :

- **Véhicule final : 2 × EMRAX 268 LC + 2 onduleurs SiC + réducteurs ~4:1** — vectorisation de couple vraie, ~10 kW/kg, le meilleur rapport performance/documentation accessible en petite série. (~18-20 k EUR, jalonnés.)
- **Mule (an 1) : le PREMIER des deux EMRAX**, en mono-moteur + différentiel provisoire. Rien n'est acheté pour être jeté : le moteur, l'onduleur, le firmware et les logs de la mule migrent tels quels sur le final. Le RDU Tesla du scénario A v0.3 est **[REJETÉ]** — il aurait été du matériel de transition à revendre.
- Le berceau AR reste agnostique (mono/twin/techno future).

## Batterie : pack modulaire en tranches [VERROUILLÉ - nouveau]

Le financement par apports successifs devient un principe d'architecture : la quille reçoit des **tranches 96s interchangeables** (même format, même refroidissement, même BMS maître).

- **Tranche 1 (mule)** : 96s10p P45B ~ **15,5 kWh** (~60 kg de cellules, ~5 k EUR) — assez pour développer TC, suspension et thermique en sablière (sessions 30-45 min, recharge 32 A sur site).
- **Tranches 2-3 (final)** : extension à 96s28p ~ **43,5 kWh** (~9-10 k EUR de plus, jalon 2) — l'autonomie d'expédition.
- Chaque tranche est un caisson IP67 autonome mécaniquement : on grandit sans re-concevoir, et un repack futur (chimie 2030) se fait tranche par tranche.

## Sourcing Chine : l'analyse honnête [nouveau]

Le propriétaire a de la famille en Chine et l'intuition qu'on y trouve « plus de moteurs, moins cher ». Vrai à l'échelle industrielle — la Chine domine la production mondiale de machines électriques — mais nuancé pour NOUS :

- **Moteur : non.** Les excellents moteurs chinois (BYD, JJE, Inovance...) sont vendus par dizaines de milliers aux constructeurs, pas à l'unité documentée. Ce qui s'achète à l'unité (plateformes type Alibaba/1688) arrive sans courbes de rendement fiables, sans support d'intégration (resolver, cannelures, protocoles onduleur), sans garantie exécutable. « Le mieux » en petite série documentée reste européen (EMRAX — Slovénie). On n'économise pas 5 k EUR pour perdre six mois d'intégration sur le composant le plus critique.
- **Composants : oui, massivement.** Contacteurs HT, pyrofuses, BMS esclaves, chargeurs OBC, câble silicone HT, connecteurs, plaques froides, LED et balisage, visserie titane, CNC de pièces **non-critiques** : qualité excellente à 40-60 % du prix européen. Règle intangible : **aucune pièce de vie (cage, suspension, direction, freinage, ancrages) sans traçabilité matière certifiée** — ces pièces restent européennes ou certifiées.
- **Rôle de la famille** : consolidation de colis (un transitaire regroupe, la famille réceptionne/vérifie), éventuel contrôle visuel avant envoi. A noter : Urumqi est à ~4 000 km des hubs de Shenzhen — le transitaire fait le travail, la famille apporte la langue et la confiance, pas la proximité.
- Estimation d'économie sur la BOM hors moteur/cellules : **-2 500 à -4 000 EUR** sur la trajectoire. Les cellules Molicel, elles, sont taïwanaises et s'achètent chez les distributeurs européens (traçabilité + transport lithium réglementé).

## Recharge terrain

Chargeur embarqué 6,6 kW (32 A industriel) : tranche mule pleine en ~2 h 30, pack final en ~7 h (la nuit). Raccordement 32 A négocié dans la convention sablière (§9.2). Génératrice de location en expédition ; remorque solaire reportée (jalon 3, optionnel).

## « Un moteur, ça s'améliore ? » [pédagogie]

Réponse courte : **oui, mais pas là où on croit.** Un moteur électrique : des électroaimants (stator) créent un champ tournant, des aimants (rotor) le poursuivent ; l'onduleur décide 20 000 fois par seconde où envoyer le courant. Pertes : cuivre (chauffe à fort couple), fer (haute vitesse), mécanique, onduleur — total 3-8 %. Un moteur moderne est à 96-97 % au meilleur point : **il ne reste presque rien à gagner en rendement crête.** Les quatre leviers réels, par retour sur investissement :

1. **Le logiciel** (gratuit, majeur) : MTPA, défluxage, et surtout notre TC à glissement — 10-20 % d'« efficacité de mission » (distance/kWh, temps au tour) là où le rendement moteur ne bouge que d'un point. Notre terrain de jeu, amélioré à chaque session par les logs.
2. **Le refroidissement** (le vrai tuning matériel) : un moteur s'étouffe en chaleur ; améliorer débit/plaques/huile ne change pas le rendement mais **la durée de crête disponible** — fonctionnellement un moteur plus gros. Atelier + télémétrie.
3. **La transmission** (1-3 %) : denture, huile, alignement — fiabilité surtout.
4. **Le hardware interne** (rebobinage, aimants) : territoire industriel, ROI amateur quasi nul — on choisit bien au départ (c'est fait : EMRAX).

Le « monstre d'efficacité » se construit dans le firmware et la thermique — précisément là où un propriétaire investi + une IA excellent.

## Les aimants : réponse à la curiosité

**Maglev : non** (il faut un rail ou une surface conductrice + des puissances folles ; et sans contact, pas de force latérale pour tourner) — mais la question méritait d'être chiffrée. **Magnétorhéologique** : sérieux mais inexistant en course 500 mm — veille. **Là où les aimants servent dès la V1** : capteurs Hall (sans contact, immunisés poussière), **accouplements magnétiques des pompes** (zéro fuite, décrochage au lieu de casse), fixations rapides magnétiques + goupille (conversion < 1 jour). Et nos EMRAX *sont* des machines à aimants en arrangement optimisé — la plus belle application d'aimants du véhicule.

# Biomimétisme : verdict rendu, liste close

## Tableau d'évaluation (rappel des retenus)

| Source | Transfert | Pertinence |
| Fennec (oreilles-radiateurs) | Échangeurs grande surface hauts dans l'air propre | **Haute** — appliqué boucle A |
| Fourmi argentée du Sahara | Revêtement réfléchissant IR du caisson batterie (-5 à -10 °C de charge solaire) | **Haute** — essai ~80 EUR au jalon 1 |
| Termitière | Carénage-cheminée d'extraction au-dessus des radiateurs (convection gratuite à l'arrêt) | **Haute** — intégré au dessin AR |
| Chameau (« stocker du frais ») | Valide le pré-refroidissement pack : la « bosse thermique » avant session | **Haute** (conceptuel, appliqué) |
| Sidewinder + scinque | Géométrie/texture des pales de paddle (banc n°6) | **Haute** — banc défini |
| Kangourou (tendons-ressorts) | Lecture énergétique de la détente ; lames stockantes d'appoint | Moyenne — après télémétrie n°2 |
| Arbres (Mattheck) | Règle de congés « racinaires » dans le cahier de dessin des nœuds | Moyenne — adoptée |

## Le dernier balayage demandé

Avant clôture, revue élargie « chaque plante, chaque bête, chaque phénomène » avec le filtre du gain tangible : cactus (auto-ombrage par côtes -> couvert par le revêtement IR), bousier (navigation céleste -> gadget, le RTK fait mieux), organes à fosses des crotales (vision IR -> une caméra thermique de secours coûterait plus qu'elle ne rapporte), peau de requin (riblets -> traînée négligeable à nos vitesses), gecko (adhésion -> neutralisée par la poussière), scarabée de Namibie (eau du brouillard -> hors périmètre véhicule). **Rien de nouveau ne passe le filtre.**

## Clôture [VERROUILLÉ]

La nature a rendu son verdict : sept transferts retenus, tous intégrés au design ou au backlog d'essais — le désert avait déjà résolu la chaleur et le sable, nous avons pris ses réponses. La partie biomimétisme est **close**, comme la liste d'innovations (§4.4) : elle ne rouvrira que si un problème nouveau apparaît (« qui, dans le vivant, a déjà ce problème ? » restera le premier réflexe — mais en réponse à un problème, jamais en chasse aux idées).

# Logistique terrain

Base : **Bordeaux**. Pas de véhicule tracteur disponible -> stratégie « stockage sur site + transport ponctuel » (§9.4).

## Le point réglementaire : le Pilat est exclu [VERROUILLÉ - rappel]

Site classé + article **L.362-1 du code de l'environnement** : la circulation motorisée hors voies ouvertes est interdite partout en France — aucune dune naturelle française n'est praticable. Sanctions lourdes, image désastreuse. Non négociable.

## Sablières girondines : la liste demandée [EN ÉTUDE - priorité]

Le bassin sableux girondin (axe Cestas - Saint-Jean-d'Illac - Marcheprime - Mios - Salles, le long de l'A63/A660, à 20-45 min de Bordeaux) concentre les exploitations. Liste issue des annuaires publics — à qualifier par contact, certains sites évoluent :

| Exploitant | Localisation | Note d'approche |
| **Sibelco France (SIFRACO)** | Mios, route du Barp | Groupe international (silice) : process de convention carré, grands sites sableux |
| **Sablière de Saint-Jean-d'Illac** | Saint-Jean-d'Illac, lieu-dit Sauts | Exploitant local : circuit de décision court — cible n°1 pour une convention souple |
| **Établissements Fabre** | Cestas, chemin de Jarry | Entreprise familiale (1958) : approche directe possible |
| **CEMEX Granulats Sud-Ouest** | Siège Pessac, sites en Gironde | Grand groupe : passer par le responsable foncier régional |
| **GSM (Heidelberg Materials)** | Sites girondins | Idem : politique RSE ouverte aux usages tiers encadrés |
| **Lafarge Granulats** | Sites girondins | Idem |

Méthode en trois canaux, en parallèle : (1) contact direct des deux locaux (Illac, Fabre) ; (2) **UNICEM Nouvelle-Aquitaine** (fédération des carrières : un seul mail touche tous les adhérents — demander « site en fin d'exploitation ouvert à une convention d'usage sportif électrique ») ; (3) registre des carrières actives de la **DREAL Nouvelle-Aquitaine** (données publiques) pour les sites en fin d'autorisation — souvent les plus ouverts. Arguments clés : véhicule **électrique silencieux** (zéro plainte voisinage — l'argument décisif vs moto-cross), zéro hydrocarbure, RC circuit, créneaux hors exploitation, indemnité + **location d'un emplacement conteneur** (revenu récurrent pour eux, solution transport pour nous). Lettre type : fournie à la prochaine itération. [Action : propriétaire valide le lancement des contacts]

## Expéditions : UAE, seul horizon extérieur [VERROUILLÉ - tranché]

Décision propriétaire : **non à la Chine (import) et non au Maghreb** (Maroc, Tunisie et le reste du Sahara nord-africain) — réserves administratives assumées. Par honnêteté de dossier, la seule formule qui lèverait mécaniquement la réserve Maghreb est consignée pour mémoire : un événement « clé en main » où l'organisateur transporte et dédouane lui-même **tout le parc** depuis la France (le participant ne touche jamais la douane) — si une telle offre carrée existe un jour au départ de Bordeaux, elle pourra être re-présentée ; d'ici là, **[REJETÉ]**, on n'en parle plus.

- **UAE — la destination extérieure unique [VERROUILLÉ]** : conteneur 20' Bordeaux -> Jebel Ali (~2-3 k EUR AR), **admission temporaire officielle 6 mois** (carnet CPD/ATA, procédure écrite, zéro arbitraire), hiver 20-28 °C idéal pour le chiller, zones désert libres (Liwa, Sweihan), la plus grande communauté sandrail du monde, pas de permis requis en zone désert. « Le plus élégant et le moins risqué » — exactement. Programmé au sous-jalon S9 (§10), véhicule mûr.
- **La piste « Gobi » [EN ÉTUDE - horizon lointain]** : l'inversion du propriétaire est la bonne — ne pas amener le buggy en Chine, **en construire un sur place**. Atouts réels : le beau-oncle dirige la sécurité d'un centre de loisirs du désert de Gobi (terrain privé + autorité locale = l'équivalent chinois de notre sablière, avec l'autorisation au bon niveau), la famille sur place, et le sourcing chinois devient optimal puisqu'il n'y a plus d'export — moteur chinois enfin pertinent (achat local), cellules CATL/EVE locales, soudure locale. Lucidité : c'est un **second projet à part entière** (plans adaptés à l'offre locale, soudeur qualifié à trouver sur place, règles du centre à cadrer), pas une copie triviale. Il ne s'étudiera sérieusement qu'une fois le véhicule français mûr — et ce référentiel (plans, firmware, leçons de sablière) en sera le point de départ tout trouvé. Rien n'est budgété à ce stade.

## Transport sans véhicule tracteur [nouveau - remplace le plan remorque]

Pas de PTAC disponible -> on inverse le problème : **le véhicule ne rentre pas à Bordeaux, il vit sur son terrain.**

- **Stockage sur site sablière** : conteneur maritime 20' aménagé (occasion posée ~2 500-3 000 EUR, ou location intégrée à la convention) — atelier sec, recharge 32 A, antivol sérieux (le site est clôturé et gardienné, c'est le métier d'une carrière). Zéro remorquage au quotidien : on vient en voiture, on roule, on branche, on repart.
- **Permis [VERROUILLÉ - sous-jalon S0]** : pas encore de permis B — parcours acté : **permis B d'abord** (~1 500 EUR, 3-6 mois de délai réel : c'est le chemin critique du projet, à lancer tout de suite), puis **B96** (formation 7 h, ~250 EUR, sans examen). Bonne nouvelle en attendant : conduire le buggy sur terrain privé fermé n'exige **aucun permis** — le pilotage commence avant le papier rose (seule l'assurance RC circuit peut poser une condition : à vérifier au devis, beaucoup de contrats loisir n'en exigent pas).
- **Transports ponctuels** (événement, expédition) : d'ici l'obtention des permis, **transporteur plateau** porte-à-porte (~2-3 EUR/km, sans permis ni stress) ; ensuite, location utilitaire + porte-engin à la journée (~200-300 EUR/we).
- **Achat d'un tracteur + remorque : [REJETÉ] à ce stade** — ~20 k EUR immobilisés pour quelques trajets/an ; la location et le transporteur font mieux. Ré-évaluable si la cadence d'événements explose.

## La nuit « Forza Horizon » : balisage lumineux du parcours [VERROUILLÉ - nouveau]

L'idée du propriétaire est excellente et techniquement mûre — et elle boucle élégamment avec le système AR : **la ligne de course calculée devient physique.**

- **Piquets LED RGB rechargeables** (~60 unités, IP67, fiche sable lestée) posés aux waypoints exportés du solveur de ligne : le RTK donne la position de pose au mètre — on matérialise la trajectoire optimale, pas une trajectoire au jugé.
- **Grammaire couleur** : ambre = apex/corde, **rouge = bord de piste et dangers** (lèvres, zones molles — la demande initiale), bleu-blanc = ligne droite lancée, vert = zone de départ/arrivée. Pilotage ESP32 + LoRa mesh : scénarios (« course », « chill », « guidage retour », extinction générale).
- **Spots d'ambiance** sur mâts à batterie (4 × LED chantier 100 W) : les points hauts du parcours et « l'oasis » du camp — l'ambiance Forza Horizon, sans groupe électrogène.
- **Règle de sécurité absolue** : le balisage est de la *scénographie et de la confirmation*, jamais de l'éclairage de conduite — le relief se lit aux phares et aux pacenotes (le mesh connaît le terrain, les piquets non). Les piquets sont frangibles (percutés sans dommage).
- Budget : ~1 800 EUR (piquets) + ~600 EUR (spots) + ~200 EUR (contrôle) — jalon 2. Pose/dépose : ~45 min à deux pour 2 km de parcours, les positions RTK étant pré-calculées.
- Bonus sablière : un parcours balisé au cordeau, silencieux et spectaculaire de nuit, est aussi le meilleur argument de démonstration auprès de l'exploitant et des assureurs — c'est tout sauf du hors-piste sauvage.

# Budget : sous-jalons à rythme libre

Retour propriétaire : 37 k en un an, c'est trop gros aujourd'hui — on ralentit. Le principe change : **plus de jalons annuels — des sous-jalons déclenchés quand l'épargne y est.** Chacun est utile seul, se stocke sans se dégrader, et n'engage pas le suivant. L'ordre est technique (on ne soude pas après avoir posé la batterie) ; le rythme est le vôtre.

| Sous-jalon | Contenu | Coût | Cumul |
| **S0 — Fondations** | Permis B (~1,5 k) + B96 (~250) ; bancs trio n° 2/4/8 (~1,2 k) ; CAO/FEA (moi, gratuit) ; démarches sablière (Annexe B) | ~3 k | 3 k |
| **S1 — Colonne** | Cellule FIA + exosquelette + quille (tubes, soudure qualifiée, visserie) | ~6,5 k | 9,5 k |
| **S2 — Jambes** | Bras + 4 bypass + direction + freins + moyeux + paddles/skis | ~8 k | 17,5 k |
| **S3 — Cœur** | 1er EMRAX 268 LC + onduleur SiC + réducteur | ~10 k | 27,5 k |
| **S4 — Sang** | Tranche pack 15,5 kWh + HT + thermique (cellules achetées en dernier : le lithium ne doit pas dormir en carton) | ~8 k | 35,5 k |
| **S5 — Nerfs** | VCU + télémétrie + RTK ; sièges/harnais/extincteur ; éclairage. **La mule roule.** | ~4 k | 39,5 k |
| S6 — Twin | 2e EMRAX + onduleur (vectorisation vraie) | ~10 k | 49,5 k |
| S7 — Souffle | Tranches pack -> 43,5 kWh | ~10 k | 59,5 k |
| S8 — Sens | Interface C/D + data station ; balisage nuit ; enceinte ; drone ; gestion de pression | ~5 k | 64,5 k |
| S9 — Horizon | Conteneur + saison UAE ; titane torché + nœuds métal ; VCU secours ; marge | ~14-18 k | ~78-83 k |

Garde-fous : prix re-confirmés au devis **à l'ouverture** de chaque sous-jalon (ce tableau pilote, il ne promet pas) ; économie sourcing Chine (-2,5 à -4 k, §7.4) et recettes éventuelles en déduction, jamais en pari ; cellules batterie toujours en dernier dans leur sous-jalon (fraîcheur). Ordre de grandeur du rythme : ~500 EUR/mois d'épargne met la mule (S5) à ~6 ans, ~1 000 EUR/mois à ~3 ans — **c'est l'épargne qui décide, pas le calendrier**. Et S0 s'ouvre à ~3 k : le projet démarre concrètement dès que le permis est lancé.

# Feuille de route, décisions, outillage

## Phases

| Phase | Contenu | Sortie |
| P0 — Numérique (en cours, gratuit) | Modèle dynamique 2-DOF sable, CAO cage paramétrique (FreeCAD MCP), FEA quille | Géométrie figée |
| P1 — S0 | **Permis B** (chemin critique) puis B96 ; bancs trio n° 2/4/8 ; lettre sablière (Annexe B) via les 3 canaux §9.2 | Données réelles + convention site + mobilité |
| P2 — S1 à S5 | Châssis complet, mono-EMRAX, tranche pack 1, TC v1 — au rythme de l'épargne | **La mule roule** |
| P3 — S6 à S8 | 2e moteur (twin), pack complet, interface C/D, balisage nuit, drone | Le monstre complet |
| P4 — S9 | Saison UAE en conteneur ; titane + nœuds métal ; VCU secours | Programme complet |

## Décisions attendues [A DÉCIDER]

1. **Ordre des sous-jalons S0-S9 validé tel quel ?** (le découpage est technique, mais l'ordre S2/S3 peut s'inverser si une opportunité d'occasion se présente sur les bypass ou le moteur).
2. **Permis B : inscription lancée ce mois-ci ?** C'est le chemin critique — tout le reste peut attendre, pas ça.
3. **Lettre sablière (Annexe B)** : relire, personnaliser les champs [entre crochets], me dire « envoie » — je préparerai alors la liste de diffusion finale (2 locaux + UNICEM).
4. **MCP** : dérouler l'Annexe A (FreeCAD puis Blender) et me dire quand c'est en place — la CAO de la cage basculera alors en modélisation pilotée en direct.
5. **Prochaine itération technique** : modèle dynamique 2-DOF + CAO paramétrique de la cage — valider ou réorienter.

## Outillage MCP recommandé

1. **FreeCAD MCP** (`neka-nat/freecad-mcp`) — priorité : je modélise cage, quille et bras en paramétrique. 2. **Blender MCP** — rendus Organic Exo, études de la signature lumineuse et du balisage nocturne. 3. **KiCad MCP** (sous-jalon S5) — schémas électriques. Déjà en place : GitHub, PDF, recherche web. **Le guide d'installation pas à pas est en Annexe A** (demande propriétaire — avec la réponse à « j'ai Docker » : inutile pour les MCP, précieux pour le serveur de Corée et WebODM).

## Infrastructure numérique : le serveur de Corée [VERROUILLÉ - nouveau]

Le serveur Vultr existant (Séoul, usage VPN) devient le **camp de base numérique** du projet, à coût marginal nul :

- **Télémétrie** : InfluxDB + Grafana — chaque session uploade ses logs (4G au retour au camp) ; dashboards accessibles de partout (et par le copilote resté en France).
- **Meshes et lignes** : dépôt versionné des scans drone et trajectoires par site — la mémoire topographique du projet.
- **CI firmware** : compilation et tests automatiques de la VCU à chaque commit (runner GitHub Actions).
- **WebODM CPU** en dépannage (sans GPU : lent mais fonctionne pour les petits meshes ; le laptop terrain reste l'outil principal).
- La latence Séoul-France (~280 ms) est sans importance : **rien de temps réel ne passe par le cloud** — tout le vital est embarqué. Le VPN existant sécurise l'ensemble. Bonus : sauvegarde hors-site de ce référentiel.

# Annexe A — Intégrer les MCP pas à pas

> **Important** : un serveur MCP tourne sur **votre** machine — celle où FreeCAD/Blender et Claude Desktop (ou Claude Code en terminal) sont installés. Les sessions Claude web/distantes ne voient pas votre localhost : une fois l'installation faite, ouvrez une session **Claude Desktop** ou un terminal `claude` local, et je piloterai la CAO en direct. Ce dépôt Git reste le pont entre les deux mondes (je pousse les scripts, vous les voyez en local, et inversement).

## A.1 — Prérequis (10 minutes)

1. **Python 3.10+** : python.org (sous Windows, cocher « Add Python to PATH » à l'installation).
2. **uv** (lanceur d'outils Python) : dans un terminal, `pip install uv` — vérifier avec `uvx --version`.
3. **Claude Desktop** à jour (claude.ai/download), et/ou **Claude Code** en terminal : `npm install -g @anthropic-ai/claude-code`.
4. **Docker** : pas nécessaire ici — ces MCP tournent en local via `uvx`, sur un socket localhost, rien n'est exposé au réseau. Votre Docker servira au §A.4.

## A.2 — FreeCAD MCP (la priorité : la cage se dessinera là)

1. Installer **FreeCAD 1.0+** : freecad.org.
2. Installer l'addon serveur : sur github.com/neka-nat/freecad-mcp, bouton Code > Download ZIP ; dézipper ; copier le dossier `addon/FreeCADMCP` dans le répertoire des modules FreeCAD — Windows : `%APPDATA%\FreeCAD\Mod\` ; macOS : `~/Library/Application Support/FreeCAD/Mod/` ; Linux : `~/.local/share/FreeCAD/Mod/`. Redémarrer FreeCAD.
3. Dans FreeCAD : menu déroulant des ateliers (en haut) -> choisir **« MCP Addon »** -> cliquer **« Start RPC Server »**. Le serveur écoute en local (port 9875). A refaire à chaque lancement de FreeCAD (avant d'ouvrir la conversation).
4. Côté **Claude Desktop** : éditer le fichier de configuration — Windows : `%APPDATA%\Claude\claude_desktop_config.json` ; macOS : `~/Library/Application Support/Claude/claude_desktop_config.json` — et y mettre : `{"mcpServers": {"freecad": {"command": "uvx", "args": ["freecad-mcp"]}}}` (si le fichier contient déjà des serveurs, ajouter seulement l'entrée `"freecad"` dans le bloc `mcpServers` existant). Redémarrer Claude Desktop : l'icône des outils doit lister « freecad ».
5. Côté **Claude Code** (terminal local) : une seule commande — `claude mcp add freecad -- uvx freecad-mcp`.
6. **Test** : demander « Ouvre un document FreeCAD et crée un tube de 50 mm de diamètre, paroi 2 mm, longueur 1 m ». Si le tube apparaît : gagné. Astuce sessions longues : l'option `only_text_feedback` du serveur coupe les captures d'écran et économise beaucoup de contexte.

## A.3 — Blender MCP (design, rendus, signature lumineuse)

1. Installer **Blender 3.0+** : blender.org.
2. Sur github.com/ahujasid/blender-mcp, télécharger le fichier `addon.py`. Dans Blender : Edit > Preferences > Add-ons > Install... > sélectionner `addon.py` > cocher **« Interface: Blender MCP »**.
3. Dans la vue 3D, ouvrir le panneau latéral (touche **N**) -> onglet **BlenderMCP** -> **Connect to Claude**.
4. Configuration client : même logique qu'en A.2.4 — entrée `"blender": {"command": "uvx", "args": ["blender-mcp"]}` dans Claude Desktop, ou `claude mcp add blender -- uvx blender-mcp` en Claude Code.
5. **Test** : « Crée une scène : tube d'acier incurvé, matériau cuivre brossé, éclairage nocturne ». Premier vrai chantier proposé : l'épine dorsale LED vue de nuit.

## A.4 — Où votre Docker sert vraiment

- **Serveur de Corée (§11.4)** : la pile télémétrie s'installe en un `docker compose up` — services `influxdb:2` (port 8086) + `grafana/grafana` (port 3000), volumes persistants, accès via votre VPN existant. Je fournirai le `docker-compose.yml` complet et provisionné à la prochaine itération (il vivra dans ce dépôt).
- **WebODM** (photogrammétrie, laptop terrain — et dépannage sur le serveur) : nativement Docker — `git clone https://github.com/OpenDroneMap/WebODM`, puis `./webodm.sh start`.
- **KiCad MCP** : au sous-jalon S5, même logique d'installation qu'en A.2.

## A.5 — Dépannage courant

- « Server disconnected » : FreeCAD/Blender doit être **ouvert** et son serveur interne **démarré** (A.2.3 / A.3.3) avant de lancer la conversation.
- `uvx` introuvable : rouvrir le terminal après l'installation de uv (rechargement du PATH).
- Pare-feu/antivirus Windows : autoriser les connexions locales (loopback) de Claude si une alerte apparaît.

# Annexe B — Lettre type sablière (à personnaliser)

Champs [entre crochets] à remplir ; envoyer d'abord aux deux exploitants locaux (§9.2), puis en version adaptée à UNICEM Nouvelle-Aquitaine. Version modifiable (.docx) fournie sur demande.

> **Objet : demande de convention d'occupation temporaire — pratique sportive électrique silencieuse**
>
> Madame, Monsieur [Nom],
>
> Résident bordelais, je développe un véhicule tout-terrain **100 % électrique** de conception française (biplace, environ une tonne), destiné à une pratique sportive sur sable exclusivement en terrain privé. Je recherche un site d'évolution régulier et me permets de vous solliciter pour une **convention d'occupation temporaire** portant sur une zone hors exploitation, ou en fin d'exploitation, de votre site de [Commune].
>
> Ce que je vous propose : un véhicule **totalement silencieux** (aucune nuisance sonore pour le voisinage, à la différence des loisirs motorisés thermiques) ; **zéro hydrocarbure** sur votre site ; une **assurance responsabilité civile dédiée** à cette pratique (attestation fournie avant tout accès) et une décharge de responsabilité établie à votre profit ; des créneaux **exclusivement à votre convenance**, hors horaires d'exploitation, sur un périmètre balisé défini ensemble ; une **indemnité d'occupation**, et — si vous disposez d'un emplacement — la **location d'une emprise pour un conteneur de stockage** (revenu récurrent pour votre exploitation) ; enfin, à votre demande, des démonstrations lors de vos événements internes ou actions RSE.
>
> Un dossier complet (présentation technique, sécurité, assurance) est à votre disposition. Je serais heureux de vous présenter le projet lors d'un rendez-vous à votre convenance.
>
> Dans l'attente de votre retour, je vous prie d'agréer, Madame, Monsieur, l'expression de mes salutations distinguées.
>
> [Prénom Nom] — [téléphone] — [mail]

# Journal des révisions

| Version | Date | Contenu |
| v0.1 | Itération 1 (chat) | Diagnostic initial : structure, masses, thermique, directions de style |
| v0.2 | 17/07/2026 | Premier PDF : design lock, 10 innovations, AR, FIA (cellule CDS), énergie/moteurs |
| v0.2.1 | 17/07/2026 | Mise en page : l'intérieur suit la couverture |
| v0.3 | 17/07/2026 | Budget 30 k -> arbitrage A/B ; nuit ; data station ; conversion < 1 j ; trajectoires ; biomimétisme ; logistique (Pilat exclu) ; MCP |
| v0.4 | 17/07/2026 | Budget re-cadré multi-année (~78-83 k, plafond 100 k) -> **twin EMRAX re-verrouillé**, mule mono-EMRAX, RDU Tesla rejeté ; pack P45B en tranches ; sourcing Chine analysé ; balisage lumineux « Forza » ; dock enceinte ; convertibilité 12 mois ; réponse chiffrée « FIA-ready = ~15 kg, non-pénalité nette » ; 3 ajouts finaux (pression pneus, VCU secours, commandes volant) puis **innovations et biomimétisme clos** ; liste sablières girondines réelles + méthode 3 canaux ; expéditions re-priorisées (Maroc encadré > UAE conteneur > Tunisie sous conditions) ; transport sans tracteur (stockage sur site) ; serveur Corée = camp numérique |
| v0.5 | 17/07/2026 | Retours propriétaire : **Maghreb rejeté, full UAE en conteneur** (seul horizon extérieur) ; piste « Gobi » consignée (construire sur place, beau-oncle au centre de loisirs — étude lointaine) ; **budget re-découpé en sous-jalons S0-S9 déclenchés par l'épargne** (S0 = 3 k : permis + bancs + sablière), rythme libre ; **permis B acté comme chemin critique** puis B96 ; **Annexe A** : guide MCP pas à pas (FreeCAD, Blender, rôle de Docker) ; **Annexe B** : lettre type sablière prête à envoyer |

# Références

- FIA — Annexe J : www.fia.com/regulation/category/100 ; code env. L.362-1 : legifrance.gouv.fr
- Sablières Gironde (annuaires publics) : kompass.com, pagesjaunes.fr ; fédération : UNICEM Nouvelle-Aquitaine ; registre carrières : DREAL NA
- UAE admission temporaire / carnet : trade.gov (country guide UAE), dubaichambers.com, atacarnet.com
- Ferries et logistique : corsicalinea.com, directferries.fr
- EMRAX : emrax.com (fiches 268) ; Molicel P45B : distributeurs UE ; u-blox ZED-F9P ; WebODM
- MCP CAO : github.com/neka-nat/freecad-mcp ; github.com/ahujasid/blender-mcp ; photogrammétrie : github.com/OpenDroneMap/WebODM
- Tous prix à re-confirmer au devis à chaque jalon.
