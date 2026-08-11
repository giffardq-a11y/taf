# 4. Journal des décisions d'architecture (ADR)

Chaque décision est numérotée, datée par son commit d'origine quand identifiable,
et documentée selon le même schéma : contexte, décision, justification, avantages,
inconvénients, impacts, risques. Les décisions sont classées par ordre chronologique
approximatif (ordre du dépôt Git, du plus ancien au plus récent). Le nom du commit
Git correspondant est donné entre parenthèses quand il existe, pour permettre de
retrouver le diff exact.

---

## ADR-001 — Outil web autonome, sans serveur, un seul fichier pour l'usage interactif

**Commit d'origine :** `db53837` *« Add Lolland production planning visualizer »*

**Contexte.** Le besoin initial est un outil de calcul de cadence pour un
planificateur unique, à utiliser ponctuellement, sans infrastructure dédiée.

**Décision.** Construire un outil HTML/JS autonome (`index.html`), ouvrable par
double-clic, sans serveur, sans installation, sans compte utilisateur.

**Justification.** Le contexte (chantier, un seul utilisateur, données
potentiellement sensibles) rend une architecture serveur disproportionnée et
risquée du point de vue de la confidentialité.

**Avantages.** Zéro coût d'infrastructure ; zéro donnée transmise à un tiers ;
distribution triviale (envoi du fichier) ; fonctionne hors ligne une fois ouvert.

**Inconvénients.** Pas de multi-utilisateur simultané, pas d'historique partagé,
pas de sauvegarde automatique côté outil (voir ADR-002 et `05_analyse_risques.md`).

**Impacts.** Structure tout le reste du projet : la page de restitution
(`report_template.html`/`build_report.py`) hérite de la même contrainte
d'autonomie (voir ADR-003).

**Risques.** Le fichier de plusieurs centaines de kilo-octets doit être diffusé
manuellement à chaque mise à jour ; aucune mise à jour automatique n'existe.

---

## ADR-002 — Aucune donnée envoyée à un serveur, aucune télémétrie

**Contexte.** Le classeur d'entrée contient des dates de production et
d'immersion d'un chantier d'infrastructure critique.

**Décision.** Ni `index.html` ni `rapport.html` n'effectuent d'appel réseau au
moment de l'usage (hormis, pour `rapport.html`, le téléchargement ponctuel de
SheetJS *au moment de la génération de la page*, pas à son exécution).

**Justification.** Exigence de confidentialité explicite, cohérente avec
ADR-001.

**Avantages.** Aucune surface d'attaque réseau côté outil ; conformité immédiate
à toute politique de sécurité qui interdirait l'envoi de données de planning à
l'extérieur.

**Inconvénients.** Aucune analyse d'usage possible, aucun retour d'erreur
centralisé (voir `05_analyse_risques.md`, absence de supervision).

**Impacts.** A dicté le choix d'inliner SheetJS dans `rapport.html` plutôt que de
le charger depuis un CDN à l'exécution.

**Risques.** Aucun mécanisme de mise à jour à distance ; toute correction de bug
exige une redistribution manuelle du fichier.

---

## ADR-003 — Extraction du solveur entre deux marqueurs, plutôt qu'un module partagé

**Contexte.** Le solveur doit s'exécuter dans trois contextes (page interactive,
page publiée, CLI Node.js) sans jamais diverger.

**Décision.** Isoler le code du solveur entre
`/* ==== SOLVEUR-CORE-DEBUT ==== */` et `/* ==== SOLVEUR-CORE-FIN ==== */` dans
`index.html`, et l'**extraire textuellement** (expression régulière) dans
`build_report.py` et `planning_runner.js`, plutôt que d'en faire un module
JavaScript importé par les trois consommateurs.

**Justification.** Éviter d'introduire une étape de build (bundler, résolution de
modules) pour l'usage interactif de base, qui doit rester « ouvrir le fichier ».

**Avantages.** Garantie stricte de source unique sans aucune dépendance de
tooling ; le diff d'un commit modifiant le solveur montre immédiatement s'il
touche au périmètre partagé (dans les marqueurs) ou seulement à l'habillage
propre à `index.html` (en dehors).

**Inconvénients.** Solution non idiomatique du point de vue de l'ingénierie
logicielle habituelle (pas de packaging, pas de tests unitaires isolés sur le
module extrait sans repasser par une extraction) ; un renommage de variable dans
le bloc extrait peut casser silencieusement l'extraction si les marqueurs de
commentaire sont eux-mêmes modifiés par erreur.

**Impacts.** Conditionne toute la chaîne d'outillage (`build_report.py`,
`planning_runner.js`) qui commence systématiquement par relire `index.html` et en
extraire ce bloc.

