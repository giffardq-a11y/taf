"""Le dossier par zone/phase : données, hypothèses, fichiers sources et contradictions
relevées entre documents — la matière du schéma interactif (`tempo/schema_zones.py`).

Ce module ne calcule rien : c'est une transcription organisée de ce qui a été lu dans les
documents reçus, gardée à jour au fil des lectures. Chaque entrée porte sa source ; une
entrée sans source ne devrait pas exister ici — si un fait n'est pas encore rattaché à un
fichier précis, il vaut mieux le laisser dans `tempo/DONNEES.md` en prose que de le figer
ici sans traçabilité.

Statuts utilisés partout :
  - `confirme`    : lu directement dans un document, sans ambiguïté d'interprétation.
  - `provisoire`  : le document lui-même le présente comme non définitif (test de
                    performance à venir, brouillon, hypothèse de travail).
  - `a_trancher`  : deux sources ou plus se contredisent, ou le document dit lui-même
                    que la question est ouverte.

Personnes citées comme responsables (« à valider par ») : reprises telles que nommées
dans la réunion du 10/08/2026 ou dans les documents — Valery Claise et Joanna sont les
deux points de contact désignés pour Quentin ; Olivier Bonnot est le sponsor/coordinateur.
Pour les documents non attribués nommément (la plupart des PPTX de la seconde vague),
le responsable est noté « équipe TEMPO » faute de mieux — à corriger dès qu'on sait qui
signe quoi.

CORRECTION IMPORTANTE (10/08/2026, confirmée directement par l'utilisateur du projet) :
les codes lettre M/N/O/P/Q/R/S/T/U+K/L et A à I ne sont PAS des zones physiques fixes —
ce sont des PHASES (des repères temporels dans le gabarit tempo) pendant lesquelles
certains travaux doivent se dérouler. La feuille `Data` du classeur N3 les présentait
comme des zones physiques (« M = Panel Factory », etc.), et cette lecture a été utilisée
partout dans ce dossier jusqu'à un contrôle croisé le 10/08/2026 qui l'a mise en doute
(aucune tâche du classeur n'est jamais étiquetée UNIT=« Panel Factory ») — l'utilisateur
a ensuite confirmé directement qu'il s'agit de phases, pas de zones. Chaque entrée
`ZONES[...]` garde son ancien libellé (`aire`/`unite`, hérité de la feuille `Data`) pour
ne pas casser la continuité du schéma, mais porte désormais aussi la répartition réelle
des UNIT trouvés dans les tâches de cette phase (champ `donnees`, entrée
« Répartition réelle... ») — c'est cette répartition qui reflète ce qui s'y passe
vraiment, pas le libellé unique hérité de la feuille Data.

SUITE (11/08/2026, confirmée directement par l'utilisateur du projet) : le schéma
interactif affichait malgré tout, pour chaque zone, une seule lettre étiquetée « phase
d'origine » — régression sur la correction ci-dessus, puisqu'un élément passe en
réalité par TOUTES les phases au cours de sa construction ; il n'y a pas de phase
« d'origine » propre à une zone. Ce libellé a été retiré de l'affichage (le détail par
zone continue de lister toutes les phases où elle apparaît, via
`ZONES_PHYSIQUES_REELLES`/`ZONES_REELLES[...]['phases']`, ce qui était déjà correct).
L'utilisateur a aussi précisé le sens global de la séquence de lettres : les phases A à
J sont les phases de préparation d'armature, les phases L à U (au sens large — le même
intervalle alphabétique que M/N/O/P/Q/R/S/T/U+K/L déjà utilisé ici) couvrent le
casting/curing puis les réparations et l'outfitting. C'est cohérent avec la
« Répartition réelle » déjà calculée : les phases A à I portent en réalité des tâches
Base Slab/LASCA/Walls/Buffer (armature), les phases M à L portent des tâches Casting
Pit/R1/R2/R3 (casting/curing), avec un début de bascule vers l'outfitting (OF1) déjà
visible sur T et L. Ça confirme aussi, a contrario, que le rattachement d'OF1-OF5/SG/
UB-S9-S7 aux lettres A-I (hérité de la feuille `Data`, jamais fiable) était erroné — voir
la contradiction déjà notée sur ces zones. La correspondance précise entre lettre de
phase et zones Outfitting/Upper Basin reste ouverte (voir le registre de validation).

Autres corrections du 11/08/2026 (utilisateur) : GTA est le sous-traitant fireprotection ;
MSE (coquille pour MSI) est le sous-traitant béton de ballast ; Lyon et Brest sont des
zones DU SITE (pas des villes de départ extérieures) — un plan général du site, avec
d'autres zones du même type, doit suivre. Mécanisme outfitting précisé : les zones
N1/N2/N3 sont à l'intérieur du hall (après casting, avant que l'élément ne dépasse du
hall) ; OF1-OF5 sont les positions à l'extérieur du hall ; UB est la position après le
big push. S1 à S9 désignent des segments de l'élément (pas les lettres de phase) : le
segment S1 est poussé successivement en N1, N2, ... jusqu'à OF5 ; le segment S2 jusqu'à
OF4 seulement ; une fois en position, le big push amène l'élément à sa position finale,
jusqu'au float-up. Voir le registre de validation pour ce qui reste à établir
précisément (correspondance complète segment↔position, zones N1/N2/N3 pas encore
représentées dans le schéma).

NOUVEAU (11/08/2026, dépouillement de STE__General_Temo_Overview__DRAFT.pptx — storyboard
de 19 diapos « Tempo X & Y » plus une diapo d'organisation d'ateliers) :
  - PREUVE DIRECTE de la concurrence des deux familles de phases : chaque diapo « Tempo X
    & Y » montre un même instant où la famille M/N/O/P/Q/R/S/T/U/K/L (production/curing)
    est à la lettre X ET la famille A à I (armature, cf. plus haut) est à la lettre Y, en
    même temps — exactement ce que l'utilisateur avait indiqué dès la première demande de
    ce chantier. Séquence complète observée (19 diapos, cycle de 18 pas qui boucle — la
    diapo 20 « Tempo M & B » répète la diapo 2) : M&B, M&C, N&C, N&D, O&D, O&E, P&E, P&F,
    Q&F, Q&G, R&G, S&H, T&H, T&I, U&I (« Push 24m »), K&A (« 18m Push »), L&A (« 30m »),
    L&B, puis M&B à nouveau.
  - AFFINEMENT : U et K sont deux pas DISTINCTS d'un seul pas chacun (« U & I » puis
    « K & A »), pas un seul « U+K » fusionné comme le laissait penser le classeur N3 (qui
    les regroupe dans une seule colonne/zone R2). Le déroulé réel semble donc avoir 11
    lettres dans cette famille (M,N,O,P,Q,R,S,T,U,K,L), pas 10.
  - NOUVELLE ZONE : « Lower Basin » apparaît comme aire à part entière (en-tête de colonne
    sur chaque diapo, à gauche d'« Upper Basin ») — pas encore représentée dans ce dossier
    ni dans le schéma interactif. Position exacte dans le flux (après Upper Basin ?) à
    confirmer — voir le registre de validation.
  - CONTRADICTION À NOTER : sur ce document, les en-têtes de colonne (aires) sont, de
    gauche à droite : Lower Basin, Upper Basin, Outfitting Area, Curing Hall, Production
    Hall, Rebar Hall — et Buffer/LASCA/BS/Walls sont dessinés sous l'en-tête « Rebar Hall »,
    pas « Production Hall ». Ce dossier classe actuellement Buffer sous Production Hall
    (voir `_AIRE_PAR_ZONE_REELLE`) — à réconcilier, voir le registre de validation.
  - La diapo « WORKSHOP ORGA » liste les ateliers de détail prévus (sujet, responsable en
    initiales, semaine, équipes impliquées) — voir `ATELIERS_DETAIL` ci-dessous.
"""

