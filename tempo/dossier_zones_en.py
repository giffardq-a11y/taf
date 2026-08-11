"""English mirror of `dossier_zones.py`, built for the FR/EN toggle on the interactive
artifact (`tempo_zones.html`). Same shapes, same keys — `ZONES_REELLES_EN`,
`LOGISTIQUE_EN`, `REGISTRE_VALIDATION_EN`, `EQUIPEMENTS_EN` — only the natural-language
fields (`texte`, `point`, `description`, `nom` of `LOGISTIQUE`) are translated. Zone
names, file names, people's names, and `statut` codes are left as-is: they're already
English technical terms (Casting Pit, Base Slab...) or proper nouns that don't
translate. This file is a manual translation of `dossier_zones.py` as it stood on
2026-08-11 — if the French source changes, this file needs updating by hand; nothing
here is auto-generated from it.
"""

ZONES_REELLES_EN = {
    'Panel Factory': {
        'aire': 'Panel Factory', 'lettre_origine': 'M', 'phases': [], 'total_taches': 0,
        'donnees': [
            {'texte': "Subcontractors found in N3 tasks: CEAS, Impostal, MSE, JD Steel, WL, BL.",
             'source': 'STE__TEMPO__N3_Takt_Plan__V0_1.xlsx (sheets CP__M)', 'statut': 'confirme'},
            {'texte': "JD Steel appears only in this zone, nowhere else in N3.",
             'source': 'STE__TEMPO__N3_Takt_Plan__V0_1.xlsx', 'statut': 'confirme'},
        ],
        'hypotheses': [], 'contradictions': [],
        'fichiers': ['STE__TEMPO__N3_Takt_Plan__V0_1.xlsx'],
    },
    'Walls': {
        'aire': 'Rebar Hall', 'lettre_origine': 'N', 'phases': [('A', 13), ('B', 13), ('C', 13),
            ('D', 13), ('E', 13), ('F', 13), ('G', 13), ('H', 13), ('I', 13)], 'total_taches': 117,
        'donnees': [
            {'texte': "6 workers, organized into 4 teams of 3 staggered in time, overlap up to 12h.",
             'source': "TEMPO Rebar & Logistic meeting (08/10/2026) + "
                       "TEMPO_N2_Presentation_Rebar_04062026.pptx", 'statut': 'confirme'},
            {'texte': "Number of trucks per wall (A to F) and per segment (S1-S9), e.g. wall B: "
                      "4,3,4,3,3,3,4,3,4 across S1→S9.",
             'source': 'Truck_for_All_Set__V2.xlsx (sheet WALL + RACK)', 'statut': 'confirme'},
            {'texte': "Wall installation order: B, C, D, E, A, F — written twice identically in "
                      "the same document (once as “Sequence of walls”, once as "
                      "“Installation of walls”), more reliable than the “B-C-A-D-E-F” "
                      "heard in the meeting (auto-transcription very noisy at that point).",
             'source': 'General_Tempo_Staggering_MDI_V5.xlsm (sheet Data base, rows 19 and 70)',
             'statut': 'confirme'},
            {'texte': "2 to 4 trucks per wall; walls delivered the shift before production, "
                      "delivery area kept free.",
             'source': 'General_Tempo_Staggering_MDI_V5.xlsm (sheet Data base, rows 17-18)',
             'statut': 'provisoire'},
        ],
        'hypotheses': [
            {'texte': "“Saturday and Sunday off (Expect some for the Wall)” — the "
                      "hypothesis document itself plans a weekend exception for the walls, and "
                      "notes elsewhere: “Work on full Saturday to ensure the walls "
                      "fabrication... Test to be done” — confirms, at the source, the "
                      "weekend-work tension already flagged elsewhere (see REGISTRE_VALIDATION), "
                      "without resolving it itself (“test to be done”).",
             'source': 'General_Tempo_Staggering_MDI_V5.xlsm (sheet Data base, rows 8 and 30)',
             'a_valider_par': 'TEMPO team (global arbitration)', 'statut': 'a_trancher'},
        ],
        'contradictions': [
            {'texte': "N3 segments without detail: our reading finds S4 and S5 missing; the "
                      "official tracker “N3 Overview (Missing)” shows S1/S3/S5/S7/S9 missing "
                      "(the odd segments). The two only overlap on S5.",
             'sources': ['STE__TEMPO__N3_Takt_Plan__V0_1.xlsx (computed, tempo/comparer_n1_n3.py)',
                          'Comparison_N1_shifts_to_target.xlsx (sheet N3 Overview (Missing))']},
        ],
        'fichiers': ['STE__TEMPO__N3_Takt_Plan__V0_1.xlsx', 'TEMPO_N2_Presentation_Rebar_04062026.pptx',
                     'Truck_for_All_Set__V2.xlsx', 'Comparison_N1_shifts_to_target.xlsx',
                     'General_Tempo_Staggering_MDI_V5.xlsm',
                     'Tempo_Walls.xlsx (not yet processed in detail)'],
    },
    'Base Slab': {
        'aire': 'Rebar Hall', 'lettre_origine': 'O', 'phases': [('A', 36), ('B', 29), ('C', 29),
            ('D', 29), ('E', 29), ('F', 29), ('H', 29), ('I', 29), ('G', 13)], 'total_taches': 252,
        'donnees': [
            {'texte': "8 workers continuously.", 'source': "TEMPO meeting (08/10/2026) + "
                      "TEMPO_N2_Presentation_Rebar_04062026.pptx", 'statut': 'confirme'},
            {'texte': "1.5 crane assigned.", 'source': 'TEMPO_N2_Presentation_Rebar_04062026.pptx',
             'statut': 'confirme'},
            {'texte': "Productivity ratio cited as an example: roughly 3 tonnes/hour for 8 people "
                      "— presented as a starting point to be validated by performance tests, not a "
                      "fixed figure.", 'source': 'TEMPO meeting (08/10/2026)', 'statut': 'provisoire'},
            {'texte': "Independent confirmation of headcounts and cranes: “Manpower: 8 BS - "
                      "8 TS - 6 WALLS” and “Crane: 1+1/2 BS - 1 special crane for walls - "
                      "2 cranes for TS” — consistent with the 8 workers / 1.5 crane already "
                      "cited for Base Slab, and adds two new figures (Top Slab: 8 workers, 2 "
                      "cranes) that had no dedicated source until now.",
             'source': 'General_Tempo_Staggering_MDI_V5.xlsm (sheet Data base, rows 9-10)',
             'statut': 'confirme'},
            {'texte': "Breakdown by sub-lot (SET) for Base Slab (BS0=3 workers, BS1 to BS4=8 "
                      "workers each) and for Top Slab (TS1 to TS4=8 workers each) — BS0 likely "
                      "being a lighter prep phase before the bulk of the rebar work.",
             'source': 'General_Tempo_Staggering_MDI_V5.xlsm (sheet Data base, rows 41-45 and 61-64)',
             'statut': 'confirme'},
            {'texte': "Cap on simultaneous cranes, all zones: no more than 2 cranes for a top "
                      "slab, no more than 1 for a wall, no more than 3 for two base slabs in the "
                      "same hall — a method rule for filling in the takt time files, consistent "
                      "with the figures above.",
             'source': 'Explanations_Takt_time_files.pptx', 'statut': 'confirme'},
        ],
        'hypotheses': [
            {'texte': "Hypotheses included in the Base Slab S1-S9 takt time: 2h to bring the jigs "
                      "back up + shoe installation + cleaning; 8 workers; 1 or 2 cranes; activity "
                      "starts at the end of skidding; surveyor, formwork and quality not included "
                      "(no coactivity planned outside skidding).",
             'source': 'General_Tempo_Staggering_MDI_V5.xlsm (sheet HYPOTHESE PL)',
             'a_valider_par': 'Valery Claise / Joanna', 'statut': 'provisoire'},
            {'texte': "Opportunity dropped from the current takt time: bringing the longitudinals "
                      "in by conveyor (limited by the crane and storage space) — not tested, not "
                      "ready.", 'source': 'General_Tempo_Staggering_MDI_V5.xlsm (sheet HYPOTHESE PL)',
             'statut': 'provisoire'},
        ],
        'contradictions': [
            {'texte': "N3 segments without detail: our reading finds S5-S8 missing; the official "
                      "tracker shows BS complete on every segment. Total disagreement.",
             'sources': ['STE__TEMPO__N3_Takt_Plan__V0_1.xlsx (computed, tempo/comparer_n1_n3.py)',
                          'Comparison_N1_shifts_to_target.xlsx (sheet N3 Overview (Missing))']},
        ],
        'fichiers': ['STE__TEMPO__N3_Takt_Plan__V0_1.xlsx', 'TEMPO_N2_Presentation_Rebar_04062026.pptx',
                     'Comparison_N1_shifts_to_target.xlsx', 'General_Tempo_Staggering_MDI_V5.xlsm',
                     'Tempo_Bottomslabs.xlsx / Tempo_Bottomslabs_LCA_rev2.xlsx (not yet processed in '
                     'detail — the source takt time sequences behind the N3 sheets, sheet by sheet '
                     'per segment/segment pair)'],
    },
    'LASCA': {
        'aire': 'Rebar Hall', 'lettre_origine': 'P', 'phases': [('C', 40), ('A', 34), ('B', 34),
            ('D', 34), ('E', 34), ('F', 34), ('H', 34), ('I', 34), ('G', 18)], 'total_taches': 296,
        'donnees': [
            {'texte': "LASCA = the rebar assembly chain area (confirmed directly by the project's "
                      "user).", 'source': 'direct confirmation', 'statut': 'confirme'},
        ],
        'hypotheses': [
            {'texte': "Hypotheses included in the LASCA takt time: scaffolding erected 1/2 shift "
                      "after skidding; rails laid during wall erection; after skidding, 1 shift for "
                      "BO S1/S9 and niches; assembly starts once LASCA is ready and skidding is "
                      "finished; no storage on LASCA (conveyor or middle LASCA) during skidding; "
                      "ESS frame delivered by conveyor.",
             'source': 'General_Tempo_Staggering_MDI_V5.xlsm (sheet HYPOTHESE PL)',
             'a_valider_par': 'Valery Claise / Joanna', 'statut': 'provisoire'},
            {'texte': "Opportunities dropped from the current takt time: storage on the central "
                      "LASCA platform; lifting the walls with BO or installing the BO in Buffer.",
             'source': 'General_Tempo_Staggering_MDI_V5.xlsm (sheet HYPOTHESE PL)', 'statut': 'provisoire'},
        ],
        'contradictions': [
            {'texte': "N3 segments without detail found: S6, S7, S8 — not yet compared to the "
                      "official tracker (which only covers BS/W/TS, not LASCA by name).",
             'sources': ['STE__TEMPO__N3_Takt_Plan__V0_1.xlsx (computed, tempo/comparer_n1_n3.py)']},
        ],
        'fichiers': ['STE__TEMPO__N3_Takt_Plan__V0_1.xlsx', 'General_Tempo_Staggering_MDI_V5.xlsm'],
    },
    'Buffer': {
        'aire': 'Production Hall', 'lettre_origine': 'Q', 'phases': [('B', 12), ('A', 11), ('C', 11),
            ('E', 11), ('F', 11), ('I', 11), ('H', 10), ('D', 9), ('G', 6), ('M', 1), ('N', 1),
            ('O', 1), ('P', 1), ('Q', 1), ('R', 1), ('S', 1)], 'total_taches': 99,
        'donnees': [
            {'texte': "“Biggest issue for S9 and shear keys, formworkers has no time to do it "
                      "if 1 shift” — flagged as a pain point, not resolved in the document.",
             'source': 'TEMPO_N2_presentation_CAS__BUF___May_26.pptx', 'statut': 'a_trancher'},
        ],
        'hypotheses': [], 'contradictions': [],
        'fichiers': ['STE__TEMPO__N3_Takt_Plan__V0_1.xlsx', 'TEMPO_N2_presentation_CAS__BUF___May_26.pptx'],
    },
    'P/U Point': {
        'aire': 'Production Hall', 'lettre_origine': 'R', 'phases': [('Q', 9), ('M', 8), ('N', 8),
            ('O', 8), ('S', 8), ('P', 7), ('R', 7), ('U+K', 3), ('T', 1)], 'total_taches': 59,
        'donnees': [], 'hypotheses': [], 'contradictions': [],
        'fichiers': ['STE__TEMPO__N3_Takt_Plan__V0_1.xlsx'],
    },
    'Casting Pit': {
        'aire': 'Production Hall', 'lettre_origine': 'S', 'phases': [('L', 162), ('T', 153),
            ('M', 125), ('N', 123), ('P', 122), ('S', 120), ('R', 118), ('O', 114), ('Q', 114),
            ('U+K', 33)], 'total_taches': 1184,
        'donnees': [
            {'texte': "30h pour, with a 2h overlap between two casts on the same plant (32h "
                      "considered in some scheduling options).",
             'source': 'General_Tempo_Staggering.xlsx (sheet Casting Pattern)', 'statut': 'confirme'},
            {'texte': "6 batching plants (A1/A2/A3, B4/B5/B6) — B6 doesn't exist yet.",
             'source': 'General_Tempo_Staggering.xlsx (sheet Casting Pattern)', 'statut': 'confirme'},
            {'texte': "Casting crew headcount: 70 BC (current status) versus 85 BC previously "
                      "agreed — gap not explained in the document.",
             'source': 'TEMPO_N2_Presentation_Casting_Team_10062026.pptx', 'statut': 'a_trancher'},
            {'texte': "Manpower peak: 105 BC at standard peak, 117 BC at extreme peak (segment "
                      "S5, 3 times per cycle).", 'source': 'TEMPO_N2_Presentation_Casting_Team_10062026.pptx',
             'statut': 'confirme'},
            {'texte': "Reduction being considered from 5 to 4 workers per casting boom — quality "
                      "risk explicitly noted by the team itself (less vibration, thicker layers).",
             'source': 'TEMPO_N2_Presentation_Casting_Team_10062026.pptx', 'statut': 'provisoire'},
            {'texte': "9+1 week cycle (9 normal + 1 buffer/ghost).",
             'source': 'TEMPO_N2_Presentation_Casting_Team_10062026.pptx', 'statut': 'confirme'},
            {'texte': "Crane/duration ratio computed segment by segment (e.g. BS S1: duration 115 "
                      "for a 12h47 “Shift”; BS S2: duration 86 for 9h33) — in both cases, "
                      "duration ÷ 9 = the number of shift-hours shown. The sheet is therefore "
                      "built on a 9h-shift hypothesis, like the Rebar presentation — a second "
                      "document now points to 9h, against a single source each for 10h/8h/12h.",
             'source': 'Cranes_conclusions.xlsx (sheets Crane Time N1 and N2)', 'statut': 'provisoire'},
        ],
        'hypotheses': [
            {'texte': "Casting crew's shift system undecided: 3×8h or 2×12h (“No "
                      "shift system in place”). Governs the whole hourly grid of the "
                      "simulation engine.", 'a_valider_par': 'Casting Team', 'statut': 'a_trancher'},
            {'texte': "Actual casting duration under review: counted as 24h but insufficient once "
                      "Sundays are put back in (S2→S8: ~27h missing; S8→S9 and "
                      "S1→S2: ~51h missing). Study under way to move to 19.5h.",
             'a_valider_par': 'CAS/Buffer team (JSO)', 'statut': 'a_trancher'},
        ],
        'contradictions': [
            {'texte': "The simulation engine (tempo/moteur/goulots.py), on the BC resource in "
                      "zone S alone, now finds a peak of 95 people at once — close to the 105-117 "
                      "cited by the Casting Team (10-20% gap, versus the factor-2 previously "
                      "observed). This figure of 95 does not, however, reproduce the 228 found by "
                      "an earlier version of the engine on the same source files, cause not "
                      "identified (likely a file-version or simulated-horizon difference, not a "
                      "deliberate fix) — the two values (95 and the old 228) still need "
                      "reconciling with the Casting Team. See also the sitewide total across all "
                      "zones (1258, not comparable to 105-117 since it adds up every element "
                      "simultaneously in progress across its whole journey) — detail in "
                      "tempo/moteur/ARCHITECTURE.md.",
             'sources': ['tempo/moteur/goulots.py (computed)', 'TEMPO_N2_Presentation_Casting_Team_10062026.pptx']},
            {'texte': "N3 segments without detail found: S9 only — not compared to the official tracker.",
             'sources': ['STE__TEMPO__N3_Takt_Plan__V0_1.xlsx (computed)']},
        ],
        'fichiers': ['General_Tempo_Staggering.xlsx', 'STE__TEMPO__N3_Takt_Plan__V0_1.xlsx',
                     'TEMPO_N2_Presentation_Casting_Team_10062026.pptx',
                     'TEMPO_N2_presentation_CAS__BUF___May_26.pptx',
                     'Tempo_full_schedule_linked_V4_70_jour.mpp', 'Cranes_conclusions.xlsx'],
    },
    'R1': {
        'aire': 'Curing Hall', 'lettre_origine': 'T', 'phases': [('T', 32), ('N', 32), ('M', 30),
            ('O', 29), ('Q', 28), ('S', 28), ('P', 26), ('R', 26), ('U+K', 17), ('L', 4)],
        'total_taches': 252,
        'donnees': [
            {'texte': "The MS Project schedule confirms, for each of the 9 segments of an "
                      "element (“TE 01”), a “Casting” task pair (~1.5 day, "
                      "resource FLC WORKER) followed by “Pushing” (~0.35 day i.e. ~8h, "
                      "resource Skidding team) — the “push” that moves the element from "
                      "one position to the next on the casting line. This is the concrete "
                      "mechanism behind the skidding already mentioned in zone S.",
             'source': 'Tempo_full_schedule_linked_V4_70_jour.mpp (tasks Casting/Pushing TE 01 '
                       '-Segment 01 to 09)', 'statut': 'confirme'},
            {'texte': "The logistics team identified in the N3 workbook itself is “Skidding” "
                      "(a dedicated resource, ~44 load rows) — found almost exclusively in phases "
                      "T, U+K and L (R1/R2/R3), attached to the UNIT=Casting Pit and P/U Point "
                      "tasks found there. It's the same team as the “Skidding team” in "
                      "the MPP schedule (Casting/Pushing, Big Push) — the logistics of moving "
                      "elements from one position to another, not the upstream logistics "
                      "(trucks/deliveries, see LOGISTIQUE).",
             'source': 'STE__TEMPO__N3_Takt_Plan__V0_1.xlsx (computed, resource column) + '
                       'Tempo_full_schedule_linked_V4_70_jour.mpp', 'statut': 'confirme'},
        ],
        'hypotheses': [], 'contradictions': [],
        'fichiers': ['STE__TEMPO__N3_Takt_Plan__V0_1.xlsx', 'Tempo_full_schedule_linked_V4_70_jour.mpp'],
    },
    'R2': {
        'aire': 'Curing Hall', 'lettre_origine': 'U+K', 'phases': [('N', 56), ('R', 39), ('P', 34),
            ('T', 34), ('O', 33), ('U+K', 29), ('Q', 27), ('S', 27)], 'total_taches': 279,
        'donnees': [], 'hypotheses': [], 'contradictions': [],
        'fichiers': ['STE__TEMPO__N3_Takt_Plan__V0_1.xlsx'],
    },
    'R3': {
        'aire': 'Curing Hall', 'lettre_origine': 'L', 'phases': [('L', 59), ('O', 28), ('S', 11),
            ('Q', 10), ('T', 10), ('P', 9), ('R', 8), ('U+K', 5)], 'total_taches': 140,
        'donnees': [], 'hypotheses': [], 'contradictions': [],
        'fichiers': ['STE__TEMPO__N3_Takt_Plan__V0_1.xlsx'],
    },
    'OF1': {
        'aire': 'Outfitting Area', 'lettre_origine': 'A', 'phases': [('L', 17), ('S', 14),
            ('T', 13), ('P', 11), ('R', 8), ('Q', 7), ('U+K', 5)], 'total_taches': 75,
        'donnees': [
            {'texte': "The outfitting MS Project schedule details, by segment (S1 to S9) and by "
                      "element (“TE 01”), a large volume of tasks: crack repairs and "
                      "concrete rework (int./ext.), fire protection, joint sealing (“ALL "
                      "tubes patching”, waterstop injection), electrical networks and "
                      "cabling, lighting, cathodic protection, realignment system, GINA, and "
                      "post-tension (see below) — 631 tasks in total for a single element.",
             'source': 'Tempo_full_schedule_linked_V4_70_jour.mpp', 'statut': 'confirme'},
            {'texte': "Mechanism clarified (08/11/2026): zones N1/N2/N3 are inside the "
                      "hall (after casting, before the element extends beyond the hall); "
                      "OF1-OF5 are the positions outside the hall; UB is the position after "
                      "the big push. S1 to S9 are segments of the element being produced "
                      "(not zones or phase letters): once produced, segment S1 is pushed "
                      "successively into N1, then N2, and so on up to OF5; segment S2 "
                      "follows the same path but stops at OF4. Once in position, the whole "
                      "element does the big push toward its final position, up to float-up.",
             'source': "confirmed directly by the project's user (08/11/2026)", 'statut': 'confirme'},
        ],
        'hypotheses': [
            {'texte': "The general mechanism (see Data above) is confirmed, but the full "
                      "correspondence still needs establishing: how many N1/N2/(N3?) "
                      "positions actually exist, which segment (S1 to S9) ends up in which "
                      "exact OF1-OF5/SG slot, and where the N1/N2/N3 zones themselves should "
                      "appear in this diagram (not shown yet — only OF1-OF5/SG and "
                      "UB-S9/S8/S7 are represented). A general site plan, announced by the "
                      "user, should help settle this.",
             'a_valider_par': 'Valery Claise / Joanna', 'statut': 'a_trancher'},
        ],
        'contradictions': [
            {'texte': "Corrected 08/10/2026 — this phase is NOT empty in the N3 workbook "
                      "(it carries 85 to 94 real tasks, see the real breakdown under Data): "
                      "the old claim of “no detailed task” relied on the mistaken reading of "
                      "this letter as the Outfitting Area/OF1-OF5 zone. Its tasks are actually "
                      "mostly attached to Base Slab/LASCA/Walls/Buffer, not to Outfitting. "
                      "Clarified 08/11/2026: this isn't a data gap, it's consistent — phases A "
                      "to I are in fact armature-preparation phases (confirmed by the user), "
                      "so attaching this letter to an OF1-OF5/SG slot (inherited from the Data "
                      "sheet, never reliable) was simply wrong. The correspondence with the "
                      "outfitting MPP schedule still needs establishing precisely (see "
                      "hypothesis).",
             'sources': ['STE__TEMPO__N3_Takt_Plan__V0_1.xlsx (computed, 08/10/2026)',
                         "confirmed directly by the project's user (08/11/2026)"]},
        ],
        'fichiers': ['STE__TEMPO__N3_Takt_Plan__V0_1.xlsx', 'Tempo_full_schedule_linked_V4_70_jour.mpp'],
    },
    'OF2': {
        'aire': 'Outfitting Area', 'lettre_origine': 'B', 'phases': [('T', 5), ('L', 5),
            ('U+K', 3), ('Q', 2)], 'total_taches': 15,
        'donnees': [
            {'texte': "The outfitting MS Project schedule details, by segment (S1 to S9) and by "
                      "element (“TE 01”), a large volume of tasks: crack repairs and "
                      "concrete rework (int./ext.), fire protection, joint sealing (“ALL "
                      "tubes patching”, waterstop injection), electrical networks and "
                      "cabling, lighting, cathodic protection, realignment system, GINA, and "
                      "post-tension (see below) — 631 tasks in total for a single element.",
             'source': 'Tempo_full_schedule_linked_V4_70_jour.mpp', 'statut': 'confirme'},
            {'texte': "Mechanism clarified (08/11/2026): zones N1/N2/N3 are inside the "
                      "hall (after casting, before the element extends beyond the hall); "
                      "OF1-OF5 are the positions outside the hall; UB is the position after "
                      "the big push. S1 to S9 are segments of the element being produced "
                      "(not zones or phase letters): once produced, segment S1 is pushed "
                      "successively into N1, then N2, and so on up to OF5; segment S2 "
                      "follows the same path but stops at OF4. Once in position, the whole "
                      "element does the big push toward its final position, up to float-up.",
             'source': "confirmed directly by the project's user (08/11/2026)", 'statut': 'confirme'},
        ],
        'hypotheses': [
            {'texte': "The general mechanism (see Data above) is confirmed, but the full "
                      "correspondence still needs establishing: how many N1/N2/(N3?) "
                      "positions actually exist, which segment (S1 to S9) ends up in which "
                      "exact OF1-OF5/SG slot, and where the N1/N2/N3 zones themselves should "
                      "appear in this diagram (not shown yet — only OF1-OF5/SG and "
                      "UB-S9/S8/S7 are represented). A general site plan, announced by the "
                      "user, should help settle this.",
             'a_valider_par': 'Valery Claise / Joanna', 'statut': 'a_trancher'},
        ],
        'contradictions': [
            {'texte': "Corrected 08/10/2026 — this phase is NOT empty in the N3 workbook "
                      "(it carries 85 to 94 real tasks, see the real breakdown under Data): "
                      "the old claim of “no detailed task” relied on the mistaken reading of "
                      "this letter as the Outfitting Area/OF1-OF5 zone. Its tasks are actually "
                      "mostly attached to Base Slab/LASCA/Walls/Buffer, not to Outfitting. "
                      "Clarified 08/11/2026: this isn't a data gap, it's consistent — phases A "
                      "to I are in fact armature-preparation phases (confirmed by the user), "
                      "so attaching this letter to an OF1-OF5/SG slot (inherited from the Data "
                      "sheet, never reliable) was simply wrong. The correspondence with the "
                      "outfitting MPP schedule still needs establishing precisely (see "
                      "hypothesis).",
             'sources': ['STE__TEMPO__N3_Takt_Plan__V0_1.xlsx (computed, 08/10/2026)',
                         "confirmed directly by the project's user (08/11/2026)"]},
        ],
        'fichiers': ['STE__TEMPO__N3_Takt_Plan__V0_1.xlsx', 'Tempo_full_schedule_linked_V4_70_jour.mpp'],
    },
    'OF3': {
        'aire': 'Outfitting Area', 'lettre_origine': 'C', 'phases': [('R', 7), ('L', 6)],
        'total_taches': 13,
        'donnees': [
            {'texte': "The outfitting MS Project schedule details, by segment (S1 to S9) and by "
                      "element (“TE 01”), a large volume of tasks — 631 tasks in total "
                      "for a single element (crack repairs, fire protection, networks, cathodic "
                      "protection, post-tension...).",
             'source': 'Tempo_full_schedule_linked_V4_70_jour.mpp', 'statut': 'confirme'},
            {'texte': "Mechanism clarified (08/11/2026): zones N1/N2/N3 are inside the "
                      "hall (after casting, before the element extends beyond the hall); "
                      "OF1-OF5 are the positions outside the hall; UB is the position after "
                      "the big push. S1 to S9 are segments of the element being produced "
                      "(not zones or phase letters): once produced, segment S1 is pushed "
                      "successively into N1, then N2, and so on up to OF5; segment S2 "
                      "follows the same path but stops at OF4. Once in position, the whole "
                      "element does the big push toward its final position, up to float-up.",
             'source': "confirmed directly by the project's user (08/11/2026)", 'statut': 'confirme'},
        ],
        'hypotheses': [
            {'texte': "The general mechanism (see Data above) is confirmed, but the full "
                      "correspondence still needs establishing: how many N1/N2/(N3?) "
                      "positions actually exist, which segment (S1 to S9) ends up in which "
                      "exact OF1-OF5/SG slot, and where the N1/N2/N3 zones themselves should "
                      "appear in this diagram (not shown yet — only OF1-OF5/SG and "
                      "UB-S9/S8/S7 are represented). A general site plan, announced by the "
                      "user, should help settle this.",
             'a_valider_par': 'Valery Claise / Joanna', 'statut': 'a_trancher'},
        ],
        'contradictions': [
            {'texte': "Corrected 08/10/2026 — this phase is NOT empty in the N3 workbook "
                      "(it carries 85 to 94 real tasks, see the real breakdown under Data): "
                      "the old claim of “no detailed task” relied on the mistaken reading of "
                      "this letter as the Outfitting Area/OF1-OF5 zone. Its tasks are actually "
                      "mostly attached to Base Slab/LASCA/Walls/Buffer, not to Outfitting. "
                      "Clarified 08/11/2026: this isn't a data gap, it's consistent — phases A "
                      "to I are in fact armature-preparation phases (confirmed by the user), "
                      "so attaching this letter to an OF1-OF5/SG slot (inherited from the Data "
                      "sheet, never reliable) was simply wrong. The correspondence with the "
                      "outfitting MPP schedule still needs establishing precisely (see "
                      "hypothesis).",
             'sources': ['STE__TEMPO__N3_Takt_Plan__V0_1.xlsx (computed, 08/10/2026)',
                         "confirmed directly by the project's user (08/11/2026)"]},
        ],
        'fichiers': ['STE__TEMPO__N3_Takt_Plan__V0_1.xlsx', 'Tempo_full_schedule_linked_V4_70_jour.mpp'],
    },
    'OF4': {
        'aire': 'Outfitting Area', 'lettre_origine': 'D', 'phases': [('S', 4), ('R', 1), ('L', 1)],
        'total_taches': 6,
        'donnees': [
            {'texte': "The outfitting MS Project schedule details, by segment (S1 to S9) and by "
                      "element (“TE 01”), a large volume of tasks — 631 tasks in total "
                      "for a single element.",
             'source': 'Tempo_full_schedule_linked_V4_70_jour.mpp', 'statut': 'confirme'},
            {'texte': "Mechanism clarified (08/11/2026): zones N1/N2/N3 are inside the "
                      "hall (after casting, before the element extends beyond the hall); "
                      "OF1-OF5 are the positions outside the hall; UB is the position after "
                      "the big push. S1 to S9 are segments of the element being produced "
                      "(not zones or phase letters): once produced, segment S1 is pushed "
                      "successively into N1, then N2, and so on up to OF5; segment S2 "
                      "follows the same path but stops at OF4. Once in position, the whole "
                      "element does the big push toward its final position, up to float-up.",
             'source': "confirmed directly by the project's user (08/11/2026)", 'statut': 'confirme'},
        ],
        'hypotheses': [
            {'texte': "The general mechanism (see Data above) is confirmed, but the full "
                      "correspondence still needs establishing: how many N1/N2/(N3?) "
                      "positions actually exist, which segment (S1 to S9) ends up in which "
                      "exact OF1-OF5/SG slot, and where the N1/N2/N3 zones themselves should "
                      "appear in this diagram (not shown yet — only OF1-OF5/SG and "
                      "UB-S9/S8/S7 are represented). A general site plan, announced by the "
                      "user, should help settle this.",
             'a_valider_par': 'Valery Claise / Joanna', 'statut': 'a_trancher'},
        ],
        'contradictions': [
            {'texte': "Corrected 08/10/2026 — this phase is NOT empty in the N3 workbook "
                      "(it carries 85 to 94 real tasks, see the real breakdown under Data): "
                      "the old claim of “no detailed task” relied on the mistaken reading of "
                      "this letter as the Outfitting Area/OF1-OF5 zone. Its tasks are actually "
                      "mostly attached to Base Slab/LASCA/Walls/Buffer, not to Outfitting. "
                      "Clarified 08/11/2026: this isn't a data gap, it's consistent — phases A "
                      "to I are in fact armature-preparation phases (confirmed by the user), "
                      "so attaching this letter to an OF1-OF5/SG slot (inherited from the Data "
                      "sheet, never reliable) was simply wrong. The correspondence with the "
                      "outfitting MPP schedule still needs establishing precisely (see "
                      "hypothesis).",
             'sources': ['STE__TEMPO__N3_Takt_Plan__V0_1.xlsx (computed, 08/10/2026)',
                         "confirmed directly by the project's user (08/11/2026)"]},
        ],
        'fichiers': ['STE__TEMPO__N3_Takt_Plan__V0_1.xlsx', 'Tempo_full_schedule_linked_V4_70_jour.mpp'],
    },
    'OF5': {
        'aire': 'Outfitting Area', 'lettre_origine': 'E', 'phases': [('T', 5)], 'total_taches': 5,
        'donnees': [
            {'texte': "The outfitting MS Project schedule details, by segment (S1 to S9) and by "
                      "element (“TE 01”), a large volume of tasks — 631 tasks in total "
                      "for a single element.",
             'source': 'Tempo_full_schedule_linked_V4_70_jour.mpp', 'statut': 'confirme'},
            {'texte': "Mechanism clarified (08/11/2026): zones N1/N2/N3 are inside the "
                      "hall (after casting, before the element extends beyond the hall); "
                      "OF1-OF5 are the positions outside the hall; UB is the position after "
                      "the big push. S1 to S9 are segments of the element being produced "
                      "(not zones or phase letters): once produced, segment S1 is pushed "
                      "successively into N1, then N2, and so on up to OF5; segment S2 "
                      "follows the same path but stops at OF4. Once in position, the whole "
                      "element does the big push toward its final position, up to float-up.",
             'source': "confirmed directly by the project's user (08/11/2026)", 'statut': 'confirme'},
        ],
        'hypotheses': [
            {'texte': "The general mechanism (see Data above) is confirmed, but the full "
                      "correspondence still needs establishing: how many N1/N2/(N3?) "
                      "positions actually exist, which segment (S1 to S9) ends up in which "
                      "exact OF1-OF5/SG slot, and where the N1/N2/N3 zones themselves should "
                      "appear in this diagram (not shown yet — only OF1-OF5/SG and "
                      "UB-S9/S8/S7 are represented). A general site plan, announced by the "
                      "user, should help settle this.",
             'a_valider_par': 'Valery Claise / Joanna', 'statut': 'a_trancher'},
        ],
        'contradictions': [
            {'texte': "Corrected 08/10/2026 — this phase is NOT empty in the N3 workbook "
                      "(it carries 85 to 94 real tasks, see the real breakdown under Data): "
                      "the old claim of “no detailed task” relied on the mistaken reading of "
                      "this letter as the Outfitting Area/OF1-OF5 zone. Its tasks are actually "
                      "mostly attached to Base Slab/LASCA/Walls/Buffer, not to Outfitting. "
                      "Clarified 08/11/2026: this isn't a data gap, it's consistent — phases A "
                      "to I are in fact armature-preparation phases (confirmed by the user), "
                      "so attaching this letter to an OF1-OF5/SG slot (inherited from the Data "
                      "sheet, never reliable) was simply wrong. The correspondence with the "
                      "outfitting MPP schedule still needs establishing precisely (see "
                      "hypothesis).",
             'sources': ['STE__TEMPO__N3_Takt_Plan__V0_1.xlsx (computed, 08/10/2026)',
                         "confirmed directly by the project's user (08/11/2026)"]},
        ],
        'fichiers': ['STE__TEMPO__N3_Takt_Plan__V0_1.xlsx', 'Tempo_full_schedule_linked_V4_70_jour.mpp'],
    },
    'SG': {
        'aire': 'Outfitting Area', 'lettre_origine': 'F', 'phases': [('L', 7), ('M', 3), ('U+K', 3)],
        'total_taches': 13,
        'donnees': [
            {'texte': "The outfitting MS Project schedule details, by segment (S1 to S9) and by "
                      "element (“TE 01”), a large volume of tasks — 631 tasks in total "
                      "for a single element.",
             'source': 'Tempo_full_schedule_linked_V4_70_jour.mpp', 'statut': 'confirme'},
            {'texte': "Mechanism clarified (08/11/2026): zones N1/N2/N3 are inside the "
                      "hall (after casting, before the element extends beyond the hall); "
                      "OF1-OF5 are the positions outside the hall; UB is the position after "
                      "the big push. S1 to S9 are segments of the element being produced "
                      "(not zones or phase letters): once produced, segment S1 is pushed "
                      "successively into N1, then N2, and so on up to OF5; segment S2 "
                      "follows the same path but stops at OF4. Once in position, the whole "
                      "element does the big push toward its final position, up to float-up.",
             'source': "confirmed directly by the project's user (08/11/2026)", 'statut': 'confirme'},
        ],
        'hypotheses': [
            {'texte': "The general mechanism (see Data above) is confirmed, but the full "
                      "correspondence still needs establishing: how many N1/N2/(N3?) "
                      "positions actually exist, which segment (S1 to S9) ends up in which "
                      "exact OF1-OF5/SG slot, and where the N1/N2/N3 zones themselves should "
                      "appear in this diagram (not shown yet — only OF1-OF5/SG and "
                      "UB-S9/S8/S7 are represented). A general site plan, announced by the "
                      "user, should help settle this.",
             'a_valider_par': 'Valery Claise / Joanna', 'statut': 'a_trancher'},
        ],
        'contradictions': [
            {'texte': "Corrected 08/10/2026 — this phase is NOT empty in the N3 workbook "
                      "(it carries 85 to 94 real tasks, see the real breakdown under Data): "
                      "the old claim of “no detailed task” relied on the mistaken reading of "
                      "this letter as the Outfitting Area/OF1-OF5 zone. Its tasks are actually "
                      "mostly attached to Base Slab/LASCA/Walls/Buffer, not to Outfitting. "
                      "Clarified 08/11/2026: this isn't a data gap, it's consistent — phases A "
                      "to I are in fact armature-preparation phases (confirmed by the user), "
                      "so attaching this letter to an OF1-OF5/SG slot (inherited from the Data "
                      "sheet, never reliable) was simply wrong. The correspondence with the "
                      "outfitting MPP schedule still needs establishing precisely (see "
                      "hypothesis).",
             'sources': ['STE__TEMPO__N3_Takt_Plan__V0_1.xlsx (computed, 08/10/2026)',
                         "confirmed directly by the project's user (08/11/2026)"]},
        ],
        'fichiers': ['STE__TEMPO__N3_Takt_Plan__V0_1.xlsx', 'Tempo_full_schedule_linked_V4_70_jour.mpp'],
    },
    'UB-S9': {
        'aire': 'Upper Basin', 'lettre_origine': 'G', 'phases': [('O', 33), ('M', 28), ('N', 24),
            ('P', 23), ('U+K', 1), ('R', 1)], 'total_taches': 110,
        'donnees': [
            {'texte': "“Big Push” = the name given in the schedule to the movement of "
                      "the complete element toward the Upper Basin (tasks “TE 01 - Big Push "
                      "Start” then “TE 01 Movement to Upper Basin (Start of Big "
                      "Push)”, both carried by the Skidding team, one day apart in this V4 "
                      "version of the schedule). It's a milestone, not a duration task — the "
                      "element finishes all its outfitting (see zones OF1-SG) before this move.",
             'source': 'Tempo_full_schedule_linked_V4_70_jour.mpp', 'statut': 'confirme'},
            {'texte': "Post-tension (“PT Threading” 3.25d, “PT Stressing” "
                      "3.25d, “PT Grout” 2.5d, resource Dywidag) is scheduled after the "
                      "Big Push in this V4 version of the schedule — which would place this "
                      "operation in the Upper Basin rather than upstream, but that's only inferred "
                      "from the tasks' chronological order, not an explicit zone assignment in the "
                      "file.", 'source': 'Tempo_full_schedule_linked_V4_70_jour.mpp', 'statut': 'provisoire'},
            {'texte': "The end of the element's sequence in the schedule also covers: closing the "
                      "sliding gate, testing the GINA and the realignment system, ballast tank "
                      "water test, then floating (“Float-up”, “Float-Down”, "
                      "“Floating Gate closure”) — consistent with the Upper Basin as the "
                      "float-out area, but the correspondence with the UB-S9/S8/S7 codes "
                      "specifically isn't made (see hypothesis).",
             'source': 'Tempo_full_schedule_linked_V4_70_jour.mpp', 'statut': 'confirme'},
        ],
        'hypotheses': [
            {'texte': "The general mechanism (see Data above) is confirmed, but the full "
                      "correspondence still needs establishing: how many N1/N2/(N3?) "
                      "positions actually exist, which segment (S1 to S9) ends up in which "
                      "exact OF1-OF5/SG slot, and where the N1/N2/N3 zones themselves should "
                      "appear in this diagram (not shown yet — only OF1-OF5/SG and "
                      "UB-S9/S8/S7 are represented). A general site plan, announced by the "
                      "user, should help settle this.",
             'a_valider_par': 'Valery Claise / Joanna', 'statut': 'a_trancher'},
        ],
        'contradictions': [
            {'texte': "Corrected 08/10/2026 — this phase is NOT empty in the N3 workbook (50 "
                      "to 87 real tasks, see the real breakdown under Data), contrary to the "
                      "old claim of “no detailed task” which relied on the mistaken "
                      "reading of this letter as the Upper Basin/UB-S9-S7 zone. Its tasks are "
                      "actually mostly attached to LASCA/Base Slab/Walls, not to the Upper "
                      "Basin. Clarified 08/11/2026: consistent with phases A to I actually "
                      "covering armature preparation (confirmed by the user), so attaching "
                      "this letter to a UB-S9/S8/S7 slot (inherited from the Data sheet, never "
                      "reliable) was wrong. The correspondence with the outfitting MPP "
                      "schedule (Big Push, post-tension, floating — Data above) still needs "
                      "establishing precisely (see hypothesis).",
             'sources': ['STE__TEMPO__N3_Takt_Plan__V0_1.xlsx (computed, 08/10/2026)',
                         "confirmed directly by the project's user (08/11/2026)"]},
        ],
        'fichiers': ['STE__TEMPO__N3_Takt_Plan__V0_1.xlsx', 'Tempo_full_schedule_linked_V4_70_jour.mpp'],
    },
    'UB-S8': {
        'aire': 'Upper Basin', 'lettre_origine': 'H', 'phases': [], 'total_taches': 0,
        'donnees': [
            {'texte': "“Big Push” = the name given in the schedule to the movement of "
                      "the complete element toward the Upper Basin — a milestone, not a duration "
                      "task, carried by the Skidding team.",
             'source': 'Tempo_full_schedule_linked_V4_70_jour.mpp', 'statut': 'confirme'},
            {'texte': "Post-tension (Threading/Stressing/Grout, resource Dywidag) is scheduled "
                      "after the Big Push in this V4 schedule version — inferred from task order, "
                      "not an explicit zone assignment.",
             'source': 'Tempo_full_schedule_linked_V4_70_jour.mpp', 'statut': 'provisoire'},
            {'texte': "End-of-sequence tasks also cover: sliding gate closure, GINA and "
                      "realignment system tests, ballast tank water test, then floating — "
                      "consistent with the Upper Basin as the float-out area, correspondence with "
                      "UB-S9/S8/S7 codes not made.",
             'source': 'Tempo_full_schedule_linked_V4_70_jour.mpp', 'statut': 'confirme'},
        ],
        'hypotheses': [
            {'texte': "The general mechanism (see Data above) is confirmed, but the full "
                      "correspondence still needs establishing: how many N1/N2/(N3?) "
                      "positions actually exist, which segment (S1 to S9) ends up in which "
                      "exact OF1-OF5/SG slot, and where the N1/N2/N3 zones themselves should "
                      "appear in this diagram (not shown yet — only OF1-OF5/SG and "
                      "UB-S9/S8/S7 are represented). A general site plan, announced by the "
                      "user, should help settle this.",
             'a_valider_par': 'Valery Claise / Joanna', 'statut': 'a_trancher'},
        ],
        'contradictions': [
            {'texte': "Corrected 08/10/2026 — this phase is NOT empty in the N3 workbook (50 "
                      "to 87 real tasks, see the real breakdown under Data), contrary to the "
                      "old claim of “no detailed task” which relied on the mistaken "
                      "reading of this letter as the Upper Basin/UB-S9-S7 zone. Its tasks are "
                      "actually mostly attached to LASCA/Base Slab/Walls, not to the Upper "
                      "Basin. Clarified 08/11/2026: consistent with phases A to I actually "
                      "covering armature preparation (confirmed by the user), so attaching "
                      "this letter to a UB-S9/S8/S7 slot (inherited from the Data sheet, never "
                      "reliable) was wrong. The correspondence with the outfitting MPP "
                      "schedule (Big Push, post-tension, floating — Data above) still needs "
                      "establishing precisely (see hypothesis).",
             'sources': ['STE__TEMPO__N3_Takt_Plan__V0_1.xlsx (computed, 08/10/2026)',
                         "confirmed directly by the project's user (08/11/2026)"]},
        ],
        'fichiers': ['STE__TEMPO__N3_Takt_Plan__V0_1.xlsx', 'Tempo_full_schedule_linked_V4_70_jour.mpp'],
    },
    'UB-S7': {
        'aire': 'Upper Basin', 'lettre_origine': 'I', 'phases': [], 'total_taches': 0,
        'donnees': [
            {'texte': "“Big Push” = the name given in the schedule to the movement of "
                      "the complete element toward the Upper Basin — a milestone, not a duration "
                      "task, carried by the Skidding team.",
             'source': 'Tempo_full_schedule_linked_V4_70_jour.mpp', 'statut': 'confirme'},
            {'texte': "Post-tension (Threading/Stressing/Grout, resource Dywidag) is scheduled "
                      "after the Big Push in this V4 schedule version — inferred from task order, "
                      "not an explicit zone assignment.",
             'source': 'Tempo_full_schedule_linked_V4_70_jour.mpp', 'statut': 'provisoire'},
            {'texte': "End-of-sequence tasks also cover: sliding gate closure, GINA and "
                      "realignment system tests, ballast tank water test, then floating — "
                      "consistent with the Upper Basin as the float-out area, correspondence with "
                      "UB-S9/S8/S7 codes not made.",
             'source': 'Tempo_full_schedule_linked_V4_70_jour.mpp', 'statut': 'confirme'},
        ],
        'hypotheses': [
            {'texte': "The general mechanism (see Data above) is confirmed, but the full "
                      "correspondence still needs establishing: how many N1/N2/(N3?) "
                      "positions actually exist, which segment (S1 to S9) ends up in which "
                      "exact OF1-OF5/SG slot, and where the N1/N2/N3 zones themselves should "
                      "appear in this diagram (not shown yet — only OF1-OF5/SG and "
                      "UB-S9/S8/S7 are represented). A general site plan, announced by the "
                      "user, should help settle this.",
             'a_valider_par': 'Valery Claise / Joanna', 'statut': 'a_trancher'},
        ],
        'contradictions': [
            {'texte': "Corrected 08/10/2026 — this phase is NOT empty in the N3 workbook (50 "
                      "to 87 real tasks, see the real breakdown under Data), contrary to the "
                      "old claim of “no detailed task” which relied on the mistaken "
                      "reading of this letter as the Upper Basin/UB-S9-S7 zone. Its tasks are "
                      "actually mostly attached to LASCA/Base Slab/Walls, not to the Upper "
                      "Basin. Clarified 08/11/2026: consistent with phases A to I actually "
                      "covering armature preparation (confirmed by the user), so attaching "
                      "this letter to a UB-S9/S8/S7 slot (inherited from the Data sheet, never "
                      "reliable) was wrong. The correspondence with the outfitting MPP "
                      "schedule (Big Push, post-tension, floating — Data above) still needs "
                      "establishing precisely (see hypothesis).",
             'sources': ['STE__TEMPO__N3_Takt_Plan__V0_1.xlsx (computed, 08/10/2026)',
                         "confirmed directly by the project's user (08/11/2026)"]},
        ],
        'fichiers': ['STE__TEMPO__N3_Takt_Plan__V0_1.xlsx', 'Tempo_full_schedule_linked_V4_70_jour.mpp'],
    },
}