**Risques.** Si les marqueurs disparaissent ou sont dupliqués, l'extraction
échoue silencieusement ou extrait la mauvaise portion — un test de non-régression
qui vérifie la présence des marqueurs n'existe pas dans le dépôt (voir
`05_analyse_risques.md`).

---

## ADR-004 — Simulation gloutonne jour par jour, pas de résolution globale sous contraintes

**Contexte.** Le calcul de cadence doit arbitrer entre de nombreuses ressources
partagées (bassins, parking, portes, jalon d'étanchéité) et 89 éléments.

**Décision.** Simuler jour par jour, ligne par ligne, en décidant localement à
chaque étape (glouton), plutôt que de formuler et résoudre un problème
d'optimisation global (par exemple un programme linéaire en nombres entiers).

**Justification.** Le besoin exprimé est un plan exploitable, vérifiable et
*explicable* — chaque décision doit pouvoir se justifier dans le journal de
calcul — plus qu'un optimum mathématiquement prouvé. Une approche gloutonne s'y
prête directement.

**Avantages.** Résultat rapide à calculer (permet l'exploration de plusieurs
dizaines de séquences candidates en quelques secondes, voir ADR-011) ; chaque
décision est traçable dans le journal ; le code reste lisible par un non
spécialiste de la recherche opérationnelle.

**Inconvénients.** Le résultat n'est **pas garanti optimal** au sens strict :
c'est une limite explicitement documentée (`README.md`, section « Limites
connues » ; reprise dans `13_audit_critique.md`).

**Impacts.** A permis de construire un optimiseur de séquence par évaluation
complète de chaque candidate plutôt que par une méthode de résolution dédiée
(voir ADR-011).

**Risques.** Sur un jeu de données très différent du classeur de référence
(topologie de ressources changée, beaucoup plus d'éléments), le temps de calcul
ou la qualité du résultat glouton pourraient se dégrader sans qu'un signal
explicite en avertisse — aucun test de performance sur un jeu de données à
grande échelle n'existe dans le dépôt.

---

## ADR-005 — L'ordre d'immersion est une donnée d'entrée, jamais modifiée

**Commit d'origine :** `4089b51` *« Take immersion dates from the P6 extract, and flag order inversions »*

**Contexte.** Le planning directeur (Primavera P6) impose un ordre d'immersion
strict ; la séquence de production du classeur peut, elle, contenir des
« inversions » par rapport à cet ordre.

**Décision.** Le programme ne modifie **jamais** l'ordre d'immersion. Il détecte
les inversions entre production et immersion, les signale, et l'optimiseur de
séquence les corrige *côté production*, jamais côté immersion.

**Justification.** L'ordre d'immersion est une contrainte physique et
contractuelle du chantier (mise en place des éléments dans le tunnel), pas un
paramètre de production.

**Avantages.** Élimine toute une classe d'erreurs (un optimiseur qui « trouverait »
un meilleur plan en réordonnant l'immersion, irréaliste sur le terrain).

**Inconvénients.** Réduit l'espace de recherche de l'optimiseur : dès que toutes
les dates d'immersion sont distinctes et renseignées (c'est le cas sur le
classeur de référence), une file sans inversion est triée de façon unique — voir
ADR-011 pour la conséquence directement tirée de cette contrainte.

**Impacts.** Structure le critère premier de l'optimiseur de séquence (zéro
inversion avant tout autre critère).

**Risques.** Si le planning P6 lui-même contenait une erreur d'ordre
d'immersion, le programme la reproduirait fidèlement sans la questionner — c'est
un choix assumé (voir `10_hypotheses.md`).

---

## ADR-006 — Une cadence atteinte n'est jamais relâchée (par défaut)

**Commit d'origine :** `a42fcd9` *« Stop releasing the rate, and let the optimiser set line loads »*

**Contexte.** Le modèle initial autorisait une ligne à ralentir puis
réaccélérer.

**Décision.** Par défaut, une ligne ne peut qu'accélérer, jamais ralentir, une
fois une cadence atteinte. Une case d'interface permet de déroger à cette règle
(un relâchement unique par ligne, en fin de programme), désactivée par défaut.

**Justification.** Mesuré : le test de faisabilité du solveur de cadence ignore
l'aval (bassins, parking, ordre d'immersion imposé) et juge parfois tenable un
rythme plus lent qui, une fois la simulation aval appliquée, ne l'est pas.
Autoriser le relâchement a coûté, sur le classeur de référence, 8 retards
supplémentaires, 1032 jours de retard cumulé et 4 changements de cadence en plus.

**Avantages.** Réduit fortement le nombre de changements de cadence à
communiquer aux équipes (environ divisé par 4, selon la mesure de `README.md`) ;
supprime des retards mesurés.

**Inconvénients.** Moins flexible en théorie (une ligne « en avance » ne peut
plus ralentir pour économiser des ressources) ; ce compromis a un coût mesuré
inverse quand la dérogation est activée volontairement.