ZONES = {
    'M': {
        'aire': 'Panel Factory',
        'unite': 'Panel Factory',
        'donnees': [
            {'texte': "Sous-traitants relevés dans les tâches N3 : CEAS, Impostal, MSE, "
                      "JD Steel, WL, BL.", 'source': 'STE__TEMPO__N3_Takt_Plan__V0_1.xlsx (feuilles CP__M)',
             'statut': 'confirme'},
            {'texte': "JD Steel n'apparaît que dans cette zone, nulle part ailleurs dans le N3.",
             'source': 'STE__TEMPO__N3_Takt_Plan__V0_1.xlsx', 'statut': 'confirme'},
        ],
        'hypotheses': [],
        'contradictions': [],
        'fichiers': ['STE__TEMPO__N3_Takt_Plan__V0_1.xlsx'],
    },
    'N': {
        'aire': 'Rebar Hall', 'unite': 'Walls',
        'donnees': [
            {'texte': "6 ouvriers, organisés en 4 équipes de 3 décalées dans le temps, "
                      "recouvrement jusqu'à 12h.", 'source': "réunion TEMPO Rebar & Logistic (10/08/2026) "
                      "+ TEMPO_N2_Presentation_Rebar_04062026.pptx", 'statut': 'confirme'},
            {'texte': "Nombre de camions par mur (A à F) et par segment (S1-S9), ex. mur B : "
                      "4,3,4,3,3,3,4,3,4 sur S1→S9.",
             'source': 'Truck_for_All_Set__V2.xlsx (feuille WALL + RACK)', 'statut': 'confirme'},
            {'texte': "Ordre d'installation des murs : B, C, D, E, A, F — écrit deux fois de façon "
                      "identique dans le même document (une fois comme « Sequence of walls », une "
                      "fois comme « Installation of walls »), plus fiable que la version « B-C-A-D-E-F »"
                      " entendue en réunion (transcription automatique très bruitée à cet endroit).",
             'source': 'General_Tempo_Staggering_MDI_V5.xlsm (feuille Data base, lignes 19 et 70)',
             'statut': 'confirme'},
            {'texte': "2 à 4 camions par mur ; livraison des murs dans le poste précédant la "
                      "production, zone de livraison libre.",
             'source': 'General_Tempo_Staggering_MDI_V5.xlsm (feuille Data base, lignes 17-18)',
             'statut': 'provisoire'},
        ],
        'hypotheses': [
            {'texte': "« Saturday and Sunday off (Expect some for the Wall) » — le document "
                      "d'hypothèses lui-même prévoit une exception week-end pour les murs, et note "
                      "ailleurs : « Work on full Saturday to ensure the walls fabrication... Test to "
                      "be done » — confirme, à la source, la tension déjà relevée par ailleurs sur "
                      "le travail du week-end (voir REGISTRE_VALIDATION), sans la trancher "
                      "elle-même (« test à faire »).",
             'source': 'General_Tempo_Staggering_MDI_V5.xlsm (feuille Data base, lignes 8 et 30)',
             'a_valider_par': 'équipe TEMPO (arbitrage global)', 'statut': 'a_trancher'},
        ],
        'contradictions': [
            {'texte': "Segments N3 sans détail : notre lecture trouve S4 et S5 manquants ; le "
                      "suivi officiel « N3 Overview (Missing) » indique S1/S3/S5/S7/S9 manquants "
                      "(les segments impairs). Les deux ne se recoupent que sur S5.",
             'sources': ['STE__TEMPO__N3_Takt_Plan__V0_1.xlsx (calculé, tempo/comparer_n1_n3.py)',
                          'Comparison_N1_shifts_to_target.xlsx (feuille N3 Overview (Missing))']},
        ],
        'fichiers': ['STE__TEMPO__N3_Takt_Plan__V0_1.xlsx', 'TEMPO_N2_Presentation_Rebar_04062026.pptx',
                     'Truck_for_All_Set__V2.xlsx', 'Comparison_N1_shifts_to_target.xlsx',
                     'General_Tempo_Staggering_MDI_V5.xlsm',
                     'Tempo_Walls.xlsx (non encore dépouillé en détail)'],
    },
    'O': {
        'aire': 'Rebar Hall', 'unite': 'Base Slab',
        'donnees': [
            {'texte': "8 ouvriers en continu.", 'source': "réunion TEMPO (10/08/2026) + "
                      "TEMPO_N2_Presentation_Rebar_04062026.pptx", 'statut': 'confirme'},
            {'texte': "1,5 grue affectée.", 'source': 'TEMPO_N2_Presentation_Rebar_04062026.pptx',
             'statut': 'confirme'},
            {'texte': "Ratio productivité cité en exemple : de l'ordre de 3 tonnes/heure pour "
                      "8 personnes — présenté comme un point de départ à valider par tests de "
                      "performance, pas un chiffre arrêté.",
             'source': 'réunion TEMPO (10/08/2026)', 'statut': 'provisoire'},
            {'texte': "Confirmation indépendante des effectifs et grues : « Manpower : 8 BS - 8 TS "
                      "- 6 WALLS » et « Crane : 1+1/2 BS - 1 special crane for walls - 2 cranes for "
                      "TS » — cohérent avec les 8 ouvriers / 1,5 grue déjà cités pour Base Slab, et "
                      "apporte deux chiffres nouveaux (Top Slab : 8 ouvriers, 2 grues) qui "
                      "n'avaient pas de source dédiée jusqu'ici.",
             'source': 'General_Tempo_Staggering_MDI_V5.xlsm (feuille Data base, lignes 9-10)',
             'statut': 'confirme'},
            {'texte': "Détail par sous-lot (SET) pour Base Slab (BS0=3 ouvriers, BS1 à BS4=8 "
                      "ouvriers chacun) et pour Top Slab (TS1 à TS4=8 ouvriers chacun) — BS0 étant "
                      "vraisemblablement une phase de préparation plus légère avant le gros du "
                      "ferraillage.", 'source': 'General_Tempo_Staggering_MDI_V5.xlsm (feuille '
                      'Data base, lignes 41-45 et 61-64)', 'statut': 'confirme'},
            {'texte': "Plafond de grues simultanées, toutes zones : pas plus de 2 grues pour un "
                      "top slab, pas plus de 1 pour un mur, pas plus de 3 pour deux base slabs "
                      "dans la même halle — règle de méthode pour remplir les fichiers takt time, "
                      "cohérente avec les chiffres ci-dessus.",
             'source': 'Explanations_Takt_time_files.pptx', 'statut': 'confirme'},
        ],
        'hypotheses': [
            {'texte': "Hypothèses incluses dans le takt time Base Slab S1-S9 : 2h pour remonter "
                      "les jigs + installation des shoes + nettoyage ; 8 ouvriers ; 1 ou 2 grues ; "
                      "démarrage de l'activité à la fin du skidding ; géomètre, coffrage et qualité "
                      "non inclus (pas de coactivité prévue hors skidding).",
             'source': 'General_Tempo_Staggering_MDI_V5.xlsm (feuille HYPOTHESE PL)',
             'a_valider_par': 'Valery Claise / Joanna', 'statut': 'provisoire'},
            {'texte': "Opportunité écartée du takt time actuel : amener les longitudinaux par "
                      "convoyeur (limité par la grue et la place de stockage) — non testé car pas "
                      "prêt.", 'source': 'General_Tempo_Staggering_MDI_V5.xlsm (feuille HYPOTHESE PL)',
             'statut': 'provisoire'},
        ],
        'contradictions': [
            {'texte': "Segments N3 sans détail : notre lecture trouve S5-S8 manquants ; le suivi "
                      "officiel indique BS complet sur tous les segments. Désaccord total.",
             'sources': ['STE__TEMPO__N3_Takt_Plan__V0_1.xlsx (calculé, tempo/comparer_n1_n3.py)',
                          'Comparison_N1_shifts_to_target.xlsx (feuille N3 Overview (Missing))']},
        ],
        'fichiers': ['STE__TEMPO__N3_Takt_Plan__V0_1.xlsx', 'TEMPO_N2_Presentation_Rebar_04062026.pptx',
                     'Comparison_N1_shifts_to_target.xlsx', 'General_Tempo_Staggering_MDI_V5.xlsm',
                     'Tempo_Bottomslabs.xlsx / Tempo_Bottomslabs_LCA_rev2.xlsx (non encore dépouillés '
                     'en détail — ce sont les séquences takt time source des feuilles N3, sheet '
                     'par sheet par segment/paire de segments)'],
    },
    'P': {
        'aire': 'Rebar Hall', 'unite': 'LASCA',
        'donnees': [
            {'texte': "LASCA = zone de la chaîne d'assemblage du ferraillage (confirmé directement "
                      "par l'utilisateur du projet).", 'source': 'confirmation directe', 'statut': 'confirme'},
        ],
        'hypotheses': [
            {'texte': "Hypothèses incluses dans le takt time LASCA : montage des échafaudages "
                      "1/2 poste après le skidding ; pose des rails pendant le montage des murs ; "
                      "après skidding, 1 poste pour BO S1/S9 et niches ; assemblage démarre quand "
                      "LASCA est prête et le skidding terminé ; pas de stockage sur LASCA (convoyeur "
                      "ou LASCA centrale) pendant le skidding ; cadre ESS livré par convoyeur.",
             'source': 'General_Tempo_Staggering_MDI_V5.xlsm (feuille HYPOTHESE PL)',
             'a_valider_par': 'Valery Claise / Joanna', 'statut': 'provisoire'},
            {'texte': "Opportunités écartées du takt time actuel : stockage en plateforme centrale "
                      "LASCA ; levage des murs avec BO ou installation du BO en Buffer.",
             'source': 'General_Tempo_Staggering_MDI_V5.xlsm (feuille HYPOTHESE PL)', 'statut': 'provisoire'},
        ],
        'contradictions': [
            {'texte': "Segments N3 sans détail trouvés : S6, S7, S8 — pas encore comparés au "
                      "suivi officiel (qui ne couvre que BS/W/TS, pas LASCA nommément).",
             'sources': ['STE__TEMPO__N3_Takt_Plan__V0_1.xlsx (calculé, tempo/comparer_n1_n3.py)']},
        ],
        'fichiers': ['STE__TEMPO__N3_Takt_Plan__V0_1.xlsx', 'General_Tempo_Staggering_MDI_V5.xlsm'],
    },
    'Q': {
        'aire': 'Production Hall', 'unite': 'Buffer',
        'donnees': [
            {'texte': "« Biggest issue for S9 and shear keys, formworkers has no time to do it if "
                      "1 shift » — signalé comme un point dur, pas résolu dans le document.",
             'source': 'TEMPO_N2_presentation_CAS__BUF___May_26.pptx', 'statut': 'a_trancher'},
        ],
        'hypotheses': [],
        'contradictions': [],
        'fichiers': ['STE__TEMPO__N3_Takt_Plan__V0_1.xlsx', 'TEMPO_N2_presentation_CAS__BUF___May_26.pptx'],
    },
    'R': {
        'aire': 'Production Hall', 'unite': 'P/U Point',
        'donnees': [],
        'hypotheses': [],
        'contradictions': [],
        'fichiers': ['STE__TEMPO__N3_Takt_Plan__V0_1.xlsx'],
    },
    'S': {
        'aire': 'Production Hall', 'unite': 'Casting Pit',
        'donnees': [
            {'texte': "Coulée de 30h, avec 2h de recouvrement entre deux coulées sur la même "
                      "centrale (32h envisagées dans certaines options de calage).",
             'source': 'General_Tempo_Staggering.xlsx (feuille Casting Pattern)', 'statut': 'confirme'},
            {'texte': "6 centrales à béton (A1/A2/A3, B4/B5/B6) — B6 n'existe pas encore.",
             'source': 'General_Tempo_Staggering.xlsx (feuille Casting Pattern)', 'statut': 'confirme'},
            {'texte': "Effectif équipe de coulée : 70 BC (statut actuel) contre 85 BC convenu "
                      "précédemment — écart non expliqué dans le document.",
             'source': 'TEMPO_N2_Presentation_Casting_Team_10062026.pptx', 'statut': 'a_trancher'},
            {'texte': "Pic de manpower : 105 BC en pic standard, 117 BC en pic extrême (segment "
                      "S5, 3 fois par cycle).", 'source': 'TEMPO_N2_Presentation_Casting_Team_10062026.pptx',
             'statut': 'confirme'},
            {'texte': "Réduction envisagée de 5 à 4 ouvriers par boom de coulée — risque qualité "
                      "explicitement noté par l'équipe elle-même (moins de vibration, couches plus "
                      "grosses).", 'source': 'TEMPO_N2_Presentation_Casting_Team_10062026.pptx',
             'statut': 'provisoire'},
            {'texte': "9+1 semaines de cycle (9 normales + 1 tampon/fantôme).",
             'source': 'TEMPO_N2_Presentation_Casting_Team_10062026.pptx', 'statut': 'confirme'},
            {'texte': "Ratio grue/durée calculé segment par segment (ex. BS S1 : durée 115 pour "
                      "12h47 de « Shift » ; BS S2 : durée 86 pour 9h33) — dans les deux cas, durée ÷ "
                      "9 = nombre d'heures de poste affiché. La feuille est donc construite sur "
                      "l'hypothèse d'un poste de 9h, comme la présentation Rebar — un deuxième "
                      "document pointe vers 9h, contre un seul chacun pour 10h/8h/12h.",
             'source': 'Cranes_conclusions.xlsx (feuilles Crane Time N1 et N2)', 'statut': 'provisoire'},
        ],
        'hypotheses': [
            {'texte': "Système de postes de l'équipe de coulée non décidé : 3×8h ou 2×12h "
                      "(« No shift system in place »). Conditionne toute la grille horaire du "
                      "moteur de simulation.", 'a_valider_par': 'équipe Casting Team',
             'statut': 'a_trancher'},
            {'texte': "Durée réelle de coulée en révision : comptée pour 24h mais insuffisante une "
                      "fois les dimanches réintégrés (S2→S8 : ~27h manquantes ; S8→S9 et S1→S2 : "
                      "~51h manquantes). Étude en cours pour repasser à 19,5h.",
             'a_valider_par': 'équipe CAS/Buffer (JSO)', 'statut': 'a_trancher'},
        ],
        'contradictions': [
            {'texte': "Le moteur de simulation (tempo/moteur/goulots.py), sur la ressource BC en "
                      "zone S seule, trouve désormais un pic de 95 personnes simultanées — proche "
                      "des 105-117 cités par l'équipe Casting Team (écart de 10-20%, plus le facteur "
                      "2 précédemment observé). Ce chiffre de 95 ne reproduit toutefois pas le 228 "
                      "trouvé par une version antérieure du moteur sur les mêmes fichiers source, "
                      "sans cause identifiée (différence de version de fichier ou d'horizon simulé "
                      "probable, pas une correction volontaire) — les deux valeurs (95 et l'ancien "
                      "228) restent donc à réconcilier avec l'équipe Casting Team. Voir aussi le "
                      "total tous zones confondues (1258, incomparable à 105-117 car il additionne "
                      "tous les éléments simultanément en cours sur tout leur parcours) — détail "
                      "dans tempo/moteur/ARCHITECTURE.md.",
             'sources': ['tempo/moteur/goulots.py (calculé)', 'TEMPO_N2_Presentation_Casting_Team_10062026.pptx']},
            {'texte': "Segments N3 sans détail trouvés : seul S9 — pas comparé au suivi officiel.",
             'sources': ['STE__TEMPO__N3_Takt_Plan__V0_1.xlsx (calculé)']},
        ],
        'fichiers': ['General_Tempo_Staggering.xlsx', 'STE__TEMPO__N3_Takt_Plan__V0_1.xlsx',
                     'TEMPO_N2_Presentation_Casting_Team_10062026.pptx',
                     'TEMPO_N2_presentation_CAS__BUF___May_26.pptx',
                     'Tempo_full_schedule_linked_V4_70_jour.mpp', 'Cranes_conclusions.xlsx'],
    },
    'T': {'aire': 'Curing Hall', 'unite': 'R1',
          'donnees': [
              {'texte': "Le planning MS Project confirme, pour chacun des 9 segments d'un élément "
                        "(« TE 01 »), une paire de tâches « Casting » (≈1,5 jour, ressource FLC "
                        "WORKER) suivie de « Pushing » (≈0,35 jour soit ~8h, ressource Skidding "
                        "team) — le « push » qui fait avancer l'élément d'une position à l'autre "
                        "dans la ligne de coulée. C'est la mécanique concrète derrière le skidding "
                        "déjà évoqué en zone S.", 'source': 'Tempo_full_schedule_linked_V4_70_jour.mpp '
                        '(tâches Casting/Pushing TE 01 -Segment 01 à 09)', 'statut': 'confirme'},
              {'texte': "L'équipe logistique identifiée dans le classeur N3 lui-même est "
                        "« Skidding » (ressource dédiée, ~44 lignes de charge) — trouvée "
                        "presque exclusivement dans les phases T, U+K et L (R1/R2/R3), "
                        "rattachée aux tâches UNIT=Casting Pit et P/U Point qui s'y trouvent. "
                        "C'est la même équipe que le « Skidding team » du planning MPP "
                        "(Casting/Pushing, Big Push) — la logistique de déplacement des "
                        "éléments d'une position à l'autre, pas la logistique amont "
                        "(camions/livraisons, voir LOGISTIQUE).",
               'source': 'STE__TEMPO__N3_Takt_Plan__V0_1.xlsx (calculé, colonne ressource) + '
                         'Tempo_full_schedule_linked_V4_70_jour.mpp', 'statut': 'confirme'},
          ], 'hypotheses': [], 'contradictions': [],
          'fichiers': ['STE__TEMPO__N3_Takt_Plan__V0_1.xlsx', 'Tempo_full_schedule_linked_V4_70_jour.mpp']},
    'U+K': {'aire': 'Curing Hall', 'unite': 'R2', 'donnees': [], 'hypotheses': [], 'contradictions': [],
             'fichiers': ['STE__TEMPO__N3_Takt_Plan__V0_1.xlsx']},
    'L': {'aire': 'Curing Hall', 'unite': 'R3', 'donnees': [], 'hypotheses': [], 'contradictions': [],
          'fichiers': ['STE__TEMPO__N3_Takt_Plan__V0_1.xlsx']},
}

