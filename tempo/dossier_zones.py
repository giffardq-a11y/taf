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
        ],
        'hypotheses': [
            {'texte': "Ordre d'installation des murs — cité B-C-A-D-E-F en réunion, très bruité "
                      "dans la transcription automatique.",
             'a_valider_par': 'Valery Claise / Joanna', 'statut': 'a_trancher'},
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
]
_HYPOTHESE_MAPPING_MPP = {
    'texte': "Correspondance non établie entre le découpage du planning MPP (par segment S1-S9 "
             "d'un élément « TE 01 ») et les codes de zone N1/N3 (OF1-OF5/SG pour l'Outfitting "
             "Area, UB-S9/S8/S7 pour l'Upper Basin). Les deux décrivent vraisemblablement les "
             "mêmes travaux vus sous deux découpages différents (par position physique dans "
             "l'aire vs par segment de l'élément), mais rien ne le confirme explicitement.",
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
                             "Base Slab/LASCA/Walls/Buffer, pas à l'Outfitting — la correspondance "
                             "avec le planning MPP outfitting (Données ci-dessus) reste donc "
                             "elle-même à confirmer, pas résolue par ce constat.",
                             'sources': ['STE__TEMPO__N3_Takt_Plan__V0_1.xlsx (calculé, 10/08/2026)']}],
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
                             "rattachées à LASCA/Base Slab/Walls, pas à l'Upper Basin — la "
                             "correspondance avec le planning MPP outfitting (Big Push, "
                             "post-tension, flottaison — Données ci-dessus) reste donc à confirmer.",
                             'sources': ['STE__TEMPO__N3_Takt_Plan__V0_1.xlsx (calculé, 10/08/2026)']}],
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