**Impacts.** Simplifie le raisonnement du solveur (une seule direction de
changement possible par défaut) et le rend plus prévisible pour les équipes de
production.

**Risques.** Si un scénario métier légitime nécessitait vraiment un
ralentissement (économie de ressources avérée), il faudrait activer
explicitement la dérogation et en accepter le coût mesuré — la case existe
précisément pour ce cas, mais son usage n'est pas guidé par le programme au-delà
d'un chiffrage.

---

## ADR-007 — Deux stratégies d'arrêt d'usine (« au plus tôt » vs « flux tendu »)

**Commit d'origine :** `1d39b7a` *« Stop the factory early and progressively, and show the tunnel section in the report »*

**Décision.** Rendre sélectionnable, par une case d'interface, la stratégie
d'extinction des lignes : cadence la plus rapide tenable et arrêt dès la file
vidée (« au plus tôt », coché par défaut), ou cadence la plus lente qui tienne
les dates, usine active jusqu'au dernier élément (« flux tendu »).

**Justification.** Les deux stratégies répondent à des besoins différents (libérer
les halles au plus tôt pour d'autres usages du site, vs lisser la charge de
production) et aucune des deux n'est universellement préférable.

**Avantages.** Sur le classeur de référence, l'arrêt au plus tôt libère la
dernière halle trois mois plus tôt (11/07/2029 contre 14/10/2029) avec zéro
retard dans les deux cas.