# Zones A-F (Outfitting) et G-I (Upper Basin) : le classeur N3 ne les détaille pas (statut
# de brouillon V0.1), mais le planning MS Project de l'outfitting (`tempo/lire_mpp.py`) est
# précisément le document qui couvre cette partie — 631 tâches pour un seul élément (« TE 01 »),
# organisées par segment (S1 à S9) plutôt que par code de zone OF1-OF5/SG ou UB-S9/S8/S7. Les
# deux découpages (zones N3/N1 vs segments MPP) ne sont pas encore mis en correspondance —
# voir l'hypothèse ci-dessous plutôt qu'une contradiction : ce n'est pas un vrai trou de donnée,
# c'est un système de repérage différent à faire concorder.
_DONNEES_OUTFITTING_MPP = [
    {'texte': "Le planning MS Project de l'outfitting détaille, par segment (S1 à S9) et par "
              "élément (« TE 01 »), un volume important de tâches : réparations de fissures et "
              "reprises béton (int./ext.), protection incendie, scellement des joints (« ALL "
              "tubes patching », injection waterstop), réseaux électriques et câblage, éclairage, "
              "protection cathodique, système de réalignement, GINA, et post-tension (voir "
              "ci-dessous) — 631 tâches au total pour un seul élément.",
     'source': 'Tempo_full_schedule_linked_V4_70_jour.mpp', 'statut': 'confirme'},
    {'texte': "Mécanisme précisé (11/08/2026) : les zones N1/N2/N3 sont à l'intérieur du hall "
              "(après casting, avant que l'élément ne dépasse du hall) ; OF1-OF5 sont les "
              "positions à l'extérieur du hall ; UB est la position après le big push. S1 à S9 "
              "désignent des segments de l'élément produit (pas des zones ni des lettres de "
              "phase) : une fois produit, le segment S1 est poussé successivement en N1, puis N2, "
              "et ainsi de suite jusqu'à OF5 ; le segment S2 suit le même chemin mais s'arrête à "
              "OF4. Une fois en position, l'élément complet fait le big push vers sa position "
              "finale, jusqu'au float-up.",
     'source': "confirmé directement par l'utilisateur du projet (11/08/2026)", 'statut': 'confirme'},
]
_HYPOTHESE_MAPPING_MPP = {
    'texte': "Le mécanisme général (voir Données ci-dessus) est confirmé, mais la correspondance "
             "complète reste à établir : combien de positions N1/N2/(N3 ?) existent réellement, "
             "quel segment (S1 à S9) termine dans quelle case OF1-OF5/SG précise, et où les zones "
             "N1/N2/N3 elles-mêmes doivent apparaître dans ce schéma (elles n'y figurent pas "
             "encore — seules OF1-OF5/SG et UB-S9/S8/S7 y sont représentées). Un plan général du "
             "site, annoncé par l'utilisateur, doit aider à trancher.",
    'a_valider_par': 'Valery Claise / Joanna', 'statut': 'a_trancher',
}

