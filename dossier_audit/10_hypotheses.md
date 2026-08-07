# 10. Hypothèses

Hypothèses de conception utilisées dans le modèle, distinguées de deux façons :
**vérifiées** (confirmées par une mesure ou une confirmation explicite du
chantier) et **non vérifiées** (posées faute d'alternative, à ne pas considérer
comme acquises).

## 10.1 Hypothèses vérifiées

| Hypothèse | Vérification |
|---|---|
| La cadence de départ du modèle est de 3 semaines par segment | Confirmé par l'utilisateur, correspond à la valeur de `Config_Cycles` du classeur réel |
| Une seule place de stockage tampon suffit pour la ligne SPE | Mesuré : une deuxième place n'apporte aucun gain sur les indicateurs de retard |
| La correspondance de zones `FI1→UB1`, `FI2→UB2`, `FI3→UB3` est correcte | Confirmé par l'utilisateur ; la zone tampon SPE est bien positionnée dans le Basin C |
| Un élément doit quitter le bassin dès qu'une place de parking est libre, sauf séjour court non bloquant | Confirmé par observation directe du chantier, et vérifié par mesure de sensibilité au nombre de places de parking (3 à 12 places) |
| Le nombre de places de parking influence directement la fin de production, sauf une fois la cadence d'immersion stabilisée | Confirmé par l'utilisateur et vérifié par mesure : le stock d'éléments en attente culmine à 10 éléments fin 2027 puis se résorbe quand la cadence d'immersion passe de 1/mois à 3/mois — cohérent avec l'affirmation |
| L'ordre d'immersion du planning P6 ne contient aucune date manquante ni aucun ex æquo, sur le classeur de référence | Vérifié par lecture exhaustive de l'onglet `Immersion` (89 dates, toutes distinctes) |
| Le jour de coulage par ligne doit se désactiver aux cadences intermédiaires (demi-semaine) | Instruction explicite de l'utilisateur, implémentée et vérifiée de bout en bout sans régression sur le classeur de référence |
| La coulée démarre 4 segments à l'intérieur des halles, pas au bord | Confirmé par l'utilisateur (observation du site), et vérifié : élimine la totalité des chevauchements visuels précédemment observés |
| Le hook-up ne doit pas ajouter de délai au-delà de la date réelle de ballast (calculée à rebours depuis l'immersion) | Diagnostic confirmé par l'utilisateur et mesuré : la correction réduit le nombre d'éléments bloqués sans dégrader aucun autre indicateur |

## 10.2 Hypothèses non vérifiées, ou vérifiées partiellement

| Hypothèse | Statut | Voir |
|---|---|---|
| Les calendriers marins à 8 h et 10 h par jour correspondent à une distinction légitime (météo vs continu), pas à une erreur de saisie | Ni confirmée ni infirmée — question explicitement en attente | `09_questions_ouvertes.md`, §9.1 |
| Les durées par défaut de post-tension (6/4/2 postes) sont représentatives de la réalité Dywidag | Non vérifiée — valeurs placeholder explicitement signalées | `09_questions_ouvertes.md`, §9.2 |
| Le post-tensioning démarre deux jours après le **démarrage** (pas la fin) de la coulée de l'élément suivant | Interprétation raisonnable, non confirmée par le sous-traitant | `09_questions_ouvertes.md`, §9.3 |
| Le parallélisme des équipes de post-tension est illimité | Hypothèse de simplification, potentiellement irréaliste | `09_questions_ouvertes.md`, §9.4 |
| Les coordonnées de la zone de stockage SPE et du Ballast Jetty sur le plan | Extrapolées, pas mesurées sur un plan officiel | `09_questions_ouvertes.md`, §9.5 |
| L'ordre de pose peut servir de position provisoire dans la coupe du tunnel, en attendant les abscisses réelles | Approximation assumée, l'ordre est correct mais pas les distances | `09_questions_ouvertes.md`, §9.6 |
| Le comportement mesuré dans un cas limite synthétique (déphasage + cadences mixtes) ne se produit pas en usage réel | Vérifié seulement sur le chemin d'interface réel, pas sur l'espace complet des configurations possibles | `09_questions_ouvertes.md`, §9.7 |

## 10.3 Hypothèses structurelles (posées dès la conception, non remises en cause à ce jour)

- **Le planning directeur (Primavera P6) est la source de vérité absolue** pour
  toute date d'immersion, tout ordre d'immersion, toute date de passage de zone
  SPE et toute durée réelle de ballast. Le solveur ne questionne jamais ces
  données : il les applique. Si le planning P6 contient une erreur, elle se
  propage telle quelle dans le résultat (voir `05_analyse_risques.md`, risque
  métier « qualité du planning directeur »).
- **Le nombre et la topologie des ressources partagées du chantier
  (6 lignes de production, 3 bassins de 2 places, 5 places de parking + 1
  réserve, 1 seule paire de portes de mise à flot active à la fois, 1 seul
  élément ballasté à la fois) sont ceux du chantier Fehmarnbelt à Rødbyhavn**,
  tels que décrits par le planificateur du chantier. Le modèle n'a jamais été
  généralisé ni testé sur une autre configuration de site.
- **Un seul classeur de référence sert de base à toutes les mesures citées dans
  ce dossier et dans `README.md`/`SUITE.md`.** Aucune validation croisée sur un
  second jeu de données n'a été documentée.
- **L'utilisateur qui édite les paramètres du modèle (`REGLES`) à l'écran sait
  ce qu'il fait** : aucune borne de cohérence n'empêche, par exemple, de fixer
  une pente d'inertie nulle ou un nombre de places négatif. L'outil fait
  confiance à l'opérateur pour des valeurs raisonnables.
- **Le format et la structure du classeur d'entrée (onglets `Inputs`,
  `Immersion`, `Config_Cycles`, `Config_SPE`) resteront stables** dans le temps.
  Un changement de structure du classeur source (renommage de colonne,
  réorganisation d'onglet) casserait la lecture sans nécessairement produire
  un message d'erreur explicite pour toutes les colonnes concernées.
- **Le classeur d'entrée est une donnée de confiance**, produite par
  l'utilisateur lui-même ou son organisation — pas une entrée potentiellement
  hostile à valider au sens sécurité (voir `06_documentation_technique.md`,
  §6.5).
