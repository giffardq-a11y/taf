# Structure du moteur — état au démarrage

Ce document explique comment le moteur est construit, pourquoi il commence par cette
capacité précise plutôt qu'une autre, et ce qui est délibérément laissé de côté en
attendant que des questions encore ouvertes (`tempo/DONNEES.md` §4) soient tranchées.
Comme pour le reste du dépôt : rien n'est deviné pour combler un trou, un trou reste un
trou tant qu'il n'est pas comblé par une vraie donnée.

## Ce que le moteur sait faire aujourd'hui

**Calculer la charge de ressource agrégée, jour par jour, sur les 5 lignes en même
temps, et repérer où elle dépasse la capacité disponible.**

C'est le sous-ensemble directement disponible avec les données reçues à ce jour, et il
répond à deux des quatre objectifs posés au départ : détecter les goulots
d'étranglement, et vérifier que la cadence retenue est tenable avec les ressources
réelles. Les deux autres (générer un planning détaillé équipe par équipe, dimensionner
les ressources) en découlent directement une fois cette première brique posée — mais pas
avant, parce qu'un planning détaillé suppose de savoir **ordonnancer** les tâches
(dans quel ordre, avec quelle marge), et ça, on ne l'a pas encore construit (cf. plus
bas, "Ce qui n'est pas encore construit").

### Le principe

Le classeur N3 décrit, tâche par tâche, la charge horaire d'**un seul élément
générique** traversant les zones du site (colonne Élément = En/En-1/En+1, jamais liée à
une ligne précise — vérifié en lisant `lire_tempo.lire_taches_n3`). Le classeur N1 donne
le **déphasage** entre les 5 lignes : chaque ligne démarre son cycle à un jour tempo
absolu différent (`L1-T1`, `L2-T3`, `L3-T23`, `L4-T25`, `L5-T49`, lu dans
`lire_n1(...)['demarrage']`).

Le moteur recopie donc le même gabarit de tâches N3 sur les 5 lignes, en décalant
chacune de son déphasage, puis additionne la demande en ressource (effectif, heures de
grue) de toutes les lignes sur chaque jour calendaire absolu. Là où la somme dépasse la
capacité déclarée d'une ressource, c'est un goulot — daté, chiffré, et pointé vers les
tâches et lignes qui le causent, pas seulement signalé en bloc.

### Deux hypothèses posées ici, à confirmer avant de leur faire confiance sur un vrai cas

1. **Le jour tempo (« Ti ») est un jour calendaire, pas un poste.** Déduit du fait que le
   cycle complet dure 70 jours calendaires pour 140 postes (2 postes/jour), et que les
   feuilles N3 portent des Ti allant jusqu'à ~70 sur toute la traversée d'un élément.
   Cohérent avec les écarts de déphasage lus au N1 : L2-L1 = 2 jours, L4-L3 = 2 jours,
   L3-L2 = 20 jours, L5-L4 = 24 jours — un déphasage petit à l'intérieur d'une paire de
   lignes (même halle) et un grand déphasage entre paires, exactement la forme du
   déphasage entre halles déjà utilisé dans l'autre outil de ce dépôt (3 segments entre
   halles ≈ 21-24 jours tempo à raison d'environ 7 jours/segment) — une cohérence externe
   qui rassure, mais qui n'a pas été confirmée verbalement par Valery ou Joanna.
2. **Une ligne relance un nouvel élément tous les 7 jours tempo.** Déduit de la feuille
   `Casting Pattern` du classeur N1 (« Casting Pattern to fit **5 castings per week** »,
   une coulée par ligne et par semaine). Réglable
   (`ParametresCalage.periode_relance_jours`), pas codé en dur — mais la valeur par défaut
   suppose cette lecture juste.

Les deux hypothèses sont posées comme des **paramètres par défaut**, pas des constantes :
tout le module `modele.py` les expose, rien n'empêche de les corriger dès qu'une réponse
arrive.

## Ce qui n'est pas encore construit, et pourquoi

- **L'ordonnancement détaillé des tâches** (qui passe avant qui, avec quelle marge, sur
  quelle fenêtre horaire précise) — un problème d'ordonnancement sous contraintes de
  ressources (RCPSP dans la littérature de recherche opérationnelle), qui suppose de
  connaître les liens de précédence entre tâches. Le classeur N3 ne les porte pas
  explicitement (pas de colonne « prédécesseur ») ; les reconstruire à partir de l'ordre
  des lignes dans chaque feuille serait une supposition, pas une lecture. Reste à
  construire une fois soit ces liens obtenus (auprès de Joanna/Valery), soit une méthode
  de reconstruction validée sur un cas connu.
- **Le système de postes de l'équipe de coulée** (3×8h ou 2×12h — toujours « No shift
  system in place » d'après la présentation Casting Team) n'est pas figé dans le moteur :
  celui-ci raisonne en **heures continues**, jamais en « postes », précisément pour ne
  pas avoir à choisir à sa place. Le jour où le système de postes est arrêté, il
  s'ajoute comme un `Calendrier` (classe déjà prévue dans `modele.py`) sans toucher au
  reste.