for _z in ['A', 'B', 'C', 'D', 'E', 'F']:
    ZONES[_z] = {
        'aire': 'Outfitting Area', 'unite': {'A': 'OF1', 'B': 'OF2', 'C': 'OF3', 'D': 'OF4', 'E': 'OF5', 'F': 'SG'}[_z],
        'donnees': list(_DONNEES_OUTFITTING_MPP), 'hypotheses': [dict(_HYPOTHESE_MAPPING_MPP)],
        'contradictions': [{'texte': "Corrigé le 10/08/2026 — cette phase N'EST PAS vide dans le "
                             "classeur N3 (elle porte 85 à 94 tâches réelles, voir la répartition "
                             "réelle en Données) : l'ancienne affirmation « aucune tâche détaillée » "
                             "reposait sur la lecture erronée de cette lettre comme zone Outfitting "
                             "Area/OF1-OF5. En réalité ses tâches sont majoritairement rattachées à "
                             "Base Slab/LASCA/Walls/Buffer, pas à l'Outfitting. Éclairci le "
                             "11/08/2026 : ce n'est pas un trou de donnée, c'est cohérent — les "
                             "phases A à I sont en réalité des phases de préparation d'armature "
                             "(confirmé par l'utilisateur), donc le rattachement de cette lettre à "
                             "une case OF1-OF5/SG (hérité de la feuille Data, jamais fiable) était "
                             "simplement erroné. La correspondance avec le planning MPP outfitting "
                             "reste néanmoins à établir précisément (voir l'hypothèse).",
                             'sources': ['STE__TEMPO__N3_Takt_Plan__V0_1.xlsx (calculé, 10/08/2026)',
                                         "confirmé directement par l'utilisateur du projet (11/08/2026)"]}],
        'fichiers': ['STE__TEMPO__N3_Takt_Plan__V0_1.xlsx', 'Tempo_full_schedule_linked_V4_70_jour.mpp'],
    }
_DONNEES_UPPER_BASIN_MPP = [
    {'texte': "« Big Push » = le nom donné dans le planning au mouvement de l'élément complet "
              "vers l'Upper Basin (tâches « TE 01 - Big Push Start » puis « TE 01 Movement to "
              "Upper Basin (Start of Big Push) », toutes deux portées par la Skidding team, à un "
              "jour d'écart dans cette version V4 du planning). C'est un jalon, pas une tâche "
              "durée — l'élément termine tout son outfitting (voir zones A-F) avant ce mouvement.",
     'source': 'Tempo_full_schedule_linked_V4_70_jour.mpp', 'statut': 'confirme'},
    {'texte': "La post-tension (« PT Threading » 3,25j, « PT Stressing » 3,25j, « PT Grout » "
              "2,5j, ressource Dywidag) est planifiée après le Big Push dans cette version V4 du "
              "planning — ce qui situerait cette opération en Upper Basin plutôt qu'en amont, "
              "mais ce n'est déduit que de l'ordre chronologique des tâches, pas d'une "
              "affectation de zone explicite dans le fichier.",
     'source': 'Tempo_full_schedule_linked_V4_70_jour.mpp', 'statut': 'provisoire'},
    {'texte': "La fin de séquence de l'élément dans le planning couvre aussi : fermeture de la "
              "porte coulissante (« Close Sliding Gate »), test de la GINA et du système de "
              "réalignement, essai des ballasts (« Ballast Tank Water Test »), puis flottaison "
              "(« Float-up », « Float-Down », « Floating Gate closure ») — cohérent avec l'Upper "
              "Basin comme zone de mise à l'eau, mais la correspondance avec les codes UB-S9/S8/"
              "S7 spécifiquement n'est pas faite (voir hypothèse).",
     'source': 'Tempo_full_schedule_linked_V4_70_jour.mpp', 'statut': 'confirme'},
]

for _z, _u in [('G', 'UB-S9'), ('H', 'UB-S8'), ('I', 'UB-S7')]:
    ZONES[_z] = {
        'aire': 'Upper Basin', 'unite': _u,
        'donnees': list(_DONNEES_UPPER_BASIN_MPP), 'hypotheses': [dict(_HYPOTHESE_MAPPING_MPP)],
        'contradictions': [{'texte': "Corrigé le 10/08/2026 — cette phase N'EST PAS vide dans le "
                             "classeur N3 (50 à 87 tâches réelles, voir la répartition réelle en "
                             "Données), contrairement à l'ancienne affirmation « aucune tâche "
                             "détaillée » qui reposait sur la lecture erronée de cette lettre comme "
                             "zone Upper Basin/UB-S9-S7. Ses tâches sont en réalité majoritairement "
                             "rattachées à LASCA/Base Slab/Walls, pas à l'Upper Basin. Éclairci le "
                             "11/08/2026 : cohérent avec le fait que les phases A à I couvrent en "
                             "réalité la préparation d'armature (confirmé par l'utilisateur), donc "
                             "le rattachement de cette lettre à une case UB-S9/S8/S7 (hérité de la "
                             "feuille Data, jamais fiable) était erroné. La correspondance avec le "
                             "planning MPP outfitting (Big Push, post-tension, flottaison — Données "
                             "ci-dessus) reste néanmoins à établir précisément (voir l'hypothèse).",
                             'sources': ['STE__TEMPO__N3_Takt_Plan__V0_1.xlsx (calculé, 10/08/2026)',
                                         "confirmé directement par l'utilisateur du projet (11/08/2026)"]}],
        'fichiers': ['STE__TEMPO__N3_Takt_Plan__V0_1.xlsx', 'Tempo_full_schedule_linked_V4_70_jour.mpp'],
    }

# Répartition réelle des UNIT trouvés dans les tâches de chaque phase (calculée le
# 10/08/2026, cf. la correction en tête de module) — {phase: [(unite, pourcentage), ...]},
# les 3-4 valeurs les plus fréquentes, sur le total des tâches de cette phase dans le
# classeur N3. C'est ce qui remplace, en fiable, l'ancien libellé unique hérité de la
# feuille Data (« M = Panel Factory », etc.), qui ne correspond à aucune tâche réelle.
_REPARTITION_REELLE_UNIT = {
    'M': [('Casting Pit', 48), ('NC (non renseigné)', 14), ('R1', 12), ('UB-S9', 11)],
    'N': [('Casting Pit', 44), ('R2', 20), ('R1', 11), ('UB-S9', 9)],
    'O': [('Casting Pit', 39), ('NC (non renseigné)', 15), ('UB-S9', 11), ('R2', 11)],
    'P': [('Casting Pit', 45), ('NC (non renseigné)', 13), ('R2', 13), ('R1', 10)],
    'Q': [('Casting Pit', 49), ('NC (non renseigné)', 15), ('R1', 12), ('R2', 12)],
    'R': [('Casting Pit', 48), ('R2', 16), ('NC (non renseigné)', 12), ('R1', 11)],
    'S': [('Casting Pit', 51), ('R1', 12), ('R2', 11), ('NC (non renseigné)', 10)],
    'T': [('Casting Pit', 57), ('R2', 13), ('R1', 12), ('OF1', 5)],
    'U+K': [('Casting Pit', 29), ('R2', 25), ('R1', 15), ('NC (non renseigné)', 14)],
    'L': [('Casting Pit', 57), ('R3', 21), ('NC (non renseigné)', 7), ('OF1', 6)],
    'A': [('Base Slab', 38), ('LASCA', 36), ('Walls', 14), ('Buffer', 12)],
    'B': [('LASCA', 39), ('Base Slab', 33), ('Walls', 15), ('Buffer', 14)],
    'C': [('LASCA', 43), ('Base Slab', 31), ('Walls', 14), ('Buffer', 12)],
    'D': [('LASCA', 40), ('Base Slab', 34), ('Walls', 15), ('Buffer', 11)],
    'E': [('LASCA', 39), ('Base Slab', 33), ('Walls', 15), ('Buffer', 13)],
    'F': [('LASCA', 39), ('Base Slab', 33), ('Walls', 15), ('Buffer', 13)],
    'G': [('LASCA', 36), ('Base Slab', 26), ('Walls', 26), ('Buffer', 12)],
    'H': [('LASCA', 40), ('Base Slab', 34), ('Walls', 15), ('Buffer', 12)],
    'I': [('LASCA', 39), ('Base Slab', 33), ('Walls', 15), ('Buffer', 13)],
}
for _z, _repartition in _REPARTITION_REELLE_UNIT.items():
    _texte_repartition = ", ".join(f"{u} {p}%" for u, p in _repartition)
    ZONES[_z]['donnees'].insert(0, {
        'texte': f"Répartition réelle des UNIT trouvés dans les tâches de la phase {_z} "
                 f"(sur le total des tâches qui y sont rattachées) : {_texte_repartition}. "
                 f"C'est l'attribut fiable pour savoir ce qui s'y passe physiquement — pas "
                 f"le libellé unique « {ZONES[_z]['unite']} » hérité de la feuille Data du "
                 f"classeur, qui ne correspond à aucune tâche réelle de cette phase.",
        'source': 'STE__TEMPO__N3_Takt_Plan__V0_1.xlsx (calculé, toutes tâches de la phase, '
                   '10/08/2026)', 'statut': 'confirme',
    })