LOGISTIQUE = {
    'nom': 'Logistique amont — livraisons Lyon/Brest → stock → halls',
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
        {'texte': "Les noms « Lyon », « Brest », mais aussi « Toulouse », « Varsovie », "
                  "« Cracovie », « Monaco », « Drogo » et « Sogod » sont vraisemblablement des "
                  "noms de code internes pour des zones de stockage/chargement sur site, et non des "
                  "destinations géographiques réelles des camions — l'hypothèse initiale (« Lyon/"
                  "Brest = points de chargement réels ») doit être révisée : plusieurs de ces mêmes "
                  "noms désignent des zones de stockage aux côtés de villes qui n'ont manifestement "
                  "aucun rapport géographique avec le chantier (Drogo, Monaco). À confirmer "
                  "explicitement — la distinction « point de chargement » vs « zone de stockage "
                  "nommée pareil » n'est peut-être pas si nette non plus.",
             'a_valider_par': 'Valery Claise', 'statut': 'a_trancher'},
        {'texte': "Durée d'un poste : 4 valeurs différentes trouvées selon le document — 9h "
                  "(présentation Rebar), 10h (Truck_for_All_Set__V2, feuille Hypothèses), 8h ou "
                  "12h (Casting Team, non tranché), et une grille N3 à fenêtres de ~4h45-5h qui "
                  "ne correspond à aucune des trois. Point le plus structurant à trancher en "
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

# Registre de validation : une ligne par point encore ouvert, tous zones confondues — la
# matière d'une réunion de conciliation, pas un rapport de plus. Regroupé par personne
# responsable pressentie, pour qu'une invitation de réunion puisse s'écrire directement
# à partir de cette liste.
REGISTRE_VALIDATION = [
    {'point': "CLARIFIÉ le 10/08/2026, directement par l'utilisateur du projet, en deux temps : "
              "(1) les codes lettre (A à I/M à L) NE SONT PAS des zones physiques, ce sont des "
              "PHASES — des repères temporels dans le gabarit tempo pendant lesquels certains "
              "travaux doivent se dérouler ; (2) une zone physique peut être travaillée sur "
              "PLUSIEURS phases (pas une correspondance 1 lettre = 1 zone). Confirmé par le calcul "
              "(voir ZONES_PHYSIQUES_REELLES dans tempo/dossier_zones.py) : « Casting Pit » "
              "apparaît dans les 10 phases M/N/O/P/Q/R/S/T/U+K/L (114 à 162 tâches chacune) ; "
              "« Walls »/« Base Slab »/« LASCA »/« Buffer » apparaissent chacune dans la quasi-"
              "totalité des 9 phases A à I, à peu près à parts égales. Chaque phase du schéma "
              "porte désormais la répartition réelle des zones physiques qu'elle touche (donnée "
              "« Répartition réelle... ») ; chaque zone physique porte la liste des phases où elle "
              "apparaît (ZONES_PHYSIQUES_REELLES). Reste ouvert : que représente exactement la "
              "feuille Data si ce n'est pas une correspondance lettre->zone physique (un repère de "
              "gabarit/position dans le cycle de 70 jours tempo ?), et faut-il redessiner le schéma "
              "visuel en conséquence (aires de regroupement, libellés des 19 cases) ?",
     'zone': 'toutes', 'responsable': 'Valery Claise / Joanna',
     'impact': "élevé — la nature du problème est clarifiée, mais le schéma visuel (regroupements "
               "par aire, libellés des 19 cases) n'a pas encore été refait en conséquence"},
    {'point': "Système de postes de l'équipe de coulée (3×8h vs 2×12h)", 'zone': 'S',
     'responsable': 'équipe Casting Team', 'impact': 'critique — conditionne toute la grille horaire du moteur'},
    {'point': "Durée de poste divergente entre 4 documents (9h/10h/8h/12h/~4h45)", 'zone': 'Logistique',
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
    {'point': "Ordre d'installation des murs (B-C-A-D-E-F, à confirmer)", 'zone': 'N',
     'responsable': 'Valery Claise / Joanna', 'impact': 'moyen'},
    {'point': "Nombre de camions Lyon 2 (12 ou 13) et Brest 2 (14,5 ou 12,5) selon le document",
     'zone': 'Logistique', 'responsable': 'équipe logistique', 'impact': 'moyen'},
    {'point': "Les noms Lyon/Brest/Toulouse/Varsovie/Cracovie/Monaco/Drogo/Sogod désignent-ils des "
              "destinations réelles, des zones de stockage nommées par convention, ou les deux à la "
              "fois selon le contexte ?", 'zone': 'Logistique', 'responsable': 'Valery Claise',
     'impact': 'moyen — structure toute la lecture des flux'},
    {'point': "Risque n°1 du registre RF (score 50) : plateformes insuffisantes pour "
              "l'approvisionnement production — action proposée (tampon 3 à 5 remorques) à valider "
              "et chiffrer", 'zone': 'Logistique', 'responsable': 'équipe logistique',
     'impact': 'élevé — condition du dimensionnement de flotte retenu (24 plateformes)'},
    {'point': "Codes de ressource non décodés : GTA, MSE/MSI, WL (« ask Lotte » — même la source "
              "ne sait pas)", 'zone': 'toutes', 'responsable': 'Lotte (pour WL), équipe TEMPO (pour le reste)',
     'impact': 'faible — gêne la lecture, pas le calcul'},
    {'point': "Nombre de places de parking remorques : 13 ou 59 selon le document (périmètres "
              "probablement différents)", 'zone': 'Logistique', 'responsable': 'équipe logistique',
     'impact': 'faible'},
    {'point': "Correspondance à établir entre le découpage du planning MPP outfitting (par "
              "segment S1-S9 d'un élément) et les codes de zone N1/N3 (OF1-OF5/SG, UB-S9/S8/S7)",
     'zone': 'A, B, C, D, E, F, G, H, I', 'responsable': 'Valery Claise / Joanna',
     'impact': 'moyen — nécessaire pour rattacher les 631 tâches MPP à un code de zone exploitable'},
    {'point': "Livraisons/jour recalculées depuis DeliveryPlan (11,6 en moyenne, pic 22) très "
              "inférieures aux 96/jour cités ailleurs — périmètre de DeliveryPlan (912 lignes) à "
              "clarifier : flux partiel ou fenêtre temporelle partielle ?",
     'zone': 'Logistique', 'responsable': 'équipe logistique',
     'impact': 'élevé — conditionne le dimensionnement de flotte si DeliveryPlan doit servir de référence'},
]