- **La replanification à partir d'un avancement réel** (objectif final évoqué en
  réunion : réagir après chaque poste si on lui donne la progression). Suppose d'abord
  l'ordonnancement détaillé ci-dessus — sans lui, il n'y a rien de assez précis à
  comparer à un avancement réel.
- **La logistique amont, en partie construite.** `logistique.py` calcule désormais la
  charge de livraisons/jour depuis `MASTERVIEW.xlsm` (DeliveryPlan), avec de vraies dates
  calendaires — voir plus bas. Reste à faire : le rapprochement avec le fichier `LIST`
  (camions par lot, fenêtres relatives à la coulée plutôt que dates absolues — même
  hurdle de calage que `charge.py`), la prise en compte des racks/stockage comme
  ressource propre, et l'unification avec la charge de main-d'œuvre sur un seul axe
  temporel une fois le calage calendaire de celle-ci confirmé.
- **Les pannes matérielles et les retards, en partie construits.** Un vrai
  réordonnancement (reprendre un planning détaillé et le rejouer avec une ressource en
  moins ou une tâche en retard) suppose toujours l'ordonnancement détaillé ci-dessus,
  qui n'existe pas. Ce qui est construit à la place (`alea.py`) : une évaluation
  d'impact sur la charge déjà connue — perte de C unités pendant D jours, déficit que ça
  crée, tampon minimal pour l'absorber. Un premier niveau de réponse, pas la
  réaffectation à chaud complète évoquée en réunion — voir plus bas.

## Organisation des fichiers

```
tempo/moteur/
  ARCHITECTURE.md   ce document
  modele.py         les classes de données (Ressource, Tache, ParametresCalage, Calendrier)
  charge.py         construit la charge de main-d'œuvre agrégée, calée sur un jour tempo relatif
  goulots.py        diagnostic goulots : pic, récurrence, dépassement de capacité, et
                     le nombre d'équipes tournantes qu'impose chaque hypothèse de poste
  logistique.py     charge logistique (livraisons/camions) depuis MASTERVIEW.xlsm, calée
                     d'emblée sur de vraies dates calendaires — pas la même échelle de temps
                     que charge.py tant que le calage de celui-ci n'est pas confirmé
  alea.py           évalue l'impact d'une perte de capacité (retard/panne) sur une charge
                     déjà calculée — pas un réordonnancement, cf. plus bas
```

`python3 -m tempo.moteur.charge <n1.xlsx> <n3.xlsx>` fait tourner la charge seule.
`python3 -m tempo.moteur.goulots <n1.xlsx> <n3.xlsx> [--capacite CODE=VALEUR]` fait
tourner charge + diagnostic — pic, récurrence, dépassement si une capacité est fournie,
et le tableau équipes-tournantes selon la durée de poste. Un test de bout en bout sur
données réelles, pas seulement des classes qui compilent.

## Premier résultat, et un écart à éclaircir avant de s'y fier

> ⚠️ **Mise en garde ajoutée le 10/08/2026, après ce calcul** : les résultats « par zone »
> ci-dessous filtrent sur le code lettre de la feuille N3 (colonne « TEMPO »). Un contrôle
> croisé a montré que ce code lettre ne correspond pas de façon fiable à l'aire physique
> déclarée pour cette lettre dans la feuille `Data` (ex. aucune tâche du classeur n'est
> jamais étiquetée UNIT=« Panel Factory », alors que la lettre M est censée le désigner).
> La zone S reste le cas le plus proche d'une lecture correcte (51% de ses tâches sont
> bien UNIT=Casting Pit), donc le chiffre ci-dessous n'est pas à jeter, mais à prendre
> avec cette réserve — voir le point critique du registre de validation
> (`tempo/dossier_zones.py`) et `tempo/moteur/courbes.py`, qui regroupe désormais par la
> colonne UNIT (fiable) plutôt que par cette lettre.

Deux lectures possibles selon le périmètre, à ne pas confondre :

- **Zone S (Casting Pit) seule**, ressource `BC` (Blue Collar) : pic de **95** en
  simultané (`python3 -m tempo.moteur.goulots ... ` avec les charges filtrées sur
  `zone == 'S'`). Se rapproche du **105-117 BC** cité par la présentation Casting Team —
  l'écart est maintenant de l'ordre de 10 à 20%, pas un facteur 2.
