# 1. Résumé exécutif

## Objectif du projet

Fournir à l'équipe de planification d'une usine de préfabrication d'éléments de tunnel
immergé un outil qui **calcule automatiquement la cadence de production à tenir sur
chaque ligne de fabrication**, rejoue jour par jour le déroulement complet de la
production (coulée béton → équipement → mise à flot → bassin → parking → ballast →
immersion), et **visualise** ce déroulement sur le plan réel du site, pour vérifier
que le plan tient les dates d'immersion imposées par le planning directeur du projet
(Primavera P6) sans recalculer ce planning à la main dans un tableur.

## Contexte

Le projet concerne la construction du **Fehmarnbelt**, une liaison fixe immergée
(route + rail) entre le Danemark (Lolland) et l'Allemagne, l'un des plus grands
tunnels immergés au monde. Les éléments de tunnel — de très grands caissons en béton
préfabriqués — sont coulés à l'usine de **Rødbyhavn (Lolland)**, puis mis à l'eau,
stockés temporairement, ballastés et enfin immergés un par un dans leur position
finale, dans l'ordre imposé par le planning directeur du chantier.

La production se répartit sur **6 lignes** :

- **5 lignes standards** (PL-1 à PL-5), regroupées par paires dans 2 halles de
  coulée (« Hall A » = PL-1/PL-2, « Hall B » = PL-3/PL-4), plus PL-5 seule ;
- **1 ligne spéciale (SPE)**, qui fabrique des éléments non standards (jonctions,
  éléments spéciaux) selon un cheminement différent, piloté par des zones nommées
  plutôt que par des segments de coulée.

Chaque élément standard se coule en **9 segments** successifs, puis passe par une
zone d'équipement (*outfitting*), avant d'être mis à flot (*float-up*) vers un
**bassin** (Basin A, B ou C — 3 bassins de 2 places chacun), d'y attendre son tour,
de rejoindre une place de **parking**, puis le **quai de ballastage** (Ballast
Jetty) où il est lesté puis immergé, dans un ordre imposé par le planning directeur.

Ce projet a démarré à partir d'un classeur Excel existant sur le chantier
(macro VBA de calcul de cadence) et d'un cahier des charges métier transmis
verbalement et par échanges itératifs avec le planificateur du chantier, formalisés
au fur et à mesure dans le code et dans `README.md`.

## Utilisateurs visés

- **Le ou les planificateurs de production de l'usine**, qui doivent décider et
  communiquer aux équipes la cadence à tenir sur chaque ligne, semaine après
  semaine, et vérifier qu'un scénario (état d'avancement réel, changement de
  paramètre, imposition d'une date) ne casse pas la tenue du planning directeur.
- **Les équipes support** qui préparent les plannings dérivés : post-tension
  (Dywidag), occupation du site au format *Target schedule*, suivi des travaux
  marins et des finitions.
- **Toute personne chargée d'auditer ou de faire évoluer le planning P6 lui-même**
  (jeu d'outils indépendant du solveur, voir plus bas).

Aucun rôle de type « exploitant final » ou grand public n'est visé : c'est un outil
métier interne, à diffusion restreinte à l'équipe planning.

## Problème résolu

Avant cet outil, la cadence de production et sa conformité aux dates d'immersion se
vérifiaient à la main, dans un classeur Excel piloté par une macro VBA figée, sans
simulation jour par jour du cheminement complet d'un élément (bassin, parking,
ballast), sans prise en compte simultanée de toutes les règles d'occupation des
ressources partagées (portes du site, places de bassin, places de parking, jalon
d'étanchéité de la ligne SPE), et sans moyen rapide de tester l'effet d'un
changement de paramètre ou d'une date imposée.

L'outil répond à trois besoins :

1. **Calculer** la cadence à tenir sur chaque ligne, en respectant à la fois la
   pente d'accélération physiquement tenable et les dates d'immersion de tous les
   éléments restants (pas seulement du prochain).
2. **Simuler** le déroulement complet, jour par jour, de tous les éléments à travers
   toutes les ressources partagées du site, pour détecter les blocages et les
   retards *avant* qu'ils ne se produisent sur le chantier.
3. **Visualiser** ce résultat de façon exploitable en réunion de planification :
   plan animé du site, Gantt de production, coupe longitudinale du tunnel,
   planning d'occupation imprimable, comparaison de scénarios.

## Valeur ajoutée

- **Détection précoce des blocages** : le solveur a mis en évidence, sur le
  classeur de référence, un verrou physique (un élément spécial bloquant
  37 autres éléments prêts derrière lui dans l'ordre d'immersion imposé) qu'une
  lecture manuelle du classeur n'avait pas révélé — voir `04_journal_decisions_ADR.md`
  et `13_audit_critique.md`.
- **Mesure systématique de l'effet de chaque règle et de chaque paramètre** : toute
  règle ajoutée au modèle est validée par une mesure chiffrée de son effet sur le
  nombre de retards, le retard cumulé et le retard maximal, avant d'être considérée
  comme acquise. Ce processus de mesure est documenté dans `README.md` et
  `SUITE.md`, et repris dans `04_journal_decisions_ADR.md`.
- **Autonomie du navigateur** : l'outil tourne entièrement dans le navigateur,
  sans serveur, sans envoi de données à un tiers — un point de conception
  déterminant pour un chantier qui manipule des données de planning
  potentiellement sensibles (voir `06_documentation_technique.md`).
- **Boîte à outils d'audit du planning directeur (P6)** indépendante du solveur,
  capable de traiter un export XER de 67 000 activités et 107 000 liens en
  quelques secondes, pour vérifier la qualité du planning directeur lui-même
  (méthodologie DCMA-14) et en extraire les règles répétées (voir
  `03_architecture.md` et `12_annexes.md`).
- **Génération de plannings dérivés** directement depuis le meilleur scénario
  calculé par le solveur : planning de post-tension (format Dywidag), planning
  d'occupation du site (format *Target schedule* du chantier).

## État d'avancement

**Fonctionnel et utilisé de façon itérative.** Le cœur du solveur (calcul de
cadence + simulation jour par jour) et l'interface de restitution sont
opérationnels et couvrent l'intégralité des règles métier explicitées à ce jour.
Sur le classeur de référence du chantier, dans sa configuration par défaut, le
solveur produit **zéro élément en retard, zéro élément bloqué** (résultat
vérifié de bout en bout par un test automatisé de navigateur — voir
`06_documentation_technique.md`).

Le projet **n'a pas de version figée ni de jalon de livraison formel** : il évolue
au rythme des échanges avec le planificateur du chantier, chaque nouvelle règle
métier ou correction étant intégrée, mesurée puis documentée. Voir
`08_roadmap.md` pour l'état détaillé « terminé / à faire » et
`09_questions_ouvertes.md` pour les points métier encore en attente d'arbitrage
(notamment une question sur les calendriers de travail des activités marines,
explicitement mise en attente le temps que le planificateur du chantier tranche
avec son propre responsable de planning).

Aucun processus d'intégration continue, aucune suite de tests automatisés
committée dans le dépôt, aucun environnement de déploiement formel : voir
`05_analyse_risques.md` pour l'évaluation de ce que cela implique.