**Inconvénients.** Le mode « au plus tôt » coûte du stockage à flot (208 jours
d'avance moyenne entre outfitting et immersion, contre 187 à flux tendu) et un
changement de cadence de plus.

**Impacts.** Le critère « fin de production » entre dans l'ordre lexicographique
de l'optimiseur de séquence quand ce mode est actif.

**Risques.** Aucun — c'est un choix explicite laissé à l'utilisateur, sans effet
caché.

---

## ADR-008 — Ligne SPE pilotée par les dates de passage de zone du planning P6

**Commits d'origine :** `574995a` *« Drive the SPE line from the P6 schedule instead of fixed zone durations »*, affiné dans plusieurs commits ultérieurs

**Contexte.** Le modèle initial estimait la progression de la ligne SPE par des
durées fixes par zone (`Config_SPE`), indépendantes du planning réel.

**Décision.** Faire suivre à la ligne SPE les dates réelles de passage de zone
lues dans le planning directeur (activités de *skidding* sous les niveaux CPA,
CP1, CP2, CP3, FI1, FI2, FI3) ; les durées fixes de `Config_SPE` ne servent plus
que de repli quand le planning ne renseigne rien pour un SPE donné.

**Justification.** Mesuré : cette correction, combinée à la correction de la
mesure des retards SPE (ADR-009 ci-dessous) et à la suppression d'une durée
inventée en fin de chaîne SPE, a fait passer le résultat de 18 retards (133 j
max, 774 j cumulés) à **zéro retard, zéro blocage** sur le classeur de
référence.

**Avantages.** Élimine une source majeure d'écart entre le modèle et la réalité
du planning directeur ; la ligne SPE devient aussi fiable que les lignes
standards.

**Inconvénients.** Rend le solveur dépendant de la qualité du planning P6 collé
dans l'onglet `Immersion` du classeur d'entrée : un planning SPE incomplet ou mal
formé dégrade directement le résultat, sans que cela soit toujours visible avant
mesure.

**Impacts.** A motivé la construction, plus tard dans le projet, de la boîte à
outils d'audit du planning P6 (`lire_xer.py`/`auditer_xer.py`/`regles_p6.py`) —
la qualité de cette donnée d'entrée mérite un contrôle propre.

**Risques.** Si une future version du planning P6 change la nomenclature des
zones ou des niveaux, le repérage par nom de zone dans le code
(`index.html`) devra être mis à jour.

---

## ADR-009 — Zone de stockage tampon dédiée pour la ligne SPE

**Commit d'origine :** `b6d321d` *« Give the SPE line its storage area, and let the optimiser pick the line »*

**Contexte.** Deux éléments SPE peuvent se retrouver en conflit d'ordre
d'immersion pour l'unique place SPE du Basin C : l'élément produit en premier
occupe la place, alors qu'un autre élément, produit après mais devant s'immerger
avant, ne peut jamais entrer.

**Décision.** Ajouter une zone de stockage tampon dédiée à la ligne SPE (hors
parking standard), où un élément qui retient la place d'un autre SPE devant
s'immerger avant lui peut être déplacé temporairement, sans que cela modifie
aucune date.

**Justification.** Mesuré sur le classeur de référence : 38 éléments bloqués
tenaient à ce seul verrou (un élément SPE bloquait 37 autres éléments par
propagation dans l'ordre d'immersion imposé). Corriger les inversions de
séquence ne changeait rien à ce blocage ; la zone de stockage le lève
entièrement, avec une seule place suffisante (vérifié : une deuxième place
n'apporte aucun gain supplémentaire).

**Avantages.** Débloque l'intégralité de la file sans toucher à l'ordre
d'immersion (contrainte ADR-005) ni inventer de date.

**Inconvénients.** Les coordonnées de cette zone sur le plan du site sont
**extrapolées**, pas mesurées sur un plan officiel (limite documentée dans
`README.md`, reprise dans `09_questions_ouvertes.md`).

**Impacts.** A révélé un cas d'école : un blocage massif dont la cause profonde
n'était pas la séquence de production (l'explication la plus intuitive) mais une
contrainte de capacité locale — a renforcé la pratique de mesure systématique du
projet (voir `13_audit_critique.md`).

**Risques.** Si la capacité réelle du chantier pour cette zone changeait, la
règle (`REGLES.placesStockageSPE`, réglable) devrait être mise à jour ; c'est
déjà un paramètre, pas une constante.

---

## ADR-010 — Étanchéité SPE en cascade à trois niveaux, négociable

**Commits d'origine :** `5d14183`, `11d16d7`, `e9c3f7c`

**Décision.** Modéliser le jalon d'étanchéité d'un SPE en trois niveaux
successifs : (1) la date de clamping du planning P6 fait foi si elle tombe assez
tôt ; (2) à défaut, une fermeture provisoire est possible au plus tôt 12 semaines
après la sortie de la zone CP3 ; (3) un seuil critique de 8 semaines reste
accessible sur autorisation explicite (case à cocher), chaque recours étant
signalé.

**Justification.** Une contrainte binaire (étanche ou non) aurait empêché de
distinguer ce qui est réellement bloquant de ce qui est une marge de sécurité
négociable ; la cascade reflète la réalité opérationnelle décrite par le
planificateur du chantier (les travaux peuvent commencer en UB1 et s'achever en
UB2, la position exacte dans la chaîne n'est pas ce qui compte, c'est
l'avancement).

**Avantages.** Permet de chiffrer précisément le gain d'une négociation
(avancer le jalon d'étanchéité) plutôt que de le traiter comme une contrainte
dure non négociable. Sur le classeur de référence, seul le palier de 42 semaines
d'avance fait basculer le résultat de 19 à 5 retards — les paliers intermédiaires
ne rapportent rien, une information qu'une contrainte binaire n'aurait jamais
révélée.

**Inconvénients.** Complexifie le modèle (trois niveaux, un seuil critique
optionnel) par rapport à une règle unique.

**Impacts.** Le solveur cherche automatiquement par dichotomie le gain minimal
qui annule le coût de cette porte, et propose le résultat dans une boîte de
dialogue à l'utilisateur.

**Risques.** Repose sur la fiabilité des dates de clamping du planning P6 ; si
elles sont mal renseignées, le premier niveau de la cascade est faussé.

---

## ADR-011 — Optimiseur de séquence : ordre lexicographique de critères, puis réaffectation aux lignes

**Commit d'origine :** `433e38f` *« Stagger the halls, and let the solver choose the production order »*, étendu par `9b41379`, `b6d321d`

**Contexte.** Une fois l'ordre d'immersion posé comme intangible (ADR-005), il
fallait décider comment optimiser malgré tout la production.

**Décision.** Comparer les séquences candidates selon un ordre lexicographique
strict de critères : nombre d'éléments bloqués → nombre d'inversions PL → nombre
d'éléments en retard → retard cumulé → retard maximal → (si arrêt au plus tôt)
date de fin de production → nombre de changements de cadence. Chaque critère ne
départage que si tous les précédents sont à égalité. Une fois ce tri épuisé,
réaffecter les éléments entre les 5 lignes standards interchangeables devient le
seul levier réellement disponible.

**Justification.** Constat mesuré : une file sans inversion est une file triée
par date d'immersion — sur un classeur où toutes les dates sont distinctes et
renseignées, cet ordre est **unique**. L'optimisation interne à une ligne n'a
donc, dans ce cas, rien à déplacer ; le vrai levier est de décider *quel élément
va sur quelle ligne*, pas dans quel ordre il y passe.

**Avantages.** A permis un gain mesuré important par un seul déplacement ciblé
(un élément changé de ligne a fait passer le retard cumulé de 1365 à 896 jours
sur une variante) ; le critère « bloqués avant retards » évite un piège de
lecture (un plan où beaucoup d'éléments ne sortent jamais paraîtrait bon sur le
seul critère « retards », qui ne compte que les éléments sortis).

**Inconvénients.** L'ordre lexicographique est rigide : un très léger gain sur
le premier critère l'emporte toujours sur un gain énorme sur les critères
suivants, ce qui peut ne pas correspondre à un jugement humain plus nuancé.

**Impacts.** A rendu nécessaire le bouton « Comparer » et le tableau
comparatif de l'interface, pour que l'utilisateur voie explicitement quel
critère a décidé.

**Risques.** Sur un classeur où plusieurs éléments partageraient la même date
d'immersion (ex æquo), le comportement de tri interne à une ligne redeviendrait
actif ; ce code existe et est toléré mais n'est pas exercé par le classeur de
référence actuel — un jeu de données avec ex æquo n'a pas été testé récemment.

---

## ADR-012 — Déphasage (staggering) entre halles, dur ou souple selon la cadence

**Commit d'origine :** `433e38f`

**Décision.** Décaler le démarrage du hall B (PL-3/PL-4) de 3 segments par
rapport au hall A (PL-1/PL-2), et PL-5 de 7 segments, pour éviter que plusieurs
bassins ne se remplissent le même jour. Cette contrainte devient **dure**
seulement à partir d'une cadence d'1 semaine/segment (et seulement quand les deux
halles tournent à la même cadence) ; en deçà, c'est une simple préférence pour
PL-5 et une contrainte dure pour le hall B.

**Justification.** Mesuré : le staggering *réduit* les retards, il ne coûte
rien (1145 j de retard cumulé avec, contre 1509 sans, sur une configuration de
référence).

**Avantages.** Empêche un engorgement simultané des portes et des bassins.

**Inconvénients.** Introduit une dépendance de phase entre lignes qui doit être
suspendue explicitement quand les deux halles divergent de cadence — cas géré
(voir ADR-016bis ci-après pour un bug lié à cette interaction, découvert et
corrigé tardivement dans le projet), pour éviter de brider indéfiniment le hall
le plus rapide.

**Impacts.** A nécessité un mécanisme de suspension automatique
(`hallsMemeCadence()`) et un signal dans le journal quand la suspension se
produit.

**Risques.** Interaction non triviale avec d'autres règles activées/désactivées
dynamiquement par cadence (voir ADR-019) — zone du code identifiée comme
sensible, voir `05_analyse_risques.md`.

---

## ADR-013 — Impositions manuelles non destructives, limitées à deux dates pilotes

**Commit d'origine :** `dd425b7` *« Let the two driving bars impose their date and re-run the solver »*

**Décision.** N'autoriser l'imposition manuelle que sur deux types de dates : le
départ de coulée d'un élément (au plus tôt seulement — on peut retarder un
lancement, jamais libérer une halle plus tôt qu'elle ne l'est réellement) et la
date d'immersion cible d'un élément. Toutes les autres dates (outfitting, bassin,
parking, ballast) restent des **sorties** calculées, jamais des entrées
imposables. Chaque imposition est stockée à part (structure `IMPOSITIONS`),
réappliquée à chaque recalcul, jamais écrite dans le classeur source.

**Justification.** Ce sont les deux seules dates qui sont de vraies données
d'entrée du modèle métier ; imposer une date de bassin ou de parking n'aurait pas
de sens tant que le solveur ne sait pas raisonner sur des dates contraintes en
aval — l'imposer casserait la cohérence du reste de la simulation sans que le
solveur puisse le détecter.

**Avantages.** Système réversible, traçable (un élément imposé porte un
marqueur visuel distinct), qui ne pollue jamais la donnée source.

**Inconvénients.** Une imposition d'immersion touche potentiellement à l'ordre
d'immersion (ADR-005) — c'est explicitement documenté comme une décision de
l'utilisateur, jamais une initiative du solveur, et un avertissement est levé si
l'ordre change.

**Impacts.** A rendu nécessaire le rapport de « conséquences » (ADR-014).

**Risques.** Si l'utilisateur change de classeur ou de paramètres entre deux
calculs, une comparaison de conséquences peut devenir non pertinente ; le
système le détecte et avertit (signature de paramètres comparée), mais ne
l'empêche pas.

---

## ADR-014 — Rapport de conséquences d'une imposition, contre une référence capturée

**Commit d'origine :** `35c2357` *« Report what an imposed date costs, against the run without one »*

**Décision.** Avant d'appliquer la première imposition d'une session, capturer
un instantané des indicateurs de référence (sans aucune date imposée). Après
chaque recalcul avec impositions actives, afficher l'écart contre cet instantané,
avec avertissement si la séquence a été réoptimisée entre-temps (effet mêlé,
difficile à isoler) ou si les paramètres ont changé (référence obsolète).

**Justification.** Une date imposée sans mesure de son effet global serait un
geste à l'aveugle ; le rapport rend le coût ou le gain immédiatement visible.

**Avantages.** Transparence directe sur l'effet d'une décision manuelle.

**Inconvénients.** La référence capturée peut devenir trompeuse si l'utilisateur
change de scénario sans redémarrer une nouvelle session de comparaison —
atténué par l'avertissement, pas éliminé.

**Impacts.** Composant d'interface dédié (`#s-consequences` dans
`report_template.html`).

**Risques.** Aucun risque de calcul (le résultat du solveur lui-même n'est pas
affecté) ; risque d'interprétation si l'avertissement de référence obsolète est
ignoré par l'utilisateur.

---

## ADR-015 — Règle « un jour de coulage par ligne », désactivée à cadence intermédiaire

**Commits d'origine :** `f431fcd` *« Give each line its own casting day, and number the pours in the Gantt »*, puis `9e411da` *« Disable casting-day rule at intermediate rhythms »* (correctif tardif)

**Contexte.** Cinq lignes qui démarreraient toutes le même jour saturent la
centrale à béton en début de semaine puis la laissent inactive le reste du
temps.

**Décision.** Attribuer à chaque ligne un jour fixe de la semaine pour son
lancement de coulée (PL-1 lundi … PL-5 vendredi, réglable). **Correctif tardif :**
cette règle se désactive désormais d'elle-même quand la ligne tourne à une
cadence intermédiaire (demi-semaine : 3,5 / 2,5 / 1,5 semaines/segment), et ne
reste active qu'aux cadences entières (4 / 3 / 2 / 1).

**Justification.** Mesuré : le cycle d'un élément dure `rythme × 7 × 9` jours.
Ce nombre n'est un multiple de 7 (donc aligné sur un jour de semaine fixe) que si
le rythme est entier. À cadence demi-entière, le jour de semaine dérive à chaque
élément et la règle forçait un rattrapage — jusqu'à 17 jours de retard maximal et
41 jours cumulés mesurés avant correctif, concentrés sur les éléments les plus
rapides, donc les moins marginés, en fin de programme. L'utilisateur a
explicitement demandé la désactivation automatique plutôt qu'un simple
avertissement.

**Avantages.** Supprime un coût de retard qui n'avait aucune contrepartie
opérationnelle réelle aux cadences intermédiaires.

**Inconvénients.** Complexifie légèrement la règle (dépendance à l'état courant
de la cadence de la ligne, `lastRhythmState`) ; un test synthétique a révélé,
lors de la validation de ce correctif, une interaction étroite avec le
déphasage entre halles sur la ligne PL-5 dans un scénario de test isolé
non représentatif du flux réel de l'interface (voir `05_analyse_risques.md` et
`09_questions_ouvertes.md`) — non reproduite en usage réel (vérifié de bout en
bout, zéro retard avant et après correctif sur le classeur de référence), mais
signalée pour vigilance.