LOGISTIQUE_EN = {
    'nom': 'Upstream logistics — supply → storage (site zones, incl. Lyon/Brest) → halls',
    'donnees': [
        {'texte': "35,345 parcels logged across 84 elements, with weight, supplier and delivery date.",
         'source': 'MASTERVIEW.xlsm (sheet ALL ELEMENTS)', 'statut': 'confirme'},
        {'texte': "912 deliveries planned, spread across the 5 production lines.",
         'source': 'MASTERVIEW.xlsm (sheet DeliveryPlan)', 'statut': 'confirme'},
        {'texte': "861 truck lots, 919 trucks in total, 4,204 tonnes.",
         'source': 'MASTERVIEW.xlsm (sheet LIST)', 'statut': 'confirme'},
        {'texte': "96 deliveries/day on average; a platform leaves roughly every 11 minutes.",
         'source': 'LAYOUT_RF.pptx + TRAILER_QUANTITY_PER_FLOW.xlsx', 'statut': 'confirme'},
        {'texte': "18h/day operating window (2 shifts).",
         'source': 'TRAILER_QUANTITY_PER_FLOW.xlsx', 'statut': 'confirme'},
        {'texte': "Recommended fleet for the Stock→Halls flow: 24 platforms (20% operating "
                  "margin included), based on an average logistics cycle of 3h40 measured by GPS "
                  "(SENSOLUS).",
         'source': 'TRAILER_QUANTITY_PER_FLOW.xlsx (sheet STOCK RF to HALL)', 'statut': 'confirme'},
        {'texte': "RF→Stock flow: 22 trucks/day; External→Stock: ~4 trucks/day; "
                  "Stock→Halls: 33 trucks/day (split across loading points Lyon 1/2/3, Brest 1/2).",
         'source': 'FLOW_BRESTLYON.pptx', 'statut': 'confirme'},
        {'texte': "789 of 830 deliveries (95.1%) need only one loading point; 41 (4.9%) need two "
                  "— the Shear Keys case, loaded at Lyon then completed at Sogod.",
         'source': 'EXCEPTIONS_TWO_STOPS_DELIVERIES.pptx, itself citing “Truck for All Sets '
                   '– V2, sheet LIST, column P”', 'statut': 'confirme'},
        {'texte': "Truck detail per loading point and origin (halls/RF/external) with handling "
                  "time: Lyon 1 = 14.5 trucks/6h40; Lyon 2 = 12 trucks/6h20 (but 13 in another "
                  "document, see contradiction); Lyon 3 = 8 trucks/3h20; Brest 1 = 10 trucks/3h25; "
                  "Brest 2 = 14.5 trucks/6h50 (but 12.5 in another document, see contradiction).",
         'source': 'Detailed_Truck__Loading_Time.xlsx', 'statut': 'confirme'},
        {'texte': "Trailer assignment plan per lot: e.g. BS segments 1-9 spread over 3 trailers "
                  "(trailer 1 = BS1,2,5 + 4 rows of U-profiles; trailer 2 = BS3,4; trailer 3 = the "
                  "rest); TS segment 5 over 6 trailers; TS segments 1-4/6-9 over 5 trailers.",
         'source': 'Trailer_Allocation_Plan.xlsx', 'statut': 'confirme'},
        {'texte': "Real weekly ESS schedule (week 18 and week 30/2026 samples): a grid in 2h "
                  "slots from 6h to 18h (6 slots/day, i.e. a 12h daily span), with deliveries "
                  "scheduled on Saturday in both samples.",
         'source': 'ESS_PLANNING.xlsx (sheets WEEK 18 and WEEK 19)', 'statut': 'confirme'},
        {'texte': "Formal RF logistics risk register, with frequency/impact/detection scored 1 to "
                  "5 and a criticality score: highest risk (score 50) = “insufficient "
                  "platforms for production supply”, proposed preventive action = a buffer of "
                  "3 to 5 extra trailers; second risk (score 40) = magnetic crane failure "
                  "(DCM/threading); third (score 36) = wind, no identified solution for now.",
         'source': 'TOPICS_RISK_ANALYSIS_SUB_ELEMENT_SIZIING.xlsx (sheet RISK ANALYSIS)',
         'statut': 'confirme'},
        {'texte': "Reserve platform sizing: max storage capacity 25 platforms in the halls, ~25 "
                  "platforms at RF (Julieto parking + buffer behind loose DCM); sized to P90 for "
                  "120 deliveries/day (1 platform ≈ 3-4 deliveries/day); detailed logistics "
                  "cycle = 40 min loading + 10 min transport to client + 3h wait + 40 min unloading "
                  "+ 10 min transport back to plant.",
         'source': 'TOPICS_RISK_ANALYSIS_SUB_ELEMENT_SIZIING.xlsx (sheet NUMBER PLATFORM)',
         'statut': 'provisoire'},
        {'texte': "Storage areas named after cities (Toulouse 800 m², Warsaw 580 m², "
                  "Lyon 3,440 m², Krakow, Monaco, Drogo) with floor area per element type and "
                  "associated handling equipment (PR14, PR51/52/53, Manitou, C1/C2, gantry crane).",
         'source': 'TOPICS_RISK_ANALYSIS_SUB_ELEMENT_SIZIING.xlsx (sheet MAX STORAGE) + '
                   'LIST_FLUX_ET_QUANTITE_MISE_EN_STOCK.xlsx', 'statut': 'confirme'},
    ],
    'hypotheses': [
        {'texte': "Lyon and Brest CONFIRMED (08/11/2026, directly by the project's user) as "
                  "zones ON SITE, not real geographic destinations — a general site plan "
                  "listing the other zones of the same kind should follow. Still likely but not "
                  "confirmed one by one: “Toulouse”, “Warsaw”, “Krakow”, “Monaco”, "
                  "“Drogo” and “Sogod” likely follow the same internal-code-name convention "
                  "for storage/loading areas on site — several of these same names already "
                  "denote storage areas alongside cities with clearly no geographic link to the "
                  "site (Drogo, Monaco), which supports this. To verify once the general plan "
                  "is received.",
             'a_valider_par': 'Valery Claise', 'statut': 'confirme'},
        {'texte': "Shift duration: 4 different values found depending on the document — 9h (Rebar "
                  "presentation, Cranes_conclusions.xlsx, AND Tempo_Walls.xlsx which literally has "
                  "columns “duration S3-S7 (shift 9h)” — 3 sources now converge on 9h), "
                  "10h (Truck_for_All_Set__V2, Hypotheses sheet — 1 source), 8h or 12h (Casting "
                  "Team, undecided — 1 source), and an N3 grid with ~4h45-5h windows matching none "
                  "of the three. 9h is becoming the best-supported hypothesis at this stage, but "
                  "still needs explicit confirmation — the single most structural point to settle "
                  "at the reconciliation meeting.",
             'a_valider_par': 'Olivier Bonnot (cross-cutting arbitration)', 'statut': 'a_trancher'},
        {'texte': "Rack name and count: “mesh” and “ESS” (08/10 meeting), "
                  "“White Rack” (MASTERVIEW.xlsm), “Yellow Rack” "
                  "(LAYOUT_RF.pptx). Two or three real types? Terminology to unify.",
             'a_valider_par': 'Valery Claise', 'statut': 'a_trancher'},
        {'texte': "Number of trailer parking spots: 13 (TRAILER_CAPACITY.pptx, one specific area) "
                  "versus 59 (LAYOUT_RF.pptx, “TOTAL”). Likely different scopes (a "
                  "sub-area vs. the site total) but unconfirmed.",
             'a_valider_par': 'logistics team', 'statut': 'a_trancher'},
    ],
    'contradictions': [
        {'texte': "Number of trucks per loading point: Lyon 2 = 12 trucks (Detailed_Truck) versus "
                  "13 (Quantity_Designation_Surface, sheet Truck Number); Brest 2 = 14.5 trucks "
                  "(Detailed_Truck) versus 12.5 (Quantity_Designation_Surface). Lyon 1, Lyon 3 and "
                  "Brest 1 agree between the two files. Clear gap on 2 of the 5 points, cause not "
                  "identified (different versions of the same calc?).",
             'sources': ['Detailed_Truck__Loading_Time.xlsx',
                          'Quantity_Designation_Surface.xlsx (sheet Truck Number)']},
        {'texte': "The real (dated) ESS schedule shows deliveries scheduled on Saturday — "
                  "consistent with the other weekend-work indicators already found in zones "
                  "Walls/Casting Pit (see REGISTRE_VALIDATION), but contradicts any “no "
                  "weekend work” hypothesis.",
             'sources': ['ESS_PLANNING.xlsx (sheets WEEK 18 and WEEK 19)']},
        {'texte': "The calibration hypothesis used so far for the engine (Ti = calendar day, Line "
                  "1 starts first) doesn't hold up against real dates: the earliest delivery date "
                  "per line in DeliveryPlan is, in order, Line 3 (05/08/2026), Line 2 (05/19), "
                  "Line 5 (05/20), Line 4 (06/01), Line 1 (06/25) — Line 1 is LAST, not first, "
                  "despite having the smallest N1 offset (T1). Likely explanation: these dates "
                  "only cover a window of the schedule (not each line's very first element), so "
                  "they don't allow direct calibration — but it invalidates a naive “earliest "
                  "delivery date” calibration, which was left untried for that reason.",
             'sources': ['MASTERVIEW.xlsm (sheet DeliveryPlan, computed)']},
        {'texte': "The number of deliveries/day recomputed directly from DeliveryPlan "
                  "(tempo/moteur/logistique.py) gives an average of 11.6/day and a peak of 22, far "
                  "below the “96 deliveries/day” cited elsewhere (LAYOUT_RF.pptx + "
                  "TRAILER_QUANTITY_PER_FLOW.xlsx) — roughly a factor of 8. Likely explanation: "
                  "DeliveryPlan (912 rows) only covers part of the total logistics flow (a "
                  "particular flow or time window), not the sitewide delivery total cited in the "
                  "96 figure — but this isn't confirmed.",
             'sources': ['MASTERVIEW.xlsm (sheet DeliveryPlan, computed via tempo/moteur/logistique.py)',
                          'LAYOUT_RF.pptx', 'TRAILER_QUANTITY_PER_FLOW.xlsx']},
    ],
    'fichiers': ['MASTERVIEW.xlsm', 'TRAILER_QUANTITY_PER_FLOW.xlsx', 'FLOW_BRESTLYON.pptx',
                 'LAYOUT_RF.pptx', 'TRAILER_CAPACITY.pptx', 'EXCEPTIONS_TWO_STOPS_DELIVERIES.pptx',
                 'Truck_for_All_Set__V2.xlsx', 'Detailed_Truck__Loading_Time.xlsx',
                 'Trailer_Allocation_Plan.xlsx', 'Quantity_Designation_Surface.xlsx',
                 'ESS_PLANNING.xlsx', 'TOPICS_RISK_ANALYSIS_SUB_ELEMENT_SIZIING.xlsx',
                 'LIST_FLUX_ET_QUANTITE_MISE_EN_STOCK.xlsx', 'JUSTIFICATION_STORAGE.pptx',
                 'Cranes_conclusions.xlsx',
                 'General_Tempo_Staggering_MDI_V5.xlsm (not yet processed beyond the HYPOTHESE PL sheet)',
                 'PROCESS.xlsx (empty file, no data)'],
}