# Vue inverse de _REPARTITION_REELLE_UNIT : pour chaque zone physique réelle (colonne
# UNIT), la liste des phases (lettres) où ses tâches apparaissent dans le classeur N3,
# avec le nombre de tâches par phase — confirme directement ce que l'utilisateur a
# précisé le 10/08/2026 : une zone physique peut être travaillée sur plusieurs phases
# (plusieurs lettres), ce n'est pas une correspondance 1 lettre = 1 zone.
ZONES_PHYSIQUES_REELLES = {
    'Casting Pit': {'total': 1184, 'phases': [('L', 162), ('T', 153), ('M', 125), ('N', 123),
                     ('P', 122), ('S', 120), ('R', 118), ('O', 114), ('Q', 114), ('U+K', 33)]},
    'LASCA': {'total': 296, 'phases': [('C', 40), ('A', 34), ('B', 34), ('D', 34), ('E', 34),
               ('F', 34), ('H', 34), ('I', 34), ('G', 18)]},
    'R2': {'total': 279, 'phases': [('N', 56), ('R', 39), ('P', 34), ('T', 34), ('O', 33),
            ('U+K', 29), ('Q', 27), ('S', 27)]},
    'Base Slab': {'total': 252, 'phases': [('A', 36), ('B', 29), ('C', 29), ('D', 29), ('E', 29),
                   ('F', 29), ('H', 29), ('I', 29), ('G', 13)]},
    'R1': {'total': 252, 'phases': [('T', 32), ('N', 32), ('M', 30), ('O', 29), ('Q', 28),
            ('S', 28), ('P', 26), ('R', 26), ('U+K', 17), ('L', 4)]},
    'R3': {'total': 140, 'phases': [('L', 59), ('O', 28), ('S', 11), ('Q', 10), ('T', 10),
            ('P', 9), ('R', 8), ('U+K', 5)]},
    'Walls': {'total': 117, 'phases': [('A', 13), ('B', 13), ('C', 13), ('D', 13), ('E', 13),
               ('F', 13), ('G', 13), ('H', 13), ('I', 13)]},
    'UB-S9': {'total': 110, 'phases': [('O', 33), ('M', 28), ('N', 24), ('P', 23), ('U+K', 1), ('R', 1)]},
    'Buffer': {'total': 99, 'phases': [('B', 12), ('A', 11), ('C', 11), ('E', 11), ('F', 11),
                ('I', 11), ('H', 10), ('D', 9), ('G', 6), ('M', 1), ('N', 1), ('O', 1), ('P', 1),
                ('Q', 1), ('R', 1), ('S', 1)]},
    'OF1': {'total': 75, 'phases': [('L', 17), ('S', 14), ('T', 13), ('P', 11), ('R', 8),
             ('Q', 7), ('U+K', 5)]},
    'P/U Point': {'total': 59, 'phases': [('Q', 9), ('M', 8), ('N', 8), ('O', 8), ('S', 8),
                   ('P', 7), ('R', 7), ('U+K', 3), ('T', 1)]},
    'UB-S1': {'total': 42, 'phases': [('M', 20), ('N', 15), ('O', 4), ('P', 2), ('R', 1)]},
    'OF2': {'total': 15, 'phases': [('T', 5), ('L', 5), ('U+K', 3), ('Q', 2)]},
    'OF3': {'total': 13, 'phases': [('R', 7), ('L', 6)]},
    'SG': {'total': 13, 'phases': [('L', 7), ('M', 3), ('U+K', 3)]},
    'UB': {'total': 10, 'phases': [('M', 4), ('N', 3), ('T', 3)]},
    'Curing Area': {'total': 7, 'phases': [('M', 1), ('N', 1), ('O', 1), ('P', 1), ('Q', 1),
                     ('R', 1), ('S', 1)]},
    'OF4': {'total': 6, 'phases': [('S', 4), ('R', 1), ('L', 1)]},
    'OF5': {'total': 5, 'phases': [('T', 5)]},
    'UB-S6': {'total': 2, 'phases': [('M', 1), ('N', 1)]},
    'South Platform': {'total': 1, 'phases': [('M', 1)]},
    'Panel Factory': {'total': 0, 'phases': []},  # déclarée par la feuille Data pour M, mais
                                                    # aucune tâche du classeur n'y est jamais
                                                    # rattachée — voir le point critique du registre.
}

# ZONES_REELLES : vue « zone physique d'abord », demandée par l'utilisateur le 10/08/2026
# après la clarification phase/zone — c'est la structure qui alimente désormais le schéma
# interactif en priorité (cliquer sur une zone -> détail par phase), ZONES (phase par
# phase) restant disponible pour la traçabilité de comment chaque donnée a été lue.
#
# Reprend le contenu de ZONES[lettre] tel quel (données/hypothèses/contradictions/
# fichiers) sous la clé du nom de zone réel que la feuille Data déclarait pour cette
# lettre — légitime pour le contenu qualitatif (les présentations Rebar/Casting Team
# parlent bien de Murs/Coulée, quelle que soit la lettre sous laquelle on les avait
# classées), pas pour la répartition de tâches N3 par lettre (remplacée ici par
# ZONES_PHYSIQUES_REELLES, la seule source fiable pour « combien de tâches, sur quelles
# phases »).
_LETTRE_VERS_ZONE_REELLE = {
    'M': 'Panel Factory', 'N': 'Walls', 'O': 'Base Slab', 'P': 'LASCA', 'Q': 'Buffer',
    'R': 'P/U Point', 'S': 'Casting Pit', 'T': 'R1', 'U+K': 'R2', 'L': 'R3',
    'A': 'OF1', 'B': 'OF2', 'C': 'OF3', 'D': 'OF4', 'E': 'OF5', 'F': 'SG',
    'G': 'UB-S9', 'H': 'UB-S8', 'I': 'UB-S7',
}
_AIRE_PAR_ZONE_REELLE = {
    'Panel Factory': 'Panel Factory',
    'Walls': 'Rebar Hall', 'Base Slab': 'Rebar Hall', 'LASCA': 'Rebar Hall',
    'Buffer': 'Production Hall', 'P/U Point': 'Production Hall', 'Casting Pit': 'Production Hall',
    'R1': 'Curing Hall', 'R2': 'Curing Hall', 'R3': 'Curing Hall',
    'OF1': 'Outfitting Area', 'OF2': 'Outfitting Area', 'OF3': 'Outfitting Area',
    'OF4': 'Outfitting Area', 'OF5': 'Outfitting Area', 'SG': 'Outfitting Area',
    'UB-S9': 'Upper Basin', 'UB-S8': 'Upper Basin', 'UB-S7': 'Upper Basin',
}

ZONES_REELLES = {}
for _lettre, _nom in _LETTRE_VERS_ZONE_REELLE.items():
    _source = ZONES[_lettre]
    _infos_taches = ZONES_PHYSIQUES_REELLES.get(_nom, {'total': 0, 'phases': []})
    ZONES_REELLES[_nom] = {
        'aire': _AIRE_PAR_ZONE_REELLE[_nom],
        'lettre_origine': _lettre,
        'phases': _infos_taches['phases'],
        'total_taches': _infos_taches['total'],
        'donnees': [d for d in _source['donnees']
                    if not d['texte'].startswith('Répartition réelle des UNIT')],
        'hypotheses': list(_source['hypotheses']),
        'contradictions': list(_source['contradictions']),
        'fichiers': list(_source['fichiers']),
    }

