# TEMPO — note de données et d'hypothèses (ferraillage + logistique jusqu'au casting pit)

Ce document consolide tout ce qui a été reçu à ce jour pour le futur simulateur détaillé
casting + logistique (voir la conversation d'origine pour le cadrage : périmètre limité à
« usine → Rebar Hall → casting pit », hors intérieur usine, outil indépendant du solveur de
cadence existant mais pensé pour rester fusionnable avec lui plus tard).

Convention tenue tout du long : **chaque chiffre est tracé à sa source** et étiqueté
`[confirmé]` ou `[provisoire]`. Rien n'est mélangé sans dire d'où ça vient — c'est la même
discipline que sur le reste du dépôt (voir `dossier_audit/13_audit_critique.md`).

## 1. Sources reçues

| Source | Type | Auteur / date | Contenu |
|---|---|---|---|
| Réunion « TEMPO - Rebar & Logistic » | Transcription (Tactiq) | Olivier Bonnot, Valery Claise, Quentin Giffard-Bouvier — 10/08/2026 | Cadrage général, niveaux N1/N2/N3, priorité des ressources |
| `General_Tempo_Staggering.xlsx` | Classeur Excel, 15 feuilles | plusieurs versions V0-V4, dernière retenue datée 31/07/2026 (SFO) | Calage N1 : postes/segment par ligne et par catégorie, options de calage des centrales à béton |
| `STE__TEMPO__N3_Takt_Plan__V0_1.xlsx` | Classeur Excel, 31 feuilles | V0.1 (brouillon explicite) | Détail N3 : tâche par tâche, effectif par fenêtre horaire, 29 zones |
| `TEMPO_N2_Presentation_Rebar_04062026.pptx` | 11 diapositives | 04/06/2026 | Hypothèses ferraillage (BS/TS/Walls), écart avec le calage N1 |
| `TEMPO_N2_presentation_CAS_BUF_May26.pptx` | 9 diapositives | JSO — 29/05/2026 | Interférences Casting Pit ↔ Rebar, écarts de takt time |
| `TEMPO_N2_Presentation_Skidding_Pushing_09062026.pptx` | 6 diapositives | JAN — 09/06/2026 | Séquence détaillée du skidding, minute par minute |
| `TEMPO_N2_Presentation_PoP_260529.pptx` | 5 diapositives | 29/05/2026 | Post-Pour, essentiellement des graphiques (peu de texte extractible) |
| `TEMPO_N2_Presentation_Casting_Team_10062026.pptx` | 7 diapositives | 10/06/2026 | Effectif de l'équipe de coulée, pics de charge, système de postes non tranché |

## 2. Vue d'ensemble confirmée du système TEMPO

