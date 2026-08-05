# Lolland Master Planner — Visualisation de Planning

Outil web autonome (un seul fichier `index.html`, tout tourne dans le navigateur —
rien n'est envoyé sur un serveur) qui rejoue le moteur de simulation de la macro
VBA « Master Optimizer » et l'affiche visuellement sur le plan du site.

## Utilisation

1. Ouvrir `index.html` dans un navigateur (double-clic, ou glisser dans un onglet).
2. **Étape 1** — Charger l'image du plan du site (le fond de plan général ou la
   vue zoomée production/bassins/parking). L'image reste locale, elle n'est
   jamais uploadée nulle part.
3. **Étape 2** — Charger le classeur Excel (`.xlsx`). Onglets attendus, identiques
   à ceux lus par la macro VBA :
   - `Inputs` — séquences de production (colonnes B/D/F/H/J/L = PL-1..PL-5, SPE ;
     colonne A = ordre ; cellule `Seq2_Debut` en ligne 1 pour la bascule de séquence
     outfitting).
   - `Immersion` — `ID Element` / `Date Immersion`.
   - `Config_Cycles` (optionnel) — seuils de dates et rythmes (semaines/segment)
     par ligne PL-1..PL-5. Valeurs par défaut appliquées si absent.
   - `Config_SPE` (optionnel) — les 7 zones de la ligne SPE (CPA→CP3 béton,
     UB1→UB3 outfitting).
   - `Config_Outfitting` (optionnel) — les phases d'outfitting Séquence 1 / Séquence 2.
4. Ajuster les paramètres si besoin (date de début, seuil de saut du Parking,
   durées Float-up / Hook-up / Ballast).
5. Cliquer **LANCER LA SIMULATION**, puis utiliser le curseur ou le bouton ▶
   (lecture automatique) pour parcourir le planning jour par jour.

## Logique métier reproduite (fidèle à la macro VBA)

Cycle de vie par élément : `Béton (zone dédiée par ligne, 1 place)` →
`Outfitting (zone dédiée par ligne, 1 place)` → `Float-up couplé
(PL1+2 / PL3+4 / PL5+SPE, le plus rapide attend le plus lent)` →
`Lower Basin (3 bassins × 2 places, Hook-up sur place)` → `Parking (pool commun de
6 places, sauté si l'immersion arrive dans moins de N semaines)` → `Ballast
Jetty` → `Immersion (sortie définitive)`.

La ligne SPE suit une chaîne de 7 zones bloquantes (CPA→CP1→CP2→CP3 béton,
UB1→UB2→UB3 outfitting) avant de rejoindre le Float-up avec PL-5.

## Géométrie du plan (coordonnées relatives %, "pixel perfect")

Reprise telle que définie dans le cahier des charges :

| Repère | Valeur |
|---|---|
| Épaisseur (Y) | 2,21 % |
| Longueur standard (PL1-5) | 7,42 % |
| Longueur spéciale (SPE) | 1,66 % |
| X entrée (Est) | 58,40 |
| X fin de halle | 50,98 |
| X fin outfitting | 42,68 |
| X Lower Basin (Ouest) | 37,01 |
| Y PL-1 / PL-2 / PL-3 / PL-4 / PL-5 / SPE | 71,71 / 69,29 / 60,66 / 58,38 / 51,83 / 48,23 |
| Parking (épi -75°) | de [16,31 ; 80,97] à [10,25 ; 47,13] |

**Point non spécifié dans le cahier des charges** : la position du *Ballast
Jetty* n'était pas donnée. Elle est estimée par extrapolation de l'axe du
parking au-delà de son extrémité Ouest (`GEO.ballast` dans `index.html`,
~[8,43 ; 36,98]). À recalibrer si vous avez la position réelle.

## Limites connues

- Les contraintes d'**inertie de pente** (0,5 sem tous les 4 mois) et de
  **flux tendu Outfitting** (libération de la place N quand N+1 atteint son
  8ᵉ segment béton) décrites dans le dossier de référence ne sont **pas**
  auto-appliquées par le solveur : comme dans la macro VBA d'origine, c'est
  l'onglet `Config_Cycles` qui doit être renseigné en respectant ces règles
  (le moteur ne fait qu'exécuter le planning tel que configuré, il n'optimise
  pas les rythmes automatiquement). Si vous voulez un vrai solveur backward
  qui choisit les rythmes automatiquement (comme l'esquissait le prototype
  V13), c'est une évolution possible à ajouter séparément.
- Un élément est signalé **en retard** (bordure rouge pulsante) si la date du
  jour dépasse sa date d'immersion cible alors qu'il n'a pas encore atteint
  le statut Ballast — cela peut arriver si le Lower Basin reste saturé trop
  longtemps.
