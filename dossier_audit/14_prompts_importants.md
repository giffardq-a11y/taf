# 14. Prompts importants

Ce document reproduit les instructions qui ont eu un effet direct et significatif
sur la conception ou le comportement du modèle. Deux catégories, clairement
distinguées :

- **Verbatim** — texte reproduit tel quel depuis l'enregistrement disponible de
  la conversation qui a produit ce code (orthographe et absence d'accents
  d'origine conservées).
- **Paraphrasé, attribué** — reconstruction fidèle d'une instruction ou d'une
  confirmation de l'utilisateur, faite à partir des formulations déjà présentes
  dans `README.md` et `SUITE.md` (« confirmé par l'utilisateur »,
  « précisé par l'utilisateur »…), pour la période antérieure à
  l'enregistrement verbatim disponible.

**Avertissement de portée.** L'assistant qui a rédigé ce dossier n'a accès qu'à
la portion la plus récente de l'historique de conversation (les échanges les
plus anciens ont été résumés puis ce résumé lui-même partiellement dépassé par
la suite des échanges). Ce document n'est donc pas une transcription intégrale
de toutes les instructions ayant influencé le projet depuis son origine — c'est
un relevé le plus complet possible compte tenu de ce qui reste effectivement
accessible.

## 14.1 Instructions verbatim (portion la plus récente du projet)

Sur le calendrier des travaux marins — **mise en attente explicite** :

> « Garde en tete la question concernant les calendrier des activites marine je
> discute avec le planificateur responsable de ce scoop »

Conséquence directe : aucune correction n'a été apportée sur ce point (voir
`09_questions_ouvertes.md`, §9.1) ; toute reprise de ce sujet doit vérifier au
préalable si cette discussion a eu lieu et quelle en a été la conclusion.

Sur la règle de sortie du bassin vers le parking — **règle métier dictée
directement**, source de l'ADR-016 :

> « un element dans le basin doit aller dans un parking des que possible des
> qu'un parking est libre. le seul cas ou cela n'est pas necessaire et lorsque
> la duree de stationnement dans un parking et inferieur a 4 semaine ET qu'elle
> ne bloque pas le float up du meme basin. le nombre de place de parking a une
> influence directe sur la fin de la production. »

Suivie de la précision :

> « le nombre de place parking pilote le demarrage du planning une fois la
> cadence d'immersion atteinte il sesse d'etre un probleme. »

Cette seconde phrase a été **vérifiée par mesure** (et non prise pour acquise
telle quelle) : le stock d'éléments en attente de parking culmine à 10 fin 2027
puis se résorbe quand la cadence d'immersion passe de 1/mois à 3/mois — cohérent
avec l'affirmation.

Sur la désactivation du jour de coulage aux cadences intermédiaires — **règle
métier dictée directement**, source de l'ADR-015 (correctif) :

> « par defaut lors des rythme intermediaire la regles des casting le meme jour
> chaque semaine par ligne doit etre desactive et rester active uniquement pour
> les rythme entier »

Sur le planning de post-tension — **demande de fonctionnalité**, source du
script `post_tension.py`, formulée en anglais dans l'échange d'origine :

> « base on the sequence encolsed plus comment can you make me a post
> tensioning schedule following the casting of the element the best scenario
> possible we have in the solver »

Puis, une fois une première version livrée, deux corrections directes :

> « pas de post tension pour spe »

> « le planning me va peux tu me l'afficher sous forme de gant classic avec
> debut fin »

> « et ajouter le numero des elements »

Ces trois messages ont directement produit la réécriture de `post_tension.py`
décrite en ADR-018 (partie « Gantt classique ») : suppression de toute
génération pour la ligne SPE (déjà conforme, confirmé), remplacement de la
grille postes-par-jour par un Gantt classique à dates début/fin, ajout des
numéros d'éléments en clair sur chaque barre.

Sur le diagnostic ayant conduit à l'ADR-019 (suppression des paramètres de
hook-up et de ballast) — **signalement de symptôme accompagné d'une hypothèse
de cause, formulée par l'utilisateur et confirmée par l'investigation** :

