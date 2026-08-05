# Lolland Master Planner — Solveur de cadence & visualisation de planning

Outil web autonome (un seul fichier `index.html`, tout tourne dans le navigateur —
aucune donnée n'est envoyée sur un serveur) qui :

1. **calcule** les rythmes de production à appliquer sur chaque ligne (PL-1..PL-5),
   en partant du rythme actuel et de l'état d'avancement réel du chantier ;
2. **rejoue** la simulation jour par jour du flux complet ;
3. **affiche** le résultat visuellement sur le plan du site, avec un curseur temporel.

## Utilisation

1. Ouvrir `index.html` dans un navigateur (double-clic, ou glisser dans un onglet).
2. **Étape 1** — Charger l'image du plan du site. L'image reste locale.
3. **Étape 2** — Charger le classeur (`.xlsx` ou `.xlsm`, macros préservées).
4. **Étape 3** — Vérifier la date de référence (par défaut : aujourd'hui). C'est le
   « présent » du solveur : tout ce qui est renseigné comme en cours l'est à cette date.
5. **Étape 4** — Ajuster les durées fixes si besoin, puis **LANCER LE SOLVEUR**.
6. Parcourir le planning avec le curseur ou le bouton ▶, et exporter le résultat.

## Ce que fait le solveur

Pour chaque élément au moment où il entre en zone béton, le solveur teste les rythmes
autorisés **du plus lent (économique) au plus rapide** et retient le premier qui respecte
simultanément :

- **la pente d'inertie de la ligne** — 0,5 sem de variation tous les 4 mois maximum,
  mesurée depuis le dernier changement réellement appliqué sur cette ligne ;
- **les dates d'immersion de tout le reste de la file** de cette ligne, pas seulement
  celle de l'élément courant.

Ce second point est essentiel : ralentir un élément repousse mécaniquement tous ceux
qui attendent derrière lui. Regarder toute la file évite au solveur d'osciller
(accélérer / ralentir / réaccélérer) et divise par ~4 le nombre de changements de
cadence à faire appliquer aux opérateurs.

Rythmes autorisés : **1,0 / 1,5 / 2,0 / 2,5 / 3,0 / 3,5 / 4,0** semaines par segment.
Le rythme d'un élément est fixé à son lancement et ne change plus jusqu'à sa sortie.

Quand aucun rythme conforme à la pente ne permet de tenir les délais, le solveur retient
le plus rapide autorisé et émet une **alerte de délai** dans le rapport.

## Structure du classeur

| Onglet | Rôle |
|---|---|
| `Inputs` | Séquences de production. Colonnes B/D/F/H/J/L = PL-1..PL-5, SPE ; colonne A = ordre. Colonnes **C/E/G/I/K/M = statut as-built** (voir ci-dessous). Cellule `Seq2_Debut` en ligne 1/2 = bascule de séquence outfitting. |
| `Immersion` | `ID Element` / `Date Immersion` — les dates cibles que le solveur doit tenir. |
| `Config_Cycles` | **Colonnes B/C (Date Seuil 1 / Cycle 1) = le rythme actuel**, saisi par vous. Les colonnes D à I (Seuils 2-4 / Cycles 2-4) sont **ignorées en entrée** : c'est le solveur qui les calcule et les réinjecte à l'export. |
| `Config_SPE` | Les 7 zones de la ligne SPE (CPA→CP3 béton, UB1→UB3 outfitting). |
| `Config_Outfitting` | Phases d'outfitting, Séquence 1 et Séquence 2. |

### Format des statuts as-built (colonnes C/E/G/I/K/M de `Inputs`)

Le statut va dans la cellule **immédiatement à droite** de l'ID de l'élément, sur la
même ligne. Un élément sans statut est considéré comme non démarré (le solveur le
lancera quand la ligne se libère), **sauf** si sa date d'immersion est déjà passée :
il est alors déduit comme terminé.

| Code | Signification |
|---|---|
| `Beton:N` | En zone béton, au segment N (1 à 9). Lignes PL uniquement. |
| `Outfitting` | En zone outfitting. Lignes PL uniquement. |
| `Zone:N` | Ligne SPE uniquement : dans la zone N (1=CPA … 7=UB3). |
| `FloatUp` | En cours de float-up. |
| `Basin` | En Lower Basin (hook-up en cours). |
| `Parking` ou `Parking:N` | Au parking (place N si connue, sinon première libre). |
| `Ballast` | Au Ballast Jetty. |
| `Done` | Déjà immergé. |

Suffixe de date optionnel pour préciser le début réel de la phase :
`Beton:5:2026-06-15`. Sans date, la phase est réputée avoir commencé à la date de
référence. Un code non reconnu est signalé dans le journal et l'élément est traité
comme non démarré.

## Sorties

- **Rapport de cadence (CSV)** — une ligne par changement de rythme (ligne, date de
  bascule, ancien → nouveau rythme, élément déclencheur), suivi des alertes de délai
  et de la liste des éléments ratant leur date cible.
- **Classeur complet** — le fichier d'origine avec `Config_Cycles` mis à jour (les
  changements calculés réinjectés dans les slots 2 à 4) et un nouvel onglet
  `Solver_Report`. Les macros VBA sont préservées si l'entrée était un `.xlsm`.
- **KPI à l'écran** — nombre d'éléments ratant leur date d'immersion, retard maximum,
  fin de projet estimée, rythme courant par ligne.

## Logique de production simulée

`Béton (1 place/ligne)` → `Outfitting (1 place/ligne)` → `Float-up couplé
(PL1+2 / PL3+4 / PL5+SPE)` → `Lower Basin (3 bassins × 2 places, hook-up sur place)` →
`Parking (pool de 6 places, sauté si l'immersion arrive dans moins de N semaines)` →
`Ballast Jetty` → `Immersion`.

La ligne SPE suit une chaîne de 7 zones bloquantes avant de rejoindre le float-up
avec PL-5.

**Float-up et entrée en bassin sans partenaire** : les files des deux lignes d'un
groupe n'ont pas la même longueur (PL-5 compte 15 éléments, SPE 10). Quand la ligne
jumelle est épuisée, les derniers éléments partent seuls — sans cette règle ils
resteraient bloqués indéfiniment. Ces départs solo sont signalés dans le journal.

## Géométrie du plan (coordonnées relatives %, "pixel perfect")

| Repère | Valeur |
|---|---|
| Épaisseur (Y) | 2,21 % |
| Longueur standard (PL1-5) / spéciale (SPE) | 7,42 % / 1,66 % |
| X entrée (Est) → fin de halle → fin outfitting → bassin (Ouest) | 58,40 → 50,98 → 42,68 → 37,01 |
| Y PL-1 / PL-2 / PL-3 / PL-4 / PL-5 / SPE | 71,71 / 69,29 / 60,66 / 58,38 / 51,83 / 48,23 |
| Parking (épi -75°) | de [16,31 ; 80,97] à [10,25 ; 47,13] |

## Limites connues

- **Position du Ballast Jetty estimée.** Elle n'était pas fournie dans le cahier des
  charges ; elle est extrapolée depuis l'axe du parking (`GEO.ballast` dans
  `index.html`). À recalibrer si vous avez la position réelle.
- **Contrainte de flux tendu non modélisée.** La règle « l'élément N libère sa place
  d'outfitting quand N+1 atteint son 8ᵉ segment béton » n'est pas implémentée : le
  moteur libère la place à la fin de l'outfitting, comme la macro VBA d'origine.
- **`Config_Cycles` n'a que 3 slots de changement par ligne.** Si le solveur en produit
  davantage, les changements au-delà ne sont pas réinjectés dans cet onglet (un
  avertissement le signale) ; la liste complète reste dans `Solver_Report` et le CSV.
- **Le solveur est glouton, pas optimal au sens strict.** Il décide ligne par ligne au
  fil de l'eau, sans arbitrage global entre lignes concurrentes pour les ressources
  partagées (bassins, parking). C'est ce que décrit le cahier des charges, et cela
  suffit à produire un plan de cadence exploitable, mais ce n'est pas une optimisation
  sous contraintes au sens mathématique.