- **Toutes zones confondues** (M à L, tout le parcours d'un élément), même ressource :
  pic de **1258** au jour 116, avec 1576 des 2058 points de charge au-dessus d'une
  capacité test de 85. Ce chiffre n'est **pas** comparable au 105-117 de la présentation
  Casting Team (qui ne couvre que l'équipe de coulée) — il additionne, à un instant
  donné, la main-d'œuvre BC de **tous les éléments simultanément en cours** sur les 5
  lignes, à tous les stades de leur parcours (Panel Factory à Curing Hall). Si le cycle
  complet dure effectivement ~70 jours calendaires et qu'un nouvel élément démarre tous
  les 7 jours par ligne (l'hypothèse `periode_relance_jours`), alors ~10 éléments sont
  simultanément « en vol » par ligne à l'état stationnaire — un fonctionnement en pipeline
  parfaitement normal pour ce type d'usine, mais qui donne un total sitewide sans commune
  mesure avec un pic mesuré zone par zone. Ce chiffre sitewide n'a encore été comparé à
  aucune donnée officielle de dimensionnement global — à faire.

Un écart persiste par rapport à la version précédente de ce document, qui citait un pic
de 228 en zone S : ce chiffre n'a pas été reproduit avec l'outil actuel (`goulots.py`),
qui donne 95 sur les mêmes fichiers sources. Cause non identifiée avec certitude — sans
doute une différence de version de fichier ou d'horizon simulé entre les deux calculs,
pas une correction volontaire. Les deux chiffres (95 et l'ancien 228) restent à
réconcilier avec Valery/Joanna avant de prendre l'un ou l'autre pour un dimensionnement
définitif — inscrit au registre de validation (`tempo/dossier_zones.py`).

## Impact de la durée de poste (registre de validation) sur le nombre d'équipes

Les fenêtres du classeur N3 tuilent la totalité des 24h de la journée (CP/PeP : 5
fenêtres d'environ 5h chacune ; PoP : 4 fenêtres de 6h) — la production tourne en
continu quelle que soit la durée de poste retenue. Ce que change la durée de poste,
c'est le nombre d'équipes distinctes nécessaires pour se relayer sur ces 24h
(`goulots.equipes_tournantes`, arrondi supérieur simple — pas une règle sociale) :

| Durée de poste | Équipes tournantes nécessaires |
|---|---|
| 8h | 3 |
| 9h | 3 |
| 10h | 3 |
| 12h | 2 |

Concrètement : retenir un poste de 12h plutôt que 8h/9h/10h réduit d'un tiers le nombre
d'équipes distinctes à constituer pour couvrir la même amplitude — un argument chiffré
de plus pour la réunion de conciliation sur ce point (`tempo/reunion_conciliation.md`),
qui ne tranche rien à sa place.

## Logistique : premier résultat, et un écart à réconcilier

`python3 -m tempo.moteur.logistique MASTERVIEW.xlsm`, sur les 912 livraisons de
`DeliveryPlan`, donne un pic de **22 livraisons/jour** (moyenne 11,6/jour) sitewide. En
retenant 3 à 4 livraisons par plateforme et par jour (milieu de fourchette 3,5, cité dans
`TOPICS_RISK_ANALYSIS_SUB_ELEMENT_SIZIING.xlsx`), ça correspondrait à environ **6
plateformes simultanées** au pic — très inférieur aux **24 plateformes** recommandées
dans `TRAILER_QUANTITY_PER_FLOW.xlsx` pour le seul flux Stock→Halls.

Cet écart n'est **pas** résolu ici : les deux chiffres ne couvrent probablement pas le
même périmètre (`DeliveryPlan` semble ne couvrir qu'une partie du flux total — voir aussi
l'écart similaire, facteur ~8, entre les 11,6/jour recalculés ici et les « 96
livraisons/jour » cités par ailleurs dans `LAYOUT_RF.pptx`), mais ce n'est pas confirmé.
Inscrit au registre de validation (`tempo/dossier_zones.py`) pour l'équipe logistique.

## Réponse à un aléa (`alea.py`) : premier scénario, pas un réordonnancement

`alea.py` répond à l'objectif « replanifier les ressources en cas de retard/casse
matériel », dans la limite de ce que le moteur permet aujourd'hui : **pas** un
réordonnancement (ça suppose l'ordonnancement détaillé tâche par tâche, toujours pas
construit), mais une évaluation d'impact — perte de C unités de capacité pendant D
jours à partir du jour J, sur une charge déjà calculée par `charge.py` ou
`logistique.py`. Le rapport distingue explicitement le déficit qui existait déjà sans
l'aléa (un aléa aggrave un problème préexistant, il ne le crée pas seul) du déficit
pendant l'incident, et donne le tampon minimal qui ramènerait ce dernier à zéro.

**Exemple sur le risque n°1 du registre RF officiel** (« plateformes insuffisantes »,
score 50/25, action proposée : tampon de 3 à 5 remorques — voir
`tempo/dossier_zones.py`, `LOGISTIQUE`) : en simulant la perte de 5 plateformes sur la
flotte de 24 recommandée, pendant la semaine du pic de livraisons observé dans
`DeliveryPlan` (22 livraisons le 25/06/2026), le déficit atteint jusqu'à **3**
plateformes/jour sur 3 jours consécutifs — la flotte recommandée n'absorbe donc pas
totalement la perte maximale envisagée dans le registre de risques, à ce niveau de
demande. Cette conclusion hérite cependant de la réserve posée plus haut : si
`DeliveryPlan` ne couvre bien qu'une fraction du flux réel (le facteur ~8 par rapport
aux « 96 livraisons/jour » cités ailleurs), la vraie exposition au risque est
probablement plus large que ce calcul ne le montre — à revérifier une fois cet écart
réconcilié.

```
python3 -m tempo.moteur.alea <n1.xlsx> <n3.xlsx> --ressource BC --zone S \
    --capacite 85 --perte 20 --jour-debut 90 --duree 10
```