**Impacts.** A nécessité d'harmoniser trois points du code
(`jourDeCoulage`, `versJourCoulage`, la marge de tolérance dans
`attenteStagger`) sur le même critère de cadence entière.

**Risques.** Voir ci-dessus ; interaction non totalement blanchie sur tous les
chemins de code possibles, seulement sur le chemin réellement emprunté par
l'interface.

---

## ADR-016 — Inversion de la règle de sortie du bassin vers le parking

**Commit d'origine :** `aba5599` *« Empty the basin as soon as a parking slot is free »*

**Contexte.** La règle initiale ne faisait sortir un élément du bassin que si un
autre élément réclamait explicitement sa place. Le bassin ne se vidait donc qu'au
dernier moment, et le nombre de places de parking n'avait presque aucun effet
mesurable sur la date de fin de production — ce qui contredisait l'observation
directe du planificateur sur le chantier.

**Décision.** Inverser la règle : un élément quitte le bassin vers une place de
parking **dès qu'une place est libre**, sauf dispense (séjour prévu de moins de
4 semaines **et** qui ne bloque aucun float-up du même bassin).

**Justification.** Instruction directe et explicite de l'utilisateur, confirmée
par la mesure : avec l'ancienne règle, faire varier le nombre de places de
parking de 5 à 12 ne changeait presque rien au résultat ; avec la règle
corrigée, 3 places bloquent 62 éléments et 10 places n'en bloquent plus aucun —
cohérent avec ce que le chantier observe.