- **Trois niveaux** : N1 (calage haut niveau, postes par segment et par ligne, dates de
  coulée/poussage fixes), N2 (charge de ressource à l'entrée : tonnage, effectif, grue),
  N3 (le détail tâche par tâche, par zone, par fenêtre horaire — le classeur
  `STE__TEMPO__N3_Takt_Plan` que ce document décrit).
- **Découpage en zones**, chacune codée par une lettre (référentiel dans la feuille `Data`
  du classeur N3) : Panel Factory (M), Rebar Hall (N), Base Slab (O), **LASCA** (P — zone de
  la chaîne d'assemblage du ferraillage, confirmé par l'utilisateur), Buffer (Q), P/U Point
  (R), Casting Pit (S), zones de cure R1/R2/R3 (T, U+K, L), zones d'outfitting et Upper
  Basin (A à I).
- **Familles de tâches par zone** : `PeP` (préparation), `CP` (au casting pit), `PoP`
  (post-pour) — 29 feuilles au total dans le classeur N3, une par (famille × zone).
- **Grille horaire, différente selon la famille** (confirmé par lecture directe des
  en-têtes) :
  - `PeP` et `CP` : 5 fenêtres/jour — 6h-11h, 11h-15h45/16h, 16h-21h, 21h-1h45/2h, **2h-6h**
    (cette dernière explicitement marquée « OT » = hors tempo, une fenêtre tampon, pas une
    fenêtre normale — cohérent avec la réunion du 10/08).
  - `PoP` : 4 fenêtres/jour de 6h — 6h-12h, 12h-18h, 18h-24h, 0h-6h.
  - **Écart avec la présentation Rebar (04/06)** : elle décrit l'hypothèse de travail comme
    2 postes de 9h, 6h-15h et un second poste jusqu'à 3h du matin, avec **3h-6h** réservé
    à la livraison de matériel — pas 2h-6h. Les deux sources ne sont pas encore
    réconciliées ; à trancher avec Valery/Joanna avant de figer une grille horaire unique
    dans le simulateur. `[provisoire — à clarifier]`
- **Lien N1 ↔ N3, confirmé par l'utilisateur** : la somme des tâches N3 d'une catégorie,
  sur une fenêtre donnée, doit à peu près retomber sur le total de postes (`Ws`) de cette
  catégorie au niveau N1. Ce n'est pas une garantie stricte — les deux classeurs sont
  alimentés séparément — mais un repère de cohérence à vérifier.
- **Chaque colonne « Ω » du N3** (fin de ligne de tâche) semble être un total par tâche
  (à confirmer : possiblement homme×heures ou effectif cumulé) — colonne présente mais pas
  systématiquement renseignée dans ce brouillon V0.1.

## 3. Chiffres confirmés, exploitables maintenant

| Donnée | Valeur | Source |
|---|---|---|
| Durée d'une coulée | **30h**, avec 2h de recouvrement entre deux coulées sur la même centrale (32h envisagées dans certaines options) | `Casting Pattern`, classeur N1 |
| Nombre de centrales à béton | **6** : A1/A2/A3 (Factory A), B4/B5/B6 (Factory B) — **B6 n'existe pas encore** | `Casting Pattern` |
| Contrainte SPE | doit utiliser B4 + B5 (A3 trop loin) | `Casting Pattern` |
| Contrainte BCJ | doit utiliser A3 + une centrale « BP C » séparée | `Casting Pattern` |
| Règle de dégradation | en cas de retard cumulé sur la semaine, **L5 saute en premier** | `Casting Pattern` |
| Cycle global | 70 jours calendaires = 10 semaines tempo = 140 postes, 9 segments, 5 lignes en déphasage | classeur N1, cohérent avec la réunion |
| Effectif de base | 8 ouvriers (Base Slab, Top Slab) ; 6 pour les murs, en 4 équipes de 3 décalées, recouvrement jusqu'à 12h | présentation Rebar + réunion |
| Grues | **1,5 grue pour Base Slab, 2 grues pour Top Slab** | présentation Rebar (nouveau chiffre, absent de la réunion) |
| Cycle de coulée | **9+1 semaines** (9 normales + 1 semaine tampon/fantôme) | présentation Casting Team, cohérent avec la note « ghost week » du `Casting Pattern` |
| Effectif équipe de coulée | **70 BC (statut actuel) vs 85 BC (convenu précédemment)** — écart non résolu | présentation Casting Team |
| Pic de manpower coulée | **105 BC en pic standard, 117 BC en pic extrême (S5, 3 fois par cycle)** | présentation Casting Team |
| Boom de coulée | réduction envisagée de 5 à 4 ouvriers par boom — **risque qualité explicitement noté** (moins de vibration, couches plus grosses) | présentation Casting Team |
| Séquence skidding détaillée | 37 tâches élémentaires « skidding → LASCA » et « skidding → Buffer », chacune avec durée (minutes) et effectif — extraites intégralement, voir `lire_sequence_pptx_tableaux()` dans `lire_tempo.py` | présentation Skidding |
| Interférences Casting/Rebar | liste précise de tâches partagées : poutres de clavettes de cisaillement, réservations de niches, réservations murs B/C (S1-S3-S7-S9) et D/E (S1-S3-S5-S7-S9), joints Omega en table basculante, **grosse réservation tous les 10 éléments en S5** | présentation CAS & Buffer |
| Équipement partagé | même jeu de vérins (« jacks ») utilisé pour skidding-vers-LASCA et skidding-vers-Buffer — **ne peuvent donc pas se faire simultanément** | présentation Skidding |

## 4. Tensions et écarts non résolus — identifiés par l'équipe elle-même, pas par nous

Ces points ne sont **pas des incohérences que j'ai déduites** : ce sont des désaccords ou
des écarts explicitement notés dans les documents source, à trancher par l'équipe avant
qu'un simulateur puisse s'appuyer dessus sans ambiguïté.

- **Travail du week-end.** L'hypothèse de base (présentation Rebar) est « pas de travail
  samedi/dimanche ». Mais :
  - Le calage N1 réel exige **4 samedis pleins par cycle de 63 jours** pour les murs (calcul
    posé dans la présentation Rebar : 9 segments × 6 murs = 54, 63 jours - week-ends = 50
    jours ouvrés, 4 jours manquants).
  - La présentation Skidding note : « **Still Sunday skidding in N1 staggering** ».
  - La présentation Casting Team pose la question explicitement : « S2 skidding in L4 are
    Sat. and casting is Monday. **Works Sunday TO PREPARE?** »
  - Trois sources indépendantes pointent la même tension, non résolue.
- **Système de postes de l'équipe de coulée : pas encore décidé.** Diapositive « Risks »
  de la présentation Casting Team : « **No shift system in place** », deux options
  ouvertes : **3×8h** ou **2×12h**. Ce point est plus fondamental qu'il n'y paraît : la
  grille horaire à 5 fenêtres du classeur N3 (zone `CP`) est donc construite sur une
  hypothèse de travail, pas sur une décision arrêtée.
- **Durée de coulée elle-même encore en révision.** La présentation CAS & Buffer indique
  que les takt times actuels (comptés pour 24h) sont **en réalité insuffisants** une fois
  les dimanches réintégrés (S2→S8 : ~27h manquantes ; S8→S9 et S1→S2 : ~51h manquantes),
  et qu'une étude est en cours pour **refaire tous les takt times sur une base de 19,5h**
  plutôt que 24h. Un test de performance était planifié semaine 29 pour valider cette
  hypothèse sur la ligne 2, segment S5.
- **LASCA — signification confirmée par l'utilisateur** (zone de la chaîne d'assemblage
  du ferraillage), mais son articulation précise avec Base Slab/Top Slab dans le calage N1
  reste à valider une fois le lien N1↔N3 vérifié par le calcul (§2 ci-dessus).