LOGISTIQUE = {
    'nom': 'Logistique amont — approvisionnement → stock (zones du site, dont Lyon/Brest) → halls',
    'donnees': [
        {'texte': "35 345 colis référencés sur 84 éléments, avec poids, fournisseur et date de "
                  "livraison.", 'source': 'MASTERVIEW.xlsm (feuille ALL ELEMENTS)', 'statut': 'confirme'},
        {'texte': "912 livraisons planifiées, réparties sur les 5 lignes de production.",
         'source': 'MASTERVIEW.xlsm (feuille DeliveryPlan)', 'statut': 'confirme'},
        {'texte': "861 lots camion, 919 camions au total, 4 204 tonnes.",
         'source': 'MASTERVIEW.xlsm (feuille LIST)', 'statut': 'confirme'},
        {'texte': "96 livraisons par jour en moyenne ; une plateforme part environ toutes les "
                  "11 minutes.", 'source': 'LAYOUT_RF.pptx + TRAILER_QUANTITY_PER_FLOW.xlsx',
         'statut': 'confirme'},
        {'texte': "Fenêtre d'exploitation de 18h/jour (2 postes).",
         'source': 'TRAILER_QUANTITY_PER_FLOW.xlsx', 'statut': 'confirme'},
        {'texte': "Flotte recommandée pour le flux Stock→Halls : 24 plateformes (marge "
                  "opérationnelle de 20% incluse), sur la base d'un cycle logistique moyen de "
                  "3h40 mesuré par GPS (SENSOLUS).",
         'source': 'TRAILER_QUANTITY_PER_FLOW.xlsx (feuille STOCK RF to HALL)', 'statut': 'confirme'},
        {'texte': "Flux RF→Stock : 22 camions/jour ; Externe→Stock : ~4 camions/jour ; "
                  "Stock→Halls : 33 camions/jour (répartis par point de chargement Lyon 1/2/3, "
                  "Brest 1/2).", 'source': 'FLOW_BRESTLYON.pptx', 'statut': 'confirme'},
        {'texte': "789 livraisons sur 830 (95,1%) ne nécessitent qu'un seul point de chargement ; "
                  "41 (4,9%) en nécessitent deux — cas des Shear Keys chargées à Lyon puis "
                  "complétées à Sogod.", 'source': 'EXCEPTIONS_TWO_STOPS_DELIVERIES.pptx, citant '
                  'lui-même « Truck for All Sets – V2, feuille LIST, colonne P »', 'statut': 'confirme'},
        {'texte': "Détail camion par point de chargement et par origine (halls/RF/externe) avec "
                  "temps de manutention : Lyon 1 = 14,5 camions/6h40 ; Lyon 2 = 12 camions/6h20 "
                  "(mais 13 dans un autre document, voir contradiction) ; Lyon 3 = 8 camions/3h20 ; "
                  "Brest 1 = 10 camions/3h25 ; Brest 2 = 14,5 camions/6h50 (mais 12,5 dans un autre "
                  "document, voir contradiction).", 'source': 'Detailed_Truck__Loading_Time.xlsx',
         'statut': 'confirme'},
        {'texte': "Plan d'affectation remorque par lot : ex. BS segments 1-9 réparties sur 3 "
                  "remorques (remorque 1 = BS1,2,5 + 4 rangées de U-profiles ; remorque 2 = BS3,4 ; "
                  "remorque 3 = reste) ; TS segment 5 sur 6 remorques ; TS segments 1-4/6-9 sur 5 "
                  "remorques.", 'source': 'Trailer_Allocation_Plan.xlsx', 'statut': 'confirme'},
        {'texte': "Planning hebdomadaire ESS réel (échantillons semaine 18 et semaine 30/2026) : "
                  "grille en tranches de 2h de 6h à 18h (6 créneaux/jour, soit une amplitude "
                  "journalière de 12h), avec des livraisons programmées le samedi dans les deux "
                  "échantillons.", 'source': 'ESS_PLANNING.xlsx (feuilles WEEK 18 et WEEK 19)',
         'statut': 'confirme'},
        {'texte': "Registre de risques logistiques RF formel, avec fréquence/impact/détection notés "
                  "de 1 à 5 et score de criticité : risque le plus élevé (score 50) = « plateformes "
                  "insuffisantes pour l'approvisionnement production », action préventive proposée "
                  "= tampon de 3 à 5 remorques supplémentaires ; second risque (score 40) = panne de "
                  "grue magnétique (DCM/threading) ; troisième (score 36) = vent, sans solution "
                  "identifiée pour l'instant.", 'source': 'TOPICS_RISK_ANALYSIS_SUB_ELEMENT_SIZIING.xlsx '
                  '(feuille RISK ANALYSIS)', 'statut': 'confirme'},
        {'texte': "Dimensionnement du nombre de plateformes en réserve : capacité de stockage "
                  "maximale 25 plateformes en halls, ~25 plateformes au RF (parking Julieto + "
                  "buffer derrière DCM loose) ; dimensionnement visé à P90 pour 120 livraisons/jour "
                  "(1 plateforme ≈ 3-4 livraisons/jour) ; cycle logistique détaillé = 40 min "
                  "chargement + 10 min transport client + 3h attente + 40 min déchargement + 10 min "
                  "transport usine.", 'source': 'TOPICS_RISK_ANALYSIS_SUB_ELEMENT_SIZIING.xlsx '
                  '(feuille NUMBER PLATFORM)', 'statut': 'provisoire'},
        {'texte': "Zones de stockage nommées par ville (Toulouse 800 m², Varsovie 580 m², Lyon "
                  "3 440 m², Cracovie, Monaco, Drogo) avec surface au sol par type d'élément et "
                  "moyen de manutention associé (PR14, PR51/52/53, Manitou, C1/C2, grue portique).",
         'source': 'TOPICS_RISK_ANALYSIS_SUB_ELEMENT_SIZIING.xlsx (feuille MAX STORAGE) + '
                    'LIST_FLUX_ET_QUANTITE_MISE_EN_STOCK.xlsx', 'statut': 'confirme'},
    ],
    'hypotheses': [
        {'texte': "Lyon et Brest CONFIRMÉS (11/08/2026, directement par l'utilisateur du projet) "
                  "comme des zones DU SITE, pas des destinations géographiques réelles — un plan "
                  "général du site listant les autres zones du même type doit suivre. Reste "
                  "probable mais non confirmé un par un : « Toulouse », « Varsovie », « Cracovie », "
                  "« Monaco », « Drogo » et « Sogod » suivent vraisemblablement la même convention "
                  "de noms de code internes pour des zones de stockage/chargement sur site — "
                  "plusieurs de ces mêmes noms désignent déjà des zones de stockage aux côtés de "
                  "villes qui n'ont manifestement aucun rapport géographique avec le chantier "
                  "(Drogo, Monaco), ce qui va dans ce sens. À vérifier sur le plan général une fois "
                  "reçu.",
             'a_valider_par': 'Valery Claise', 'statut': 'confirme'},
        {'texte': "Durée d'un poste : 4 valeurs différentes trouvées selon le document — 9h "
                  "(présentation Rebar, Cranes_conclusions.xlsx, ET Tempo_Walls.xlsx qui a "
                  "littéralement des colonnes « duration S3-S7 (shift 9h) » — 3 sources "
                  "convergent maintenant sur 9h), 10h (Truck_for_All_Set__V2, feuille "
                  "Hypothèses — 1 source), 8h ou 12h (Casting Team, non tranché — 1 source), et "
                  "une grille N3 à fenêtres de ~4h45-5h qui ne correspond à aucune des trois. "
                  "9h devient l'hypothèse la mieux étayée à ce stade, mais reste à faire "
                  "confirmer explicitement — le point reste le plus structurant à trancher en "
                  "réunion de conciliation.",
             'a_valider_par': 'Olivier Bonnot (arbitrage transverse)', 'statut': 'a_trancher'},
        {'texte': "Nom et nombre de types de rack : « mesh » et « ESS » (réunion du 10/08), "
                  "« White Rack » (MASTERVIEW.xlsm), « Yellow Rack » (LAYOUT_RF.pptx). Deux ou "
                  "trois types réels ? Terminologie à unifier.",
             'a_valider_par': 'Valery Claise', 'statut': 'a_trancher'},
        {'texte': "Nombre de places de parking remorques : 13 (TRAILER_CAPACITY.pptx, une zone "
                  "précise) contre 59 (LAYOUT_RF.pptx, « TOTAL »). Périmètres probablement "
                  "différents (une sous-zone vs le total du site) mais non confirmé.",
             'a_valider_par': 'équipe logistique', 'statut': 'a_trancher'},
    ],
    'contradictions': [
        {'texte': "Nombre de camions par point de chargement : Lyon 2 = 12 camions (Detailed_Truck) "
                  "contre 13 (Quantity_Designation_Surface, feuille Truck Number) ; Brest 2 = 14,5 "
                  "camions (Detailed_Truck) contre 12,5 (Quantity_Designation_Surface). Lyon 1, "
                  "Lyon 3 et Brest 1 concordent entre les deux fichiers. Écart net sur 2 des 5 "
                  "points, cause non identifiée (versions différentes du même calcul ?).",
             'sources': ['Detailed_Truck__Loading_Time.xlsx',
                          'Quantity_Designation_Surface.xlsx (feuille Truck Number)']},
        {'texte': "Le planning ESS réel (échantillons datés) montre des livraisons programmées le "
                  "samedi — cohérent avec les autres indices de travail le week-end déjà relevés "
                  "en zones N/S (voir REGISTRE_VALIDATION), mais contradictoire avec toute "
                  "hypothèse de « pas de travail le week-end ».",
             'sources': ['ESS_PLANNING.xlsx (feuilles WEEK 18 et WEEK 19)']},
        {'texte': "L'hypothèse de calage retenue jusqu'ici pour le moteur (Ti = jour calendaire, "
                  "Line 1 démarre en premier) ne se confirme pas sur les dates réelles : la date de "
                  "livraison la plus ancienne par ligne dans DeliveryPlan est, dans l'ordre, Line 3 "
                  "(08/05/2026), Line 2 (19/05), Line 5 (20/05), Line 4 (01/06), Line 1 (25/06) — "
                  "Line 1 est la DERNIÈRE, pas la première, contrairement à son déphasage N1 le plus "
                  "petit (T1). Explication probable : ces dates ne couvrent qu'une fenêtre du "
                  "planning (pas le tout premier élément de chaque ligne), donc ne permettent pas "
                  "de calage direct — mais ça invalide un calage naïf par « date de livraison la "
                  "plus ancienne », resté non tenté pour cette raison.",
             'sources': ['MASTERVIEW.xlsm (feuille DeliveryPlan, calculé)']},
        {'texte': "Le nombre de livraisons/jour recalculé directement depuis DeliveryPlan "
                  "(tempo/moteur/logistique.py) donne une moyenne de 11,6/jour et un pic à 22, très "
                  "loin des « 96 livraisons/jour » cités par ailleurs (LAYOUT_RF.pptx + "
                  "TRAILER_QUANTITY_PER_FLOW.xlsx) — facteur 8 environ. Explication probable : "
                  "DeliveryPlan (912 lignes) ne couvre qu'une partie du flux logistique total (un "
                  "flux ou une fenêtre temporelle particuliers), pas la totalité des livraisons "
                  "sitewide citée dans le chiffre de 96 — mais ce n'est pas confirmé.",
             'sources': ['MASTERVIEW.xlsm (feuille DeliveryPlan, calculé via tempo/moteur/logistique.py)',
                          'LAYOUT_RF.pptx', 'TRAILER_QUANTITY_PER_FLOW.xlsx']},
    ],
    'fichiers': ['MASTERVIEW.xlsm', 'TRAILER_QUANTITY_PER_FLOW.xlsx', 'FLOW_BRESTLYON.pptx',
                 'LAYOUT_RF.pptx', 'TRAILER_CAPACITY.pptx', 'EXCEPTIONS_TWO_STOPS_DELIVERIES.pptx',
                 'Truck_for_All_Set__V2.xlsx', 'Detailed_Truck__Loading_Time.xlsx',
                 'Trailer_Allocation_Plan.xlsx', 'Quantity_Designation_Surface.xlsx',
                 'ESS_PLANNING.xlsx', 'TOPICS_RISK_ANALYSIS_SUB_ELEMENT_SIZIING.xlsx',
                 'LIST_FLUX_ET_QUANTITE_MISE_EN_STOCK.xlsx', 'JUSTIFICATION_STORAGE.pptx',
                 'Cranes_conclusions.xlsx',
                 'General_Tempo_Staggering_MDI_V5.xlsm (non encore dépouillé au-delà de la feuille '
                 'HYPOTHESE PL)', 'PROCESS.xlsx (fichier vide, aucune donnée)'],
}

