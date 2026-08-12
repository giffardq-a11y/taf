# Lolland Master Planner - version segmentaire béton

## Correction appliquée

Cette version corrige le calcul béton des lignes PL-1 à PL-5.

Avant, le moteur calculait la durée béton comme un bloc complet :

```js
rythme * 7 * 9
```

Maintenant, le moteur construit un planning segment par segment :

```js
segmentsBeton = [
  { no: 1, debut, fin, rythme, dureeJours },
  ...
  { no: 9, debut, fin, rythme, dureeJours }
]
```

## Arrondi option C

Les cycles avec demi-journées sont répartis par bornes cumulées arrondies.

Exemple pour 2,5 semaines par segment :

```text
2,5 semaines = 17,5 jours
segments : 18 / 17 / 18 / 17 / 18 / 17 / 18 / 17 / 18 jours
```

La moyenne du cycle reste respectée et les dates restent en jours entiers.

## Règles métier conservées

- PL-1 à PL-4 : la logique existante empêchant le ralentissement reste en place.
- PL-5 : le ralentissement reste autorisé comme dans le solveur actuel.
- La cadence reste fixée au lancement de l'élément et ne change pas pendant ses 9 segments.

## Correction du segment 7

La fin d'outfitting se base maintenant sur la vraie fin du segment 7 de l'élément suivant :

```js
finSegmentBeton(suiv, 7)
```

au lieu d'un calcul global approximatif.

## Correction as-built

La syntaxe :

```text
Beton:N
```

signifie que l'élément est dans le segment N.

La syntaxe :

```text
Beton:N:AAAA-MM-JJ
```

signifie que la date donnée est le début réel du segment N. Le solveur reconstitue ensuite les segments précédents.

## Push GitHub

Depuis le dossier du dépôt :

```powershell
git checkout claude/visual-production-planning-endu9v
copy /Y index.html index.backup.html
# Remplacer index.html par le fichier index.html fourni dans ce package
git add index.html README.md report_template.html
git commit -m "Corrige le calcul beton segment par segment"
git push origin claude/visual-production-planning-endu9v
```