> « je n'arrive pas a obtenir une sequence sans retard peux tu regarder.
> enleve le parametre de duree de ballast et de hookup puisque nous avons les
> durees reel j'ai l'impression qu'elle s'ajoute. »

Point notable pour un futur repreneur du projet : l'hypothèse de l'utilisateur
(« elle s'ajoute », c'est-à-dire un double comptage) s'est révélée **exacte**
après investigation du code — un exemple direct de signalement métier précis et
correctement diagnostiqué a posteriori, qui a permis de localiser le défaut en
une seule itération plutôt que par exploration large.

Sur la commande à l'origine de ce dossier lui-même :

> « Préparation d'un dossier projet complet pour audit externe […] Ton objectif
> est donc de produire un dossier autoportant, complet, structuré et
> indépendant du modèle qui l'a généré. »

L'intégralité de la structure en 15 points demandée dans ce message est
reproduite dans `00_INDEX.md`, qui sert de table des matières à l'ensemble du
dossier.

## 14.2 Instructions et confirmations paraphrasées (période antérieure), attribuées à leur trace documentaire

Les éléments suivants sont reconstruits fidèlement à partir des mentions
explicites de `README.md` et `SUITE.md` (« confirmé par l'utilisateur »,
« précisé par l'utilisateur », etc.), la formulation verbatim d'origine n'étant
plus accessible à ce dossier.

- **Cadence de départ** — confirmation que la cadence initiale du modèle est
  bien de 3 semaines par segment, correspondant à `Config_Cycles` du classeur
  réel (source : `SUITE.md`, section « Résultat courant »).
- **Une cadence atteinte n'est jamais relâchée** — posé comme règle de base du
  modèle, avec dérogation explicitement acceptée comme exception rare et
  coûteuse plutôt que comme comportement par défaut (source : `README.md`,
  section « Ce que fait le solveur »).
- **Correction de la cascade d'étanchéité SPE** — précision apportée par
  l'utilisateur que le clamping P6 *est* l'étanchéité (fermeture définitive), la
  position exacte du SPE dans la chaîne UB n'entrant pas en compte pour la
  fermeture provisoire (source : `SUITE.md`, « Règle corrigée, en cascade
  (précisée par l'utilisateur) »).
- **Capacité de la zone de stockage SPE** — confirmation qu'une seule place
  existe réellement sur le chantier (source : `SUITE.md`, section « Le blocage
  de départ »).
- **Correspondance des zones FI1/FI2/FI3 ↔ UB1/UB2/UB3** — confirmation
  explicite de la correspondance directe, et que la zone tampon est bien dans
  le Basin C (source : `SUITE.md`, section « Sortie de chaîne SPE »).
- **Position de la coulée à l'intérieur des halles** — signalement que la
  coulée démarre 4 segments à l'intérieur des halles, pas à leur bord (source :
  contexte de capture d'écran décrit dans l'historique de session, repris dans
  `README.md`, table de géométrie du plan).
- **Chevauchements visuels de bassins** — deux captures d'écran signalant des
  éléments qui se superposent dans la zone des bassins, avec le commentaire
  « cela ne devrait pas se passer » / « cela non plus », à l'origine directe des
  ADR-016 et ADR-016bis.
- **Doute sur le fonctionnement du recalcul** — remarque « il me semble que la
  recalculation du solveur ne fonctionne pas », qui a conduit à l'investigation
  et à la correction du bug de capture de variable (`t` masquant la fonction de
  conversion de date) dans `report_template.html`, décrite dans l'historique de
  session.

## 14.3 Ce que ce relevé n'inclut pas

- Les tout premiers échanges ayant défini le périmètre initial du projet (avant
  la réduction du classeur, avant la première version du solveur) ne sont plus
  accessibles verbatim à la session qui rédige ce dossier ; leur contenu
  fonctionnel est néanmoins entièrement capturé dans le code et dans
  `README.md`, qui reste la source la plus fiable pour la justification de
  chaque règle du modèle.
- Les échanges purement conversationnels (accusés de réception, questions de
  clarification sans effet sur le code) ne sont pas reproduits ici : seules les
  instructions ayant eu un effet direct et traçable sur le comportement du
  modèle ou sur un livrable sont retenues.