**Avantages.** Restaure la sensibilité du modèle au nombre de places de
parking, un paramètre physique réel et coûteux à changer sur le terrain — le
modèle devient donc utile pour dimensionner cette ressource.

**Inconvénients.** A nécessité de revoir la logique de détection de « qui
réclame une place » (la file se forme désormais en amont du bassin, au niveau du
statut d'attente de float-up, plutôt qu'à flot) — deux corrections en cascade
ont été nécessaires pour stabiliser le comportement (voir aussi ADR-016bis).

**Impacts.** A conduit l'assistant à corriger explicitement, auprès de
l'utilisateur, une affirmation antérieure erronée selon laquelle le nombre de
places de parking n'affectait pas significativement la date de fin de
production — cette affirmation reposait sur l'ancienne règle, incorrecte.

**Risques.** Aucun risque de calcul résiduel identifié ; règle vérifiée par
mesure de sensibilité complète (3 à 12 places).

---

## ADR-016bis — Le float-up ne peut plus se lancer vers un bassin occupé

**Commit d'origine :** `6171450` *« Refuse a float-up into an occupied basin »*

**Contexte.** Directement lié à ADR-016 : une fois la sortie du bassin
accélérée, un bug préexistant est devenu visible — un float-up pouvait être
lancé vers un poste de bassin déjà occupé, provoquant un chevauchement visuel de
deux éléments sur le plan (signalé par l'utilisateur via deux captures d'écran).