# Équipements et prestataires trouvés, tous documents confondus, consolidés par zone —
# répond directement à « tout les équipements que tu as trouvé ». `type` distingue
# grue/centrale/véhicule/prestataire/stockage pour un futur filtre ; `zones` cite les
# zones réelles (ZONES_REELLES) où l'équipement a été relevé, 'Logistique' pour ce qui
# concerne l'amont (hors zones de production).
EQUIPEMENTS = [
    {'nom': 'Skidding team', 'type': 'équipe logistique interne',
     'description': "Déplace les éléments d'une position de coulée/curing à l'autre "
                     "(« Pushing »), et l'élément complet vers l'Upper Basin (« Big Push »). "
                     "Identifiée à la fois dans le N3 (ressource dédiée, phases T/U+K/L) et "
                     "dans le planning MPP outfitting.",
     'zones': ['R1', 'R2', 'R3', 'Casting Pit', 'Upper Basin'],
     'source': 'STE__TEMPO__N3_Takt_Plan__V0_1.xlsx + Tempo_full_schedule_linked_V4_70_jour.mpp'},
    {'nom': 'Grues Casting Pit (nombre non précisé)', 'type': 'grue',
     'description': "Seule zone où le classeur N3 documente des heures-grue par tâche "
                     "(185 tâches sur 3243, uniquement phases M à L) — voir la courbe "
                     "d'utilisation grue calculée dans le schéma.",
     'zones': ['Casting Pit'], 'source': 'STE__TEMPO__N3_Takt_Plan__V0_1.xlsx (calculé)'},
    {'nom': 'Grue(s) Base Slab', 'type': 'grue', 'description': '1,5 grue affectée.',
     'zones': ['Base Slab'], 'source': 'TEMPO_N2_Presentation_Rebar_04062026.pptx + '
              'General_Tempo_Staggering_MDI_V5.xlsm'},
    {'nom': 'Grue(s) Top Slab', 'type': 'grue', 'description': '2 grues affectées.',
     'zones': ['Base Slab'], 'source': 'General_Tempo_Staggering_MDI_V5.xlsm (feuille Data base)'},
    {'nom': 'Grue spéciale murs', 'type': 'grue', 'description': '1 grue dédiée aux murs.',
     'zones': ['Walls'], 'source': 'General_Tempo_Staggering_MDI_V5.xlsm (feuille Data base)'},
    {'nom': 'C1 / C2', 'type': 'grue', 'description': "Grues de mise en stock RF, capacités "
                     "citées à 15,25 et 15,00 (unité non confirmée) — voir aussi le plafond "
                     "« pas plus de 2 grues pour un top slab, 1 pour un mur, 3 pour deux base "
                     "slabs même halle ».",
     'zones': ['Logistique'], 'source': 'Detailed_Truck__Loading_Time.xlsx + '
              'Explanations_Takt_time_files.pptx'},
    {'nom': 'Centrales à béton (6, dont B6 pas encore construite)', 'type': 'centrale à béton',
     'description': 'A1/A2/A3, B4/B5/B6 — B6 n\'existe pas encore.',
     'zones': ['Casting Pit'], 'source': 'General_Tempo_Staggering.xlsx (feuille Casting Pattern)'},
    {'nom': 'Flotte plateformes/remorques (24 recommandées)', 'type': 'véhicule',
     'description': "Dimensionnement recommandé pour le flux Stock→Halls, marge "
                     "opérationnelle 20% incluse — voir aussi le risque n°1 du registre RF "
                     "(tampon de 3 à 5 remorques proposé) et le module tempo/moteur/alea.py.",
     'zones': ['Logistique'], 'source': 'TRAILER_QUANTITY_PER_FLOW.xlsx (feuille STOCK RF to HALL)'},
    {'nom': 'Racks (mesh/ESS, White Rack, Yellow Rack — nombre de types non confirmé)',
     'type': 'stockage', 'description': "Trois désignations trouvées pour ce qui pourrait "
                     "être 2 ou 3 types réels — voir le registre de validation.",
     'zones': ['Logistique'], 'source': 'réunion TEMPO (10/08) + MASTERVIEW.xlsm + LAYOUT_RF.pptx'},
    {'nom': 'PR14 / PR51 / PR52 / PR53', 'type': 'moyen de manutention',
     'description': "Moyens de manutention cités pour la mise en stock (Starter Bar, panels "
                     "DCM) dans les zones de stockage nommées Toulouse/Sogod.",
     'zones': ['Logistique'], 'source': 'LIST_FLUX_ET_QUANTITE_MISE_EN_STOCK.xlsx'},
    {'nom': 'Manitou / Truck Mounted Crane', 'type': 'moyen de manutention',
     'description': "Cités pour la manutention de Niches, TO, EF (zone de stockage nommée "
                     "Krakow) et Threading/Progress (zone nommée Monaco/Toulouse).",
     'zones': ['Logistique'], 'source': 'LIST_FLUX_ET_QUANTITE_MISE_EN_STOCK.xlsx'},
    {'nom': 'Dywidag (post-tension)', 'type': 'prestataire',
     'description': "PT Threading (3,25j), PT Stressing (3,25j), PT Grout (2,5j) — planifiés "
                     "après le Big Push d'après l'ordre du planning MPP.",
     'zones': ['Upper Basin'], 'source': 'Tempo_full_schedule_linked_V4_70_jour.mpp'},
    {'nom': 'FLC WORKER', 'type': 'main-d\'œuvre (BC FLC)',
     'description': "Ressource des tâches « Casting » par segment dans le planning MPP "
                     "(~1,5 jour/segment).", 'zones': ['Casting Pit'],
     'source': 'Tempo_full_schedule_linked_V4_70_jour.mpp'},
    {'nom': 'CEAS, GTA, Impostal, Sejerslev, Constructel, JD Steel, MSE, WL, BL',
     'type': 'sous-traitant', 'description': "Codes sous-traitants relevés dans les colonnes "
                     "ressource du N3. GTA = fireprotection, MSE (coquille pour MSI) = béton de "
                     "ballast — décodés le 11/08/2026, confirmés par l'utilisateur. Décodage "
                     "encore incomplet pour WL (voir le registre de validation).",
     'zones': ['toutes'], 'source': 'STE__TEMPO__N3_Takt_Plan__V0_1.xlsx (feuille Data) + '
              'Tempo_full_schedule_linked_V4_70_jour.mpp + '
              "confirmé directement par l'utilisateur du projet (11/08/2026, pour GTA/MSE)"},
]

# Ateliers de détail (« WORKSHOP ORGA », dernière diapo de STE__General_Temo_Overview__
# DRAFT.pptx) : sujet, responsable pressenti (initiales telles que dans le document — non
# décodées, voir le registre de validation), semaine(s) planifiée(s), équipes impliquées.
# C'est une liste d'ateliers à tenir, pas des points à trancher — gardée séparée du
# registre de validation pour cette raison, même structure de traçabilité.
ATELIERS_DETAIL = [
    {'sujet': 'Sliding Gate', 'responsable': 'PDE',
     'notes': "Bien avancé mais pas formalisé — à fusionner avec l'atelier Float-up ? "
              "(question posée dans le document lui-même).",
     'semaines': [], 'equipes': ['Marine', 'OF', 'Skidding', 'PP & R'], 'statut': 'provisoire'},
    {'sujet': 'Float-up', 'responsable': None,
     'notes': "Aucun responsable ni semaine indiqués dans le document (points "
              "d'interrogation « Float-up ?? ») — atelier pas encore cadré.",
     'semaines': [], 'equipes': ['Marine', 'Plant', 'OF', 'Skidding'], 'statut': 'a_trancher'},
    {'sujet': 'General Post-Pour', 'responsable': 'SFO',
     'notes': "Atelier de 2025 — à revoir après les ateliers détaillés Outfitting.",
     'semaines': ['1 – W19'], 'equipes': ['PP & R', 'Outfitting', 'TE System', 'Survey', 'Plant'],
     'statut': 'confirme'},
    {'sujet': 'Detailed Outfitting Transversal', 'responsable': 'MTS',
     'notes': '', 'semaines': ['1 – W18 28/04'], 'equipes': ['OF.T'], 'statut': 'confirme'},
    {'sujet': 'Detailed Outfitting Integrated', 'responsable': 'MJA',
     'notes': '', 'semaines': ['1 – W18 28/04'], 'equipes': ['OF.I', 'TES'], 'statut': 'confirme'},
    {'sujet': 'Detailed Repairs', 'responsable': 'JUO',
     'notes': "Fait, à revoir/mettre à jour d'après le document.",
     'semaines': [], 'equipes': ['PP & R'], 'statut': 'provisoire'},
    {'sujet': 'General Pre-Pour', 'responsable': 'SFO',
     'notes': '', 'semaines': ['1 – W19'],
     'equipes': ['FW', 'CAS', 'Skidding', 'Rebar Hall', 'Survey', 'Plant'], 'statut': 'confirme'},
    {'sujet': 'Detailed Casting Pit', 'responsable': 'OSI',
     'notes': '', 'semaines': ['1 – W17 23/04', '2 – W18 29/04'],
     'equipes': ['FW', 'CAS', 'Skidding', 'Survey'], 'statut': 'confirme'},
    {'sujet': 'Detailed Rebar Hall', 'responsable': 'MDI',
     'notes': "Un 3e passage évoqué (« from 2nd WS? ») mais pas confirmé.",
     'semaines': ['1 – W17 22/04', '2 – W18 29/04'],
     'equipes': ['Rebar Hall', 'Panel Factory', 'Skidding', 'Survey', 'CAS'], 'statut': 'confirme'},
    {'sujet': 'Panel Factory', 'responsable': 'PBR',
     'notes': "Périmètre : jusqu'aux livraisons dans les halls.",
     'semaines': ['1 – W17 23/04', '2 – W19'],
     'equipes': ['Panel Factory', 'Rebar Hall'], 'statut': 'confirme'},
    {'sujet': 'Detailed S9-S1', 'responsable': 'AGA',
     'notes': '', 'semaines': ['3 – W17 21/04', '4 – W17 22/04', '5 – W18 27/04'],
     'equipes': ['FW (KST + PKR)'], 'statut': 'confirme'},
    {'sujet': 'Detailed Casting Sequence', 'responsable': 'PPB / DHU',
     'notes': '', 'semaines': ['1 – W18 27/04'],
     'equipes': ['CAS', 'Lab', 'Batching Plant'], 'statut': 'confirme'},
]

