# 12. Annexes

## 12.1 Valeurs par défaut du modèle (`REGLES`, extrait de `index.html`)

Reproduction fidèle, à la date de ce dossier, de l'objet `REGLES` qui centralise
les règles et seuils du modèle. Toutes ces valeurs sont réglables depuis
l'interface (étape 6), sauf indication contraire.

| Clé | Valeur par défaut | Signification |
|---|---|---|
| `segments` | 9 | Segments béton d'un élément standard |
| `segmentsOutfitting` | 7 | L'outfitting s'achève au 7e segment de l'élément suivant |
| `rythmes` | `[4, 3.5, 3, 2.5, 2, 1.5, 1]` | Rythmes autorisés, en semaines/segment, du plus lent au plus rapide |
| `penteSem` | 1 | Variation de cadence autorisée… |
| `pentePeriodeMois` | 4 | …par tranche de 4 mois |
| `staggerHallB` | 3 | Segments de déphasage du hall B sur le hall A |
| `staggerPL5` | 7 | Idem pour PL-5, en préférence seulement (jamais bloquant) |
| `staggerCadenceDure` | 1 | Cadence (sem/segment) à partir de laquelle le déphasage devient contraignant |
| `etancheSem` | 12 | Fermeture provisoire d'un SPE, au plus tôt, après la sortie de CP3 |
| `etancheCritiqueSem` | 8 | Seuil critique, accessible sur autorisation explicite |
| `parkingPlaces` | 5 | Places de parking sans limite de durée |
| `parkingReserveJours` | 30 | La 6e place ne s'ouvre que pour un départ prévu sous ce délai |
| `basins` | 3 | Nombre de bassins |
| `basinPlaces` | 2 | Places par bassin |
| `arretAuPlusTot` | `true` | Vider les halles au plus tôt plutôt que produire à flux tendu |
| `accelererEnCoursCycle` | `false` | Accélérer sans attendre le prochain départ béton |
| `floatUpUnique` | `true` | Une seule paire de portes : un seul float-up à la fois |
| `vacances` | `true` | Arrêts annuels de l'usine |
| `noelSemaines` | 2 | Durée de l'arrêt de fin d'année (semaine du 25 décembre) |
| `paquesSemaines` | 1 | Durée de l'arrêt de semaine sainte |
| `bassinLibrePourFloatUp` | `true` | Ne pas lancer un float-up vers un bassin encore occupé |
| `jourCoulage` | `true` | Chaque ligne coule son jour, aux cadences entières uniquement |
| `joursCoulage` | `{1:1, 2:2, 3:3, 4:4, 5:5}` | Jour de la semaine par ligne (1 = lundi … 5 = vendredi) |
| `ballastJoursDefaut` | 7 | Repli interne (non réglable) pour un élément sans durée de ballast réelle (P6) |

## 12.2 Critères de l'optimiseur de séquence, dans l'ordre

1. Nombre d'éléments **bloqués** (non immergés en fin de simulation)
2. Nombre d'**inversions** entre ordre de production (lignes PL) et ordre
   d'immersion imposé
3. Nombre d'éléments **en retard** sur leur date cible
4. **Retard cumulé** (somme des retards, en jours)
5. **Retard maximal** (le plus grand retard individuel, en jours)
6. *(si stratégie « arrêt au plus tôt » active)* **Date de fin de production**
7. Nombre de **changements de cadence** à communiquer aux équipes

Comparaison lexicographique stricte : un critère ne départage deux séquences
candidates que si tous les critères précédents sont strictement à égalité.

## 12.3 Grille DCMA-14 — les 14 points de contrôle

Méthode de référence utilisée (avec adaptations) par `auditer_xer.py` pour
évaluer la qualité d'un planning Primavera P6. Les seuils indiqués sont ceux
généralement cités par la méthode d'origine — traités dans ce projet comme des
**repères**, pas comme des verdicts automatiques (un dépassement de seuil est
signalé et expliqué, jamais qualifié seul de « défaut »).

| # | Contrôle | Repère habituel |
|---|---|---|
| 1 | Extrémités ouvertes (activités sans prédécesseur ou sans successeur) | 0 (hors début/fin de projet) |
| 2 | Décalages positifs (lags) | ≤ 5 % des liens |
| 3 | Types de liens Fin→Début | ≥ 90 % des liens |
| 4 | Décalages négatifs (leads) | 0 |
| 5 | Contraintes dures | ≤ 5 % des activités |
| 6 | Marge totale élevée (> 44 j) | ≤ 5 % des activités non terminées |
| 7 | Marge négative | 0 |
| 8 | Durées élevées (> 44 j) | ≤ 5 % des tâches |
| 9 | Cohérence des dates réalisées vs date d'état | 0 anomalie |
| 10 | Activités sans ressource ni coût | à examiner (pas de seuil universel) |
| 11 | *(variante étendue dans ce projet)* Calendriers — cohérence capacité/durée journalière déclarée | 0 anomalie |
| 12 | Arborescence WBS — profondeur et nœuds sans activité | à examiner |
| 13 | Chemin déterminant (*critical path*) — proportion d'activités qui le portent | à examiner |
| 14 | Liens à décalage positif sur le chemin déterminant | 0 |