**Décision.** Un float-up ne peut désormais démarrer que si le bassin
d'arrivée a une place réellement libre pour chaque élément du groupe partant.

**Justification.** Correction d'un bug de simulation, confirmé visuellement par
l'utilisateur sur le plan animé.

**Avantages.** Élimine les chevauchements visuels et les incohérences physiques
correspondantes.

**Inconvénients.** A déplacé la formation de la file d'attente vers l'amont
(statut « attente de bassin » ou « attente de float-up »), ce qui a cassé la
détection de « qui réclame une place » ailleurs dans le code (voir ADR-016) —
nécessitant une seconde correction pour rester cohérent.

**Impacts.** Corrige directement un défaut visible et rapporté par
l'utilisateur ; illustre une dépendance en cascade entre deux règles qui semblent
indépendantes à première lecture.

**Risques.** Ce type d'interaction en cascade (une correction en amont expose un
bug latent en aval) est une caractéristique structurelle du modèle — voir
`05_analyse_risques.md` pour l'évaluation de ce risque en tant que classe.

---

## ADR-017 — Géométrie de coulée corrigée : les 4 premiers segments sont coulés à l'intérieur des halles

**Commit d'origine :** `da5651d` *« Cast inside the halls, and show the SPE before the Upper Basin »*

**Contexte.** Le modèle plaçait initialement le poste de coulée au bord des
halles ; l'utilisateur a signalé que la coulée démarre en réalité 4 segments à
l'intérieur.

**Décision.** Décaler la position de référence de la coulée (`GEO.x_entry`) de
108 pixels vers l'est sur le plan (4/9 de la longueur d'un élément), pour
refléter que les 4 premiers segments sont coulés à l'intérieur des halles.

**Justification.** Signalement direct de l'utilisateur, confronté à une
observation du site.

**Avantages.** Vérifié : élimine la totalité des 3239 chevauchements visuels
préexistants entre coulée béton et zone d'outfitting sur une même ligne, dans le
rendu animé.

**Inconvénients.** Aucun — correction géométrique pure, sans effet sur le
calcul de cadence lui-même.

**Impacts.** Uniquement sur le rendu visuel (`GEO`), aucun effet sur les dates
calculées.

**Risques.** Aucun.

---

## ADR-018 — Synchronisation des paramètres par défaut de `planning_runner.js` avec l'interface

**Commit d'origine :** correction dans le commit `c79a43c` *« Draw the post-tensioning schedule from the solver's casting dates »*

**Contexte.** `planning_runner.js` avait des valeurs de paramètres par défaut
obsolètes (paramètres manquants ou logique d'option inversée), si bien que le
« meilleur scénario » exporté en ligne de commande ne correspondait pas à ce que
l'interface affichait à l'écran par défaut.

**Décision.** Aligner strictement les valeurs par défaut de `planning_runner.js`
sur celles de `report_template.html`.

**Justification.** Un générateur de planning dérivé (post-tension, occupation du
site) doit refléter le même scénario que celui validé visuellement par
l'utilisateur, sinon les deux outils divergent silencieusement.

**Avantages.** Garantit la cohérence entre ce que l'utilisateur voit à l'écran
et ce que les exports en ligne de commande produisent.

**Inconvénients.** Ce type de duplication de valeurs par défaut (une fois dans
`report_template.html`, une fois dans `planning_runner.js`) reste un point de
divergence potentiel à chaque nouveau paramètre ajouté — pas de mécanisme
automatique qui empêcherait une nouvelle dérive. Voir `05_analyse_risques.md`.

**Impacts.** A nécessité de revalider et régénérer le planning de post-tension
déjà livré, une fois la correction faite.

**Risques.** Risque récurrent tant qu'aucun test de non-régression ne compare
automatiquement les deux jeux de valeurs par défaut.

---

## ADR-019 — Suppression des paramètres de durée de hook-up et de ballast, correction d'un double comptage

**Commit d'origine :** `688bc48` *« Fix hook-up double-counting an element's basin dwell against its real ballast date »*

**Contexte.** L'utilisateur a signalé ne plus réussir à obtenir de séquence sans
retard et a suspecté un double comptage entre les durées réelles issues du
planning P6 et des paramètres forfaitaires d'interface (« Durée Hook-up »,
« Durée Ballast »).