# Registre de validation : une ligne par point encore ouvert, tous zones confondues — la
# matière d'une réunion de conciliation, pas un rapport de plus. Regroupé par personne
# responsable pressentie, pour qu'une invitation de réunion puisse s'écrire directement
# à partir de cette liste.
REGISTRE_VALIDATION = [
    {'point': "QUASI RÉSOLU le 10/08/2026. Rappel : (1) l'utilisateur a confirmé directement que "
              "les codes lettre (A à I/M à L) sont des PHASES, pas des zones physiques ; (2) une "
              "zone physique peut être travaillée sur PLUSIEURS phases. Le mécanisme exact a "
              "ensuite été retrouvé dans General_Tempo_Staggering_MDI_V5.xlsm, feuille "
              "« 70__63 - 1L - V0 » (le gabarit source à 70 jours pour une ligne) : chaque lettre "
              "désigne une fenêtre d'environ 7 jours tempo (T1 à T7) le long du cycle de 70 jours "
              "d'un élément — la lettre M réapparaît d'ailleurs à la colonne 299 de cette feuille, "
              "confirmant que le cycle se répète. Pour chaque fenêtre, plusieurs lignes UNIT "
              "(Walls, BS, LASCA, Buffer, CP...) portent simultanément un nombre de postes non nul "
              "— c'est exactement ce qui explique le mélange trouvé dans "
              "ZONES_PHYSIQUES_REELLES/« Répartition réelle » : plusieurs zones physiques "
              "avancent en parallèle à l'intérieur d'une même fenêtre temporelle. Ne reste "
              "vraiment ouvert que l'aspect visuel : faut-il redessiner le schéma (actuellement "
              "organisé par zone physique depuis la mise à jour du 10/08) pour montrer aussi "
              "explicitement ce découpage en fenêtres de 7 jours ?",
     'zone': 'toutes', 'responsable': 'Valery Claise / Joanna',
     'impact': "moyen — le mécanisme est compris et documenté ; il ne reste qu'une question de "
               "présentation, plus de fiabilité des données"},
    {'point': "Système de postes de l'équipe de coulée (3×8h vs 2×12h)", 'zone': 'S',
     'responsable': 'équipe Casting Team', 'impact': 'critique — conditionne toute la grille horaire du moteur'},
    {'point': "Durée de poste divergente entre documents — 9h maintenant confirmé par 3 sources "
              "indépendantes (Rebar, Cranes_conclusions.xlsx, Tempo_Walls.xlsx) contre 1 chacune "
              "pour 10h et 8h/12h ; reste à faire trancher officiellement.", 'zone': 'Logistique',
     'responsable': 'Olivier Bonnot', 'impact': 'critique — même sujet que ci-dessus, vu sous un autre angle'},
    {'point': "Écart entre notre relevé des segments N3 manquants et le suivi officiel "
              "(N3 Overview (Missing))", 'zone': 'N, O',
     'responsable': 'Valery Claise / Joanna', 'impact': 'élevé — détermine où concentrer le chiffrage restant'},
    {'point': "Pic d'effectif BC en zone Casting Pit : 95 avec l'outil actuel (proche des 105-117 "
              "cités) vs 228 trouvé par une version antérieure du même calcul — cause de l'écart "
              "entre les deux calculs non identifiée", 'zone': 'S', 'responsable': 'équipe Casting Team',
     'impact': 'moyen — réduit fortement depuis la dernière mesure, à confirmer plutôt qu\'à dimensionner dessus'},
    {'point': "Travail du week-end : hypothèse « aucun » mais quatre sources indépendantes signalent "
              "un besoin réel (4 samedis/cycle pour les murs, dimanche skidding en L4, S2 skidding "
              "L4 tombe un samedi, livraisons ESS programmées le samedi dans les deux échantillons "
              "de planning réel disponibles)", 'zone': 'N, S, Logistique',
     'responsable': 'équipe TEMPO (arbitrage global)', 'impact': 'élevé'},
    {'point': "Nombre et nom des types de rack (mesh/ESS vs White vs Yellow)", 'zone': 'Logistique',
     'responsable': 'Valery Claise', 'impact': 'moyen'},
    {'point': "Ordre d'installation des murs — quasi résolu : B,C,D,E,A,F trouvé deux fois "
              "identique dans General_Tempo_Staggering_MDI_V5.xlsm, plus fiable que le "
              "« B-C-A-D-E-F » entendu en réunion (transcription bruitée). À faire confirmer "
              "simplement en réunion plutôt qu'à retrancher depuis zéro.", 'zone': 'Walls',
     'responsable': 'Valery Claise / Joanna', 'impact': 'faible'},
    {'point': "Nombre de camions Lyon 2 (12 ou 13) et Brest 2 (14,5 ou 12,5) selon le document",
     'zone': 'Logistique', 'responsable': 'équipe logistique', 'impact': 'moyen'},
    {'point': "PARTIELLEMENT RÉSOLU le 11/08/2026 : Lyon et Brest confirmés comme zones DU SITE "
              "(pas des destinations géographiques réelles), directement par l'utilisateur, qui a "
              "annoncé fournir un plan général du site listant les autres zones du même type. "
              "Reste ouvert : Toulouse/Varsovie/Cracovie/Monaco/Drogo/Sogod suivent "
              "vraisemblablement la même convention mais ne sont pas encore confirmés "
              "explicitement un par un — à vérifier sur le plan général une fois reçu.",
     'zone': 'Logistique', 'responsable': 'Valery Claise',
     'impact': 'moyen — structure toute la lecture des flux'},
    {'point': "Risque n°1 du registre RF (score 50) : plateformes insuffisantes pour "
              "l'approvisionnement production — action proposée (tampon 3 à 5 remorques) à valider "
              "et chiffrer", 'zone': 'Logistique', 'responsable': 'équipe logistique',
     'impact': 'élevé — condition du dimensionnement de flotte retenu (24 plateformes)'},
    {'point': "PRESQUE RÉSOLU le 11/08/2026 : GTA (fireprotection) et MSE/MSI (béton de ballast) "
              "décodés, confirmés directement par l'utilisateur. Ne reste ouvert que WL (« ask "
              "Lotte » — même la source ne sait pas).",
     'zone': 'toutes', 'responsable': 'Lotte (pour WL)',
     'impact': 'faible — gêne la lecture, pas le calcul'},
    {'point': "Nombre de places de parking remorques : 13 ou 59 selon le document (périmètres "
              "probablement différents)", 'zone': 'Logistique', 'responsable': 'équipe logistique',
     'impact': 'faible'},
    {'point': "MÉCANISME PRÉCISÉ le 11/08/2026 (utilisateur), correspondance exacte encore ouverte. "
              "N1/N2/N3 = zones à l'intérieur du hall (après casting, avant que l'élément ne dépasse "
              "du hall) ; OF1-OF5 = positions à l'extérieur du hall ; UB = position après le big "
              "push. S1 à S9 sont des segments de l'élément, pas des zones : le segment S1 est "
              "poussé successivement en N1, N2, ... jusqu'à OF5 ; le segment S2 s'arrête à OF4. "
              "Reste à établir : le nombre exact de positions N1/N2/(N3 ?), le détail "
              "segment↔position pour S3 à S9, et où faire figurer les zones N1/N2/N3 dans ce "
              "schéma (absentes pour l'instant — seules OF1-OF5/SG et UB-S9/S8/S7 y sont "
              "représentées). Un plan général du site, annoncé par l'utilisateur, doit aider à "
              "trancher.",
     'zone': 'Outfitting Area, Upper Basin', 'responsable': 'Valery Claise / Joanna',
     'impact': 'moyen — nécessaire pour rattacher les 631 tâches MPP à un code de zone exploitable'},
    {'point': "Livraisons/jour recalculées depuis DeliveryPlan (11,6 en moyenne, pic 22) très "
              "inférieures aux 96/jour cités ailleurs — périmètre de DeliveryPlan (912 lignes) à "
              "clarifier : flux partiel ou fenêtre temporelle partielle ?",
     'zone': 'Logistique', 'responsable': 'équipe logistique',
     'impact': 'élevé — conditionne le dimensionnement de flotte si DeliveryPlan doit servir de référence'},
    {'point': "NOUVEAU 11/08/2026 (STE__General_Temo_Overview__DRAFT.pptx) : une aire « Lower "
              "Basin » apparaît en en-tête sur les 19 diapos du storyboard tempo, à gauche "
              "d'« Upper Basin » — pas encore représentée dans ce dossier ni dans le schéma "
              "interactif. Sa position exacte dans le flux (juste après Upper Basin ? une "
              "sous-zone ?) et son contenu (sous-zones, tâches) restent à établir.",
     'zone': 'toutes', 'responsable': 'Valery Claise / Joanna',
     'impact': 'moyen — une aire entière du site manque au schéma actuel'},
    {'point': "CONTRADICTION 11/08/2026 (STE__General_Temo_Overview__DRAFT.pptx) : ce document "
              "dessine Buffer/LASCA/BS/Walls sous l'en-tête « Rebar Hall », alors que ce dossier "
              "classe Buffer sous « Production Hall » (voir `_AIRE_PAR_ZONE_REELLE`). À "
              "réconcilier — peut-être une zone de transition comptée différemment selon les "
              "documents.",
     'zone': 'Buffer', 'responsable': 'Valery Claise / Joanna',
     'impact': 'faible — n\'affecte que le regroupement visuel par aire, pas les données de zone elles-mêmes'},
    {'point': "Initiales des responsables d'ateliers non décodées : PDE, SFO, MTS, MJA, JUO, OSI, "
              "MDI, PBR, AGA, PPB, DHU (voir ATELIERS_DETAIL, tiré de STE__General_Temo_Overview__"
              "DRAFT.pptx, diapo « WORKSHOP ORGA »).",
     'zone': 'toutes', 'responsable': 'équipe TEMPO',
     'impact': 'faible — gêne la lecture, pas le calcul'},
]