EQUIPEMENTS_EN = [
    {'nom': 'Skidding team', 'type': 'internal logistics crew',
     'description': "Moves elements from one casting/curing position to the next "
                     "(“Pushing”), and the complete element to the Upper Basin "
                     "(“Big Push”). Identified both in N3 (dedicated resource, phases "
                     "T/U+K/L) and in the outfitting MPP schedule.",
     'zones': ['R1', 'R2', 'R3', 'Casting Pit', 'Upper Basin'],
     'source': 'STE__TEMPO__N3_Takt_Plan__V0_1.xlsx + Tempo_full_schedule_linked_V4_70_jour.mpp'},
    {'nom': 'Casting Pit cranes (count unspecified)', 'type': 'crane',
     'description': "The only zone where the N3 workbook documents crane-hours per task (185 of "
                     "3243 tasks, phases M to L only) — see the computed crane-utilization curve "
                     "in the schematic.",
     'zones': ['Casting Pit'], 'source': 'STE__TEMPO__N3_Takt_Plan__V0_1.xlsx (computed)'},
    {'nom': 'Base Slab crane(s)', 'type': 'crane', 'description': '1.5 crane assigned.',
     'zones': ['Base Slab'], 'source': 'TEMPO_N2_Presentation_Rebar_04062026.pptx + '
              'General_Tempo_Staggering_MDI_V5.xlsm'},
    {'nom': 'Top Slab crane(s)', 'type': 'crane', 'description': '2 cranes assigned.',
     'zones': ['Base Slab'], 'source': 'General_Tempo_Staggering_MDI_V5.xlsm (sheet Data base)'},
    {'nom': 'Special wall crane', 'type': 'crane', 'description': '1 crane dedicated to the walls.',
     'zones': ['Walls'], 'source': 'General_Tempo_Staggering_MDI_V5.xlsm (sheet Data base)'},
    {'nom': 'C1 / C2', 'type': 'crane', 'description': "RF storage cranes, capacities cited as "
                     "15.25 and 15.00 (unit unconfirmed) — see also the cap “no more than 2 "
                     "cranes for a top slab, 1 for a wall, 3 for two base slabs in the same "
                     "hall”.",
     'zones': ['Logistique'], 'source': 'Detailed_Truck__Loading_Time.xlsx + '
              'Explanations_Takt_time_files.pptx'},
    {'nom': 'Batching plants (6, one not yet built)', 'type': 'batching plant',
     'description': "A1/A2/A3, B4/B5/B6 — B6 doesn't exist yet.",
     'zones': ['Casting Pit'], 'source': 'General_Tempo_Staggering.xlsx (sheet Casting Pattern)'},
    {'nom': 'Platform/trailer fleet (24 recommended)', 'type': 'vehicle',
     'description': "Recommended sizing for the Stock→Halls flow, 20% operating margin "
                     "included — see also RF risk register item #1 (buffer of 3 to 5 trailers "
                     "proposed) and tempo/moteur/alea.py.",
     'zones': ['Logistique'], 'source': 'TRAILER_QUANTITY_PER_FLOW.xlsx (sheet STOCK RF to HALL)'},
    {'nom': 'Racks (mesh/ESS, White Rack, Yellow Rack — number of types unconfirmed)',
     'type': 'storage', 'description': "Three names found for what could be 2 or 3 real types — "
                     "see the validation register.",
     'zones': ['Logistique'], 'source': 'TEMPO meeting (08/10) + MASTERVIEW.xlsm + LAYOUT_RF.pptx'},
    {'nom': 'PR14 / PR51 / PR52 / PR53', 'type': 'handling equipment',
     'description': "Handling equipment cited for storage (Starter Bar, DCM panels) in the "
                     "storage areas named Toulouse/Sogod.",
     'zones': ['Logistique'], 'source': 'LIST_FLUX_ET_QUANTITE_MISE_EN_STOCK.xlsx'},
    {'nom': 'Manitou / Truck Mounted Crane', 'type': 'handling equipment',
     'description': "Cited for handling Niches, TO, EF (storage area named Krakow) and "
                     "Threading/Progress (area named Monaco/Toulouse).",
     'zones': ['Logistique'], 'source': 'LIST_FLUX_ET_QUANTITE_MISE_EN_STOCK.xlsx'},
    {'nom': 'Dywidag (post-tension)', 'type': 'subcontractor',
     'description': "PT Threading (3.25d), PT Stressing (3.25d), PT Grout (2.5d) — scheduled "
                     "after the Big Push per the MPP schedule's task order.",
     'zones': ['Upper Basin'], 'source': 'Tempo_full_schedule_linked_V4_70_jour.mpp'},
    {'nom': 'FLC WORKER', 'type': 'labor (BC FLC)',
     'description': "Resource for the per-segment “Casting” tasks in the MPP schedule "
                     "(~1.5 day/segment).", 'zones': ['Casting Pit'],
     'source': 'Tempo_full_schedule_linked_V4_70_jour.mpp'},
    {'nom': 'CEAS, GTA, Impostal, Sejerslev, Constructel, JD Steel, MSE, WL, BL',
     'type': 'subcontractor', 'description': "Subcontractor codes found in the N3 resource "
                     "columns. GTA = fire protection, MSE (typo for MSI) = ballast concrete — "
                     "decoded 08/11/2026, confirmed by the user. Decoding still incomplete for "
                     "WL (see the validation register).",
     'zones': ['toutes'], 'source': 'STE__TEMPO__N3_Takt_Plan__V0_1.xlsx (sheet Data) + '
              'Tempo_full_schedule_linked_V4_70_jour.mpp + '
              "confirmed directly by the project's user (08/11/2026, for GTA/MSE)"},
]