## 5. Ce que `lire_tempo.py` extrait déjà

Script à `tempo/lire_tempo.py`. Trois fonctions principales :

```python
lire_reference(chemin_n3)                     # référentiel de codes (feuille Data)
lire_taches_n3(chemin_n3)                      # -> (taches, charges) : 3243 tâches, 12850 cases
                                                #    d'effectif sur les 29 feuilles PeP/CP/PoP
lire_n1(chemin_n1, feuille)                    # -> 25 entrées ligne×catégorie (postes/segment)
lire_sequence_pptx_tableaux(chemin_pptx, n)    # -> tableaux détaillés d'une diapositive
                                                #    (ex. les 37 tâches de skidding)
```

Exécuté en ligne de commande, le script imprime un résumé de contrôle (comptes, zones
couvertes, vérification N1) — voir `python3 tempo/lire_tempo.py --help`.

**Ce que le script ne fait pas encore** : rapprocher N1 et N3 pour vérifier leur cohérence
chiffrée (§2), ni transformer les cinq présentations en un référentiel unique de règles —
c'est la suite logique, une fois les points de la section 4 clarifiés (ou explicitement
mis en attente, comme cela a été fait pour la question des calendriers marins sur l'autre
projet du dépôt).

## 6. Prochaines étapes proposées

1. Faire trancher par l'équipe (Valery/Joanna) les points de la section 4, ou les
   documenter comme volontairement en attente si un arbitrage rapide n'est pas possible —
   en particulier le système de postes de l'équipe de coulée, qui conditionne toute la
   grille horaire du simulateur.
2. Rapprocher programmatiquement N1 et N3 (sommer les tâches N3 par catégorie/segment et
   comparer à `Ws` du N1) pour confirmer ou infirmer le lien décrit en §2 — un script
   court, dans l'esprit de `auditer_xer.py` sur l'autre projet.
3. Une fois ces deux points faits, commencer la conception du moteur de simulation
   lui-même (ressources, contraintes, replanification), sur des données dont on sait
   précisément ce qui est confirmé et ce qui ne l'est pas encore.