**Décision.** Supprimer les deux paramètres d'interface. Le hook-up devient un
repère d'affichage fixe (1 jour), sans effet sur le calcul. La durée de ballast
vient exclusivement de l'activité P6 « Floatout, 1st Phase Ballast Concrete »
propre à chaque élément, avec un repli interne fixe et non réglable
(`REGLES.ballastJoursDefaut`, 7 jours) pour les rares éléments sans cette
donnée.

**Justification.** Diagnostic confirmé : la sortie du bassin était bloquée par
une attente forfaitaire calculée **en avant** depuis l'entrée en bassin (durée de
hook-up), en plus de la date réelle de départ au ballast, elle-même calculée **à
rebours** depuis la date d'immersion cible. Un élément déjà tendu sur sa date de
ballast réelle pouvait ainsi être retardé une seconde fois, sans aucune
justification physique — le hook-up n'est, dans la réalité décrite, que les 24
dernières heures avant le Ballast Jetty, déjà comprises dans la fenêtre réelle,
pas un délai supplémentaire.

**Avantages.** Mesuré : sur le classeur de référence, avec le déphasage entre
halles désactivé pour isoler l'effet, le nombre d'éléments bloqués passe de 85 à
62, sans dégradation ailleurs. Simplifie l'interface (deux paramètres en moins,
tous deux ambigus).

**Inconvénients.** Le float-up (mise à flot) n'a, lui, toujours aucune source de
durée réelle par élément dans le planning P6 exploité par le code à ce jour ; son
paramètre d'interface a donc été conservé tel quel — un traitement asymétrique
entre les trois durées aval (float-up, hook-up, ballast), documenté ici pour
qu'il ne soit pas pris pour un oubli.

**Impacts.** A nécessité de revoir 3 points de code interdépendants (la garde de
sortie de bassin pour les lignes standards, la même garde pour la ligne SPE, et
l'estimation prospective de durée de pipeline utilisée pour le choix de
cadence) pour éliminer complètement la double contrainte, pas seulement son
symptôme le plus visible.

**Risques.** Aucun test de non-régression automatisé ne verrouille
spécifiquement ce comportement (l'absence de double comptage) pour l'avenir —
une future modification pourrait réintroduire un mécanisme équivalent sans
qu'un test échoue pour le signaler. Voir `05_analyse_risques.md`.

---

## ADR-020 — Boîte à outils d'audit du planning P6 tenue séparée du solveur

**Commits d'origine :** ensemble de commits non fusionnés au solveur, fichiers
`lire_xer.py`, `auditer_xer.py`, `regles_p6.py`

**Contexte.** Le besoin d'auditer la qualité du planning directeur lui-même (à
partir d'un export XER de 67 000 activités) est apparu en cours de projet,
distinct du besoin de calcul de cadence.

**Décision.** Construire cette boîte à outils comme un ensemble de scripts
Python **totalement indépendants** du solveur JavaScript, ne partageant aucun
code, aucune structure de données, et ne réinjectant aucun résultat
automatiquement dans les règles du solveur (`REGLES`).

**Justification.** Les deux besoins ont des cycles de vie différents (l'audit
est ponctuel, à chaque nouvelle publication du planning P6 ; le solveur tourne à
chaque cycle de planification) et des publics parfois différents (l'audit
intéresse aussi le planificateur du bureau d'études P6, pas seulement le
planificateur de production).

**Avantages.** Aucun risque de régression croisée entre les deux outils ;
l'audit peut évoluer (nouveaux contrôles DCMA, nouveaux motifs de règles) sans
jamais risquer de casser le calcul de cadence.

**Inconvénients.** Un constat de l'audit (par exemple, une anomalie de
calendrier détectée) ne se traduit **pas automatiquement** en correction du
modèle du solveur : le lien reste manuel, fait par un humain qui lit le rapport
d'audit puis, s'il le juge pertinent, modifie `REGLES` ou signale un problème au
planificateur P6.

**Impacts.** Deux bases de code, deux langages, aucune donnée partagée au moment
de l'exécution (le pont, `extraire_p6.py` → `donnees_p6.txt` → `planning_cible.py`,
ne transporte que des données d'habillage — travaux marins, finitions —, jamais
de règle de calcul).

**Risques.** Une divergence de vocabulaire ou de règle métier pourrait
apparaître entre les deux outils sans qu'aucun mécanisme automatique ne la
détecte, puisqu'ils ne se recoupent jamais au moment de l'exécution. Voir
`05_analyse_risques.md`.