REGISTRE_VALIDATION_EN = [
    {'point': "QUASI-RESOLVED 08/10/2026. Recap: (1) the user directly confirmed that the letter "
              "codes (A to I/M to L) are PHASES, not physical zones; (2) a physical zone can be "
              "worked across SEVERAL phases. The exact mechanism was then found in "
              "General_Tempo_Staggering_MDI_V5.xlsm, sheet “70__63 - 1L - V0” (the "
              "70-day source template for one line): each letter marks a window of roughly 7 "
              "tempo days (T1 to T7) along an element's 70-day cycle — letter M even recurs at "
              "column 299 of that sheet, confirming the cycle repeats. Within each window, "
              "several UNIT rows (Walls, BS, LASCA, Buffer, CP...) carry a non-zero shift count "
              "at the same time — exactly what explains the mix found in "
              "ZONES_PHYSIQUES_REELLES/“Real breakdown”: several physical zones advance "
              "in parallel within the same time window. What's genuinely still open is the visual "
              "side: should the schematic (now organized by physical zone since the 08/10 update) "
              "also explicitly show this 7-day-window breakdown?",
     'zone': 'toutes', 'responsable': 'Valery Claise / Joanna',
     'impact': "medium — the mechanism is understood and documented; only a presentation "
               "question remains, no longer a data-reliability one"},
    {'point': "Casting crew's shift system (3×8h vs 2×12h)", 'zone': 'S',
     'responsable': 'Casting Team', 'impact': 'critical — governs the engine’s entire hourly grid'},
    {'point': "Shift duration diverging across documents — 9h now confirmed by 3 independent "
              "sources (Rebar, Cranes_conclusions.xlsx, Tempo_Walls.xlsx) against 1 each for 10h "
              "and 8h/12h; still needs official settling.", 'zone': 'Logistique',
     'responsable': 'Olivier Bonnot', 'impact': 'critical — same topic as above, seen from another angle'},
    {'point': "Gap between our reading of missing N3 segments and the official tracker "
              "(N3 Overview (Missing))", 'zone': 'N, O',
     'responsable': 'Valery Claise / Joanna', 'impact': 'high — determines where to focus the remaining scoping work'},
    {'point': "BC headcount peak in the Casting Pit zone: 95 with the current tool (close to the "
              "105-117 cited) vs. 228 found by an earlier version of the same calculation — cause "
              "of the gap between the two calculations not identified", 'zone': 'S',
     'responsable': 'Casting Team',
     'impact': 'medium — sharply down since the last measurement, to confirm rather than size against'},
    {'point': "Weekend work: hypothesis is “none” but four independent sources point to "
              "a real need (4 Saturdays/cycle for the walls, Sunday skidding on L4, L4's S2 "
              "skidding falls on a Saturday, ESS deliveries scheduled on Saturday in both "
              "available real-schedule samples)", 'zone': 'N, S, Logistique',
     'responsable': 'TEMPO team (global arbitration)', 'impact': 'high'},
    {'point': "Number and name of rack types (mesh/ESS vs White vs Yellow)", 'zone': 'Logistique',
     'responsable': 'Valery Claise', 'impact': 'medium'},
    {'point': "Wall installation order — nearly resolved: B,C,D,E,A,F found identically twice in "
              "General_Tempo_Staggering_MDI_V5.xlsm, more reliable than the “B-C-A-D-E-F” "
              "heard in the (noisy) meeting transcript. Just needs confirming in a meeting rather "
              "than re-deriving from scratch.", 'zone': 'Walls',
     'responsable': 'Valery Claise / Joanna', 'impact': 'low'},
    {'point': "Number of trucks at Lyon 2 (12 or 13) and Brest 2 (14.5 or 12.5) depending on the "
              "document", 'zone': 'Logistique', 'responsable': 'logistics team', 'impact': 'medium'},
    {'point': "PARTIALLY RESOLVED 08/11/2026: Lyon and Brest confirmed as ON-SITE zones (not real "
              "geographic destinations), directly by the user, who announced a general site plan "
              "listing the other zones of the same kind. Still open: "
              "Toulouse/Warsaw/Krakow/Monaco/Drogo/Sogod likely follow the same convention but "
              "aren't confirmed one by one yet — to check on the general plan once received.",
     'zone': 'Logistique', 'responsable': 'Valery Claise',
     'impact': 'medium — shapes the entire reading of the flows'},
    {'point': "RF risk register item #1 (score 50): insufficient platforms for production supply "
              "— proposed action (buffer of 3 to 5 trailers) to validate and cost out",
     'zone': 'Logistique', 'responsable': 'logistics team',
     'impact': 'high — a condition of the chosen fleet size (24 platforms)'},
    {'point': "NEARLY RESOLVED 08/11/2026: GTA (fire protection) and MSE/MSI (ballast concrete) "
              "decoded, confirmed directly by the user. Only WL remains open (“ask Lotte” — "
              "even the source doesn't know).",
     'zone': 'toutes', 'responsable': 'Lotte (for WL)',
     'impact': 'low — hinders reading, not the calculation'},
    {'point': "Number of trailer parking spots: 13 or 59 depending on the document (likely "
              "different scopes)", 'zone': 'Logistique', 'responsable': 'logistics team',
     'impact': 'low'},
    {'point': "MECHANISM CLARIFIED 08/11/2026 (user), exact correspondence still open. N1/N2/N3 "
              "= zones inside the hall (after casting, before the element extends beyond the "
              "hall); OF1-OF5 = positions outside the hall; UB = position after the big push. S1 "
              "to S9 are segments of the element, not zones: segment S1 is pushed successively "
              "into N1, N2, ... up to OF5; segment S2 stops at OF4. Still to establish: the exact "
              "number of N1/N2/(N3?) positions, the segment↔position detail for S3 to S9, and "
              "where to show the N1/N2/N3 zones in this diagram (absent for now — only "
              "OF1-OF5/SG and UB-S9/S8/S7 are represented). A general site plan, announced by "
              "the user, should help settle this.",
     'zone': 'Outfitting Area, Upper Basin', 'responsable': 'Valery Claise / Joanna',
     'impact': 'medium — needed to attach the 631 MPP tasks to a usable zone code'},
    {'point': "Deliveries/day recomputed from DeliveryPlan (11.6 average, peak 22) far below the "
              "96/day cited elsewhere — DeliveryPlan's scope (912 rows) needs clarifying: partial "
              "flow or partial time window?",
     'zone': 'Logistique', 'responsable': 'logistics team',
     'impact': 'high — governs fleet sizing if DeliveryPlan is to be used as the reference'},
]