Résultat mesuré sur l'export de référence (86 Mo, 66 985 activités, 107 022
liens, 108 calendriers, traité en ~4 secondes) : densité de liens 1,60 par
activité (repère sain : 1,5 à 2,5) ; 86,7 % de liens Fin→Début ; 0,1 % de
contraintes dures ; 25,6 % des liens traversent deux calendriers différents (à
examiner au cas par cas, pas un défaut en soi) ; une anomalie de calendrier
détectée (préfixes `TUX-MAR-DPP+DO` et `TUX-MAR-TRW-TS`, 2000 h/an déclarées
sous deux durées journalières différentes, 8 h et 10 h — voir
`09_questions_ouvertes.md`, §9.1).

## 12.4 Sections de la page de restitution (`report_template.html`)

Liste, dans l'ordre d'apparition à l'écran, des sections fonctionnelles de la
page publiée :

1. Données de calcul (chargement, paramètres, date de référence)
2. Vue d'ensemble (indicateurs clés)
3. Conséquences des dates imposées *(affichée seulement si une imposition est active)*
4. Séquence de production *(classeur vs optimisée)*
5. Cadence par ligne dans le temps
6. Mouvement des éléments sur le site (plan animé)
7. Coupe du tunnel
8. Arrêt de l'usine
9. Changements de cadence à appliquer
10. Éléments manquant leur date cible
11. Écoulement de la production
12. Avancement des finitions
13. Planning d'occupation du site
14. Toutes les contraintes du modèle
15. Journal du calcul

## 12.5 Historique des commits significatifs (référence rapide)

Liste chronologique (du plus ancien au plus récent) des commits correspondant à
une décision documentée dans `04_journal_decisions_ADR.md`. Pour l'historique
complet, voir `git log` sur la branche `claude/staggering-sequence-optimizer-ot6zxr`
(67 commits au total à la date de ce dossier).

| Commit | Résumé | ADR associé |
|---|---|---|
| `db53837` | Add Lolland production planning visualizer | ADR-001 |
| `4089b51` | Take immersion dates from the P6 extract, and flag order inversions | ADR-005 |
| `a42fcd9` | Stop releasing the rate, and let the optimiser set line loads | ADR-006 |
| `1d39b7a` | Stop the factory early and progressively, and show the tunnel section in the report | ADR-007 |
| `433e38f` | Stagger the halls, and let the solver choose the production order | ADR-011, ADR-012 |
| `b6d321d` | Give the SPE line its storage area, and let the optimiser pick the line | ADR-009 |
| `574995a` | Drive the SPE line from the P6 schedule instead of fixed zone durations | ADR-008 |
| `5d14183` | Reach watertightness by cascade: clamping, then provisional, then critical | ADR-010 |
| `f431fcd` | Give each line its own casting day, and number the pours in the Gantt | ADR-015 |
| `dd425b7` | Let the two driving bars impose their date and re-run the solver | ADR-013 |
| `35c2357` | Report what an imposed date costs, against the run without one | ADR-014 |
| `da5651d` | Cast inside the halls, and show the SPE before the Upper Basin | ADR-017 |
| `6171450` | Refuse a float-up into an occupied basin | ADR-016bis |
| `aba5599` | Empty the basin as soon as a parking slot is free | ADR-016 |
| `c79a43c` | Draw the post-tensioning schedule from the solver's casting dates | ADR-018 |
| `9e411da` | Disable casting-day rule at intermediate rhythms; redraw post-tension as a classic Gantt | ADR-015 (correctif) |
| `688bc48` | Fix hook-up double-counting an element's basin dwell against its real ballast date | ADR-019 |

## 12.6 Références et documents complémentaires internes au dépôt

- `README.md` — documentation métier de référence, ~1100 lignes, près de
  40 sections thématiques.
- `SUITE.md` — note de reprise et journal de mesures, ~500 lignes.
- Fichiers sources cités tout au long de ce dossier : `index.html`,
  `report_template.html`, `build_report.py`, `planning_runner.js`,
  `post_tension.py`, `planning_cible.py`, `extraire_p6.py`,
  `reduire_classeur.py`, `lire_xer.py`, `auditer_xer.py`, `regles_p6.py`.

## 12.7 Références externes (méthodologies et formats, non fournies avec le dépôt)

- Méthode d'audit de planning **DCMA-14**, *Defense Contract Management Agency*
  (référence méthodologique publique, non embarquée dans ce dépôt).
- Format d'export **XER** de Primavera P6 (Oracle) — format tabulé documenté par
  l'éditeur, lu ici par un parseur maison (`lire_xer.py`), sans dépendance à un
  outil ou une bibliothèque Oracle.
- Modèle de planning de post-tension fourni par le sous-traitant **Dywidag**
  (fichier Excel transmis hors dépôt, `Dividag_tempo.xlsx` dans les échanges
  d'origine) — sert de gabarit visuel à `post_tension.py`.
