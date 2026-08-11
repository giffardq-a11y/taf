"""Inventaire et audit de qualité d'un planning P6, à partir de son export XER.

    python3 auditer_xer.py planning.xer [-o rapport.txt]

Ce que le script mesure — et pourquoi. Les seuils entre parenthèses sont ceux de l'évaluation
DCMA en 14 points, la grille la plus répandue pour juger un planning ; ils servent de repère,
pas de verdict. Un planning de chantier a de bonnes raisons de s'en écarter, mais il doit
pouvoir dire lesquelles.

  1. Extrémités ouvertes  — activités sans prédécesseur ou sans successeur (cible : 0 hors
     jalons de début et de fin). Une extrémité ouverte flotte librement : elle ne pousse rien
     et rien ne la pousse, donc sa date ne veut rien dire.
  2. Décalages positifs   — un lag est une durée sans propriétaire, sans ressource et sans
     avancement (≤ 5 % des liens).
  3. Types de liens       — la part de fin-début (≥ 90 %). Les SS/FF sont légitimes mais se
     vérifient un par un.
  4. Décalages négatifs   — un lead fait démarrer un successeur avant la fin de son
     prédécesseur : le chemin critique en devient faux (cible : 0).
  5. Contraintes dures    — MSO/MFO/obligatoires figent une date et court-circuitent la
     logique (≤ 5 % des activités).
  6. Marge élevée         — plus de 44 jours de marge totale : souvent le signe d'une logique
     manquante plutôt que d'une vraie latitude (≤ 5 %).
  7. Marge négative       — cible : 0. Sinon le planning se sait déjà en retard.
  8. Durées longues       — plus de 44 jours : une tâche trop grosse cache sa logique interne
     et bloque ses successeurs plus longtemps que nécessaire (≤ 5 %).
  9. Dates invalides      — réalisé au-delà de la date d'état, prévisionnel en deçà.
 10. Ressources           — activités sans ressource ni coût : leur durée n'est adossée à rien.

Et, hors DCMA, ce qui compte autant sur un planning répétitif :
  - la densité de liens et les liens redondants (un chemin plus long existe déjà) ;
  - les boucles de logique ;
  - les liens qui traversent deux calendriers différents : parfois des jours fantômes,
    parfois la frontière légitime entre un quai ouvert en continu et un moyen en mer
    limité par l'état de mer — le chiffre se lit, il ne se corrige pas de lui-même ;
  - la profondeur et le remplissage du WBS ;
  - la composition du chemin déterminant calculé par P6 lui-même.

Rien n'est corrigé ici : le script lit, compte et signale.
"""
import argparse
import collections
import datetime
import sys

from lire_xer import lire, entier, reel, date

# Les tables et colonnes strictement nécessaires : le reste du fichier n'est pas gardé.
BESOINS = {
    'PROJECT': ['proj_id', 'proj_short_name', 'last_recalc_date', 'plan_start_date',
                'scd_end_date', 'critical_path_type', 'clndr_id'],
    'SCHEDOPTIONS': None,
    'CALENDAR': ['clndr_id', 'clndr_name', 'clndr_type', 'day_hr_cnt', 'week_hr_cnt',
                 'year_hr_cnt', 'default_flag'],
    'PROJWBS': ['wbs_id', 'parent_wbs_id', 'wbs_name', 'proj_node_flag'],
    'TASK': ['task_id', 'wbs_id', 'clndr_id', 'task_code', 'task_name', 'task_type',
             'status_code', 'total_float_hr_cnt', 'free_float_hr_cnt', 'target_drtn_hr_cnt',
             'remain_drtn_hr_cnt', 'cstr_type', 'cstr_date', 'cstr_type2', 'cstr_date2',
             'act_start_date', 'act_end_date', 'early_start_date', 'early_end_date',
             'target_start_date', 'target_end_date', 'driving_path_flag', 'float_path'],
    'TASKPRED': ['task_id', 'pred_task_id', 'pred_type', 'lag_hr_cnt'],
    'TASKRSRC': ['task_id', 'rsrc_id', 'target_cost', 'target_qty'],
    'RSRC': ['rsrc_id', 'rsrc_name', 'rsrc_short_name', 'rsrc_type'],
}

DUREE_LONGUE_J = 44        # seuils DCMA, en jours ouvrés
MARGE_HAUTE_J = 44

TYPE_TACHE = {'TT_Task': 'tâche', 'TT_Mile': 'jalon début', 'TT_FinMile': 'jalon fin',
              'TT_LOE': 'niveau d\'effort', 'TT_WBS': 'récapitulative WBS', 'TT_Rsrc': 'tâche ressource'}
STATUT = {'TK_NotStart': 'non démarrée', 'TK_Active': 'en cours', 'TK_Complete': 'terminée'}
TYPE_LIEN = {'PR_FS': 'FD (fin → début)', 'PR_SS': 'DD (début → début)',
             'PR_FF': 'FF (fin → fin)', 'PR_SF': 'DF (début → fin)'}
# Contraintes « dures » : elles imposent une date au lieu de la laisser découler de la logique.
CSTR_DURES = {'CS_MANDSTART', 'CS_MANDFIN', 'CS_MSO', 'CS_MSOA', 'CS_MSOB'}
CSTR_NOM = {
    'CS_ALAP': 'au plus tard (ALAP)', 'CS_MEO': 'début au plus tôt le',
    'CS_MEOA': 'début au plus tôt le', 'CS_MEOB': 'début au plus tard le',
    'CS_MANDSTART': 'début obligatoire', 'CS_MANDFIN': 'fin obligatoire',
    'CS_MSO': 'démarrage imposé', 'CS_MSOA': 'fin au plus tôt le', 'CS_MSOB': 'fin au plus tard le',
}


def pct(n, total):
    return f'{100.0 * n / total:5.1f} %' if total else '    — '


class Rapport:
    """Accumule les lignes du rapport ; tout est écrit d'un coup à la fin."""

    def __init__(self):
        self.lignes = []

    def titre(self, t):
        self.lignes += ['', '=' * 78, t.upper(), '=' * 78]

    def section(self, t):
        self.lignes += ['', '── ' + t + ' ' + '─' * max(0, 74 - len(t))]

    def dire(self, *l):
        self.lignes += list(l)

    def tableau(self, entetes, rangs, aligne_droite=()):
        cols = [max(len(str(e)), *(len(str(r[i])) for r in rangs)) if rangs else len(str(e))
                for i, e in enumerate(entetes)]
        fmt = lambda r: '  '.join(
            (str(v).rjust(cols[i]) if i in aligne_droite else str(v).ljust(cols[i]))
            for i, v in enumerate(r))
        self.lignes.append('  ' + fmt(entetes))
        self.lignes.append('  ' + '  '.join('─' * c for c in cols))
        for r in rangs:
            self.lignes.append('  ' + fmt(r))

    def texte(self):
        return '\n'.join(self.lignes) + '\n'


def analyser(chemin, rap):
    rap.dire(f'Fichier : {chemin}')
    t = lire(chemin, BESOINS)
    taches = t['TASK']
    liens = t['TASKPRED']
    cals = {c['clndr_id']: c for c in t['CALENDAR']}
    par_id = {x['task_id']: x for x in taches}

    # Heures par jour du calendrier de l'activité : sans cela, comparer des durées en heures
    # entre une activité en 8 h et une en 24 h n'a aucun sens.
    def hj(tache):
        c = cals.get(tache.get('clndr_id'))
        v = reel(c['day_hr_cnt']) if c else 8.0
        return v if v > 0 else 8.0

    # ---------------------------------------------------------------- projet
    rap.titre('1. Projet et options de calcul')
    proj = t['PROJECT'][0] if t['PROJECT'] else {}
    dd = date(proj.get('last_recalc_date'))
    rap.dire(f"  Projet             : {proj.get('proj_short_name', '?')}",
             f"  Date d'état        : {dd:%d/%m/%Y} " % () if dd else "  Date d'état        : —",
             f"  Début planifié     : {date(proj.get('plan_start_date')) and date(proj['plan_start_date']).strftime('%d/%m/%Y') or '—'}",
             f"  Fin planifiée      : {date(proj.get('scd_end_date')) and date(proj['scd_end_date']).strftime('%d/%m/%Y') or '—'}")
    if t.get('SCHEDOPTIONS'):
        o = t['SCHEDOPTIONS'][0]
        interessant = [
            ('sched_retained_logic', 'Logique conservée hors séquence'),
            ('sched_progress_override', 'Progression prioritaire hors séquence'),
            ('sched_float_type', 'Base de calcul de la marge'),
            ('sched_calendar_on_relationship_lag', 'Calendrier appliqué aux décalages'),
            ('sched_open_critical_flag', 'Extrémités ouvertes vues comme critiques'),
            ('sched_outer_depend_type', 'Traitement des liens externes'),
            ('enable_multiple_longest_path_calc', 'Chemins déterminants multiples'),
        ]
        rap.section('Options de calcul du planning')
        rap.tableau(['Option', 'Valeur'],
                    [[lib, o.get(k, '—') or '—'] for k, lib in interessant if k in o])

    # ---------------------------------------------------------------- volumétrie
    rap.titre('2. Volumétrie')
    n = len(taches)
    rap.dire(f'  {n:>7} activités', f'  {len(liens):>7} liens de logique',
             f'  {len(t["PROJWBS"]):>7} nœuds WBS', f'  {len(cals):>7} calendriers',
             f'  {len(t["RSRC"]):>7} ressources', f'  {len(t["TASKRSRC"]):>7} affectations de ressource',
             '',
             f'  Densité : {len(liens) / n:.2f} lien par activité.')
    rap.dire('  Repère : un planning correctement maillé tourne entre 1,5 et 2,5. En deçà, la',
             "  logique est incomplète ; bien au-delà, elle est redondante.")

    rap.section('Activités par type')
    par_type = collections.Counter(x['task_type'] for x in taches)
    rap.tableau(['Type', 'Nombre', 'Part'],
                [[TYPE_TACHE.get(k, k), v, pct(v, n)] for k, v in par_type.most_common()], (1, 2))
    rap.section('Activités par statut')
    par_st = collections.Counter(x['status_code'] for x in taches)
    rap.tableau(['Statut', 'Nombre', 'Part'],
                [[STATUT.get(k, k), v, pct(v, n)] for k, v in par_st.most_common()], (1, 2))

    # ---------------------------------------------------------------- logique
    rap.titre('3. Logique')
    succ = collections.defaultdict(list)
    pred = collections.defaultdict(list)
    for l in liens:
        succ[l['pred_task_id']].append(l)
        pred[l['task_id']].append(l)

    rap.section('Types de liens (DCMA 3 : au moins 90 % de fin → début)')
    par_lien = collections.Counter(l['pred_type'] for l in liens)
    rap.tableau(['Type', 'Nombre', 'Part'],
                [[TYPE_LIEN.get(k, k), v, pct(v, len(liens))] for k, v in par_lien.most_common()], (1, 2))

    rap.section('Décalages (DCMA 2 : au plus 5 % de lags ; DCMA 4 : aucun lead)')
    lags = [reel(l['lag_hr_cnt']) for l in liens]
    nlag = sum(1 for v in lags if v > 0)
    nlead = sum(1 for v in lags if v < 0)
    rap.tableau(['Décalage', 'Nombre', 'Part'],
                [['nul', len(lags) - nlag - nlead, pct(len(lags) - nlag - nlead, len(lags))],
                 ['positif (lag)', nlag, pct(nlag, len(lags))],
                 ['négatif (lead)', nlead, pct(nlead, len(lags))]], (1, 2))
    if nlag:
        gros = sorted((v for v in lags if v > 0), reverse=True)
        rap.dire(f'  Lag le plus long : {gros[0] / 8:.0f} j ouvrés (à 8 h/j). '
                 f'Médiane des lags : {gros[len(gros) // 2] / 8:.1f} j.')
    if nlead:
        rap.dire(f"  ⚠ {nlead} lead(s) : un successeur démarre avant la fin de son prédécesseur.",
                 "    Le chemin critique calculé par P6 en devient discutable.")

    rap.section('Extrémités ouvertes (DCMA 1)')
    # Les récapitulatives WBS et les niveaux d'effort n'ont pas à porter de logique propre.
    reels = [x for x in taches if x['task_type'] in ('TT_Task', 'TT_Mile', 'TT_FinMile')]
    sans_pred = [x for x in reels if not pred[x['task_id']]]
    sans_succ = [x for x in reels if not succ[x['task_id']]]
    orphelins = [x for x in reels if not pred[x['task_id']] and not succ[x['task_id']]]
    rap.tableau(['Cas', 'Nombre', 'Part des activités réelles'],
                [['sans prédécesseur', len(sans_pred), pct(len(sans_pred), len(reels))],
                 ['sans successeur', len(sans_succ), pct(len(sans_succ), len(reels))],
                 ['ni l\'un ni l\'autre (isolées)', len(orphelins), pct(len(orphelins), len(reels))]], (1, 2))
    rap.dire(f'  ({len(reels)} activités réelles : tâches et jalons, hors récapitulatives et',
             "   niveaux d'effort, qui n'ont pas à porter de logique propre.)")

    # ---------------------------------------------------------------- contraintes
    rap.titre('4. Contraintes (DCMA 5 : au plus 5 % de contraintes dures)')
    contraintes = collections.Counter()
    for x in taches:
        for k in ('cstr_type', 'cstr_type2'):
            if x.get(k):
                contraintes[x[k]] += 1
    ndur = sum(v for k, v in contraintes.items() if k in CSTR_DURES)
    ntot = sum(contraintes.values())
    if contraintes:
        rap.tableau(['Contrainte', 'Nombre', 'Part des activités', 'Dure ?'],
                    [[CSTR_NOM.get(k, k), v, pct(v, n), 'oui' if k in CSTR_DURES else '']
                     for k, v in contraintes.most_common()], (1, 2))
    rap.dire('', f'  Total : {ntot} contrainte(s) sur {n} activités ({pct(ntot, n).strip()}),',
             f'  dont {ndur} dure(s) ({pct(ndur, n).strip()}).')

    # ---------------------------------------------------------------- marges
    rap.titre('5. Marges et durées')
    marges = [(x, reel(x['total_float_hr_cnt']) / hj(x)) for x in reels
              if x['status_code'] != 'TK_Complete' and x.get('total_float_hr_cnt') != '']
    neg = [(x, m) for x, m in marges if m < 0]
    zero = [(x, m) for x, m in marges if -1e-9 <= m <= 1e-9]
    haute = [(x, m) for x, m in marges if m > MARGE_HAUTE_J]
    rap.section('Marge totale (DCMA 6 : ≤ 5 % au-delà de 44 j ; DCMA 7 : aucune négative)')
    rap.tableau(['Marge', 'Nombre', 'Part des activités non terminées'],
                [['négative', len(neg), pct(len(neg), len(marges))],
                 ['nulle (critique)', len(zero), pct(len(zero), len(marges))],
                 [f'supérieure à {MARGE_HAUTE_J} j', len(haute), pct(len(haute), len(marges))]], (1, 2))
    if neg:
        pire = sorted(neg, key=lambda p: p[1])[:8]
        rap.dire('', '  Les marges les plus négatives :')
        rap.tableau(['Code', 'Activité', 'Marge (j)'],
                    [[x['task_code'], x['task_name'][:52], f'{m:.0f}'] for x, m in pire], (2,))

    rap.section(f'Durées (DCMA 8 : au plus 5 % au-delà de {DUREE_LONGUE_J} j)')
    durees = [(x, reel(x['target_drtn_hr_cnt']) / hj(x)) for x in reels if x['task_type'] == 'TT_Task']
    longues = [(x, d) for x, d in durees if d > DUREE_LONGUE_J]
    rap.dire(f'  {len(longues)} tâche(s) de plus de {DUREE_LONGUE_J} j sur {len(durees)} '
             f'({pct(len(longues), len(durees)).strip()}).')
    if longues:
        rap.dire('', '  Les plus longues :')
        rap.tableau(['Code', 'Activité', 'Durée (j)'],
                    [[x['task_code'], x['task_name'][:52], f'{d:.0f}']
                     for x, d in sorted(longues, key=lambda p: -p[1])[:8]], (2,))

    # ---------------------------------------------------------------- dates
    rap.titre('6. Cohérence des dates (DCMA 9)')
    if dd:
        futur = [x for x in reels if (date(x['act_start_date']) or date(x['act_end_date']))
                 and max(d for d in (date(x['act_start_date']), date(x['act_end_date'])) if d) > dd]
        passe = [x for x in reels if x['status_code'] != 'TK_Complete'
                 and (date(x['early_start_date']) or datetime.datetime.max) < dd]
        rap.tableau(['Cas', 'Nombre'],
                    [[f"réalisé postérieur à la date d'état ({dd:%d/%m/%Y})", len(futur)],
                     ["prévisionnel antérieur à la date d'état", len(passe)]], (1,))
    else:
        rap.dire("  Pas de date d'état dans l'export : contrôle impossible.")

    # ---------------------------------------------------------------- ressources
    rap.titre('7. Ressources (DCMA 10)')
    avec = {a['task_id'] for a in t['TASKRSRC']}
    sans = [x for x in reels if x['task_type'] == 'TT_Task' and x['task_id'] not in avec]
    rap.dire(f'  {len(sans)} tâche(s) sans aucune ressource ni coût sur {len(durees)} '
             f'({pct(len(sans), len(durees)).strip()}).')
    par_rsrc = collections.Counter(a['rsrc_id'] for a in t['TASKRSRC'])
    noms = {r['rsrc_id']: (r['rsrc_short_name'] or r['rsrc_name']) for r in t['RSRC']}
    rap.dire('', '  Ressources les plus sollicitées :')
    rap.tableau(['Ressource', 'Affectations'],
                [[noms.get(k, k)[:52], v] for k, v in par_rsrc.most_common(10)], (1,))

    # ---------------------------------------------------------------- calendriers
    rap.titre('8. Calendriers')
    utilises = collections.Counter(x['clndr_id'] for x in taches)
    rap.dire(f'  {len(cals)} calendrier(s) déclaré(s), {len(utilises)} réellement utilisé(s)',
             f'  par des activités — {len(cals) - len(utilises)} inutilisé(s).')
    rap.dire('', '  Les plus employés :')
    rap.tableau(['Calendrier', 'h/j', 'Activités'],
                [[(cals.get(k, {}).get('clndr_name') or k)[:52],
                  f"{reel(cals.get(k, {}).get('day_hr_cnt', 8)):.0f}", v]
                 for k, v in utilises.most_common(10)], (1, 2))
    # Un lien entre deux calendriers différents fabrique des jours ouvrés qui n'existent que
    # d'un côté. C'est parfois un défaut, mais pas toujours : sur des travaux maritimes, un
    # calendrier réduit encode la praticabilité météo d'un moyen, et la traversée entre un
    # quai ouvert 24 h et une drague limitée par l'état de mer est alors parfaitement fondée.
    # Le chiffre se lit, il ne se corrige pas de lui-même.
    croises = sum(1 for l in liens
                  if l['task_id'] in par_id and l['pred_task_id'] in par_id
                  and par_id[l['task_id']]['clndr_id'] != par_id[l['pred_task_id']]['clndr_id'])
    rap.dire('', f'  {croises} lien(s) relient deux activités de calendriers différents '
             f'({pct(croises, len(liens)).strip()}).',
             "  Chaque traversée fabrique des jours ouvrés d'un seul côté du lien. À vérifier",
             '  au cas par cas : sur des travaux en mer, un calendrier réduit peut encoder la',
             "  praticabilité météo d'un moyen, et la traversée est alors justifiée.")
    # Même moyen déclaré avec deux longueurs de journée : les durées cessent d'être comparables
    # d'une phase à l'autre, puisque P6 convertit les heures en jours par `day_hr_cnt`.
    parAn = collections.defaultdict(set)
    for k in utilises:
        c = cals.get(k, {})
        parAn[(round(reel(c.get('year_hr_cnt', 0))), (c.get('clndr_name') or '')[:14])].add(
            round(reel(c.get('day_hr_cnt', 8))))
    melanges = {k: v for k, v in parAn.items() if len(v) > 1}
    if melanges:
        rap.dire('', '  Même capacité annuelle, longueur de journée différente :')
        rap.tableau(['h/an', 'Préfixe de calendrier', 'h/j déclarées'],
                    [[a, n, ' et '.join(str(x) for x in sorted(v))] for (a, n), v in
                     sorted(melanges.items())[:10]], (0,))
        rap.dire("  P6 convertit les durées en jours par `day_hr_cnt` : une tâche « de 3 jours »",
                 "  ne vaut pas le même nombre d'heures selon la version du calendrier employée.")

    # ---------------------------------------------------------------- WBS
    rap.titre('9. Arborescence WBS')
    parents = {w['wbs_id']: w['parent_wbs_id'] for w in t['PROJWBS']}

    def profondeur(w):
        d, vus = 0, set()
        while w and w in parents and w not in vus:
            vus.add(w)
            w = parents[w]
            d += 1
        return d
    prof = collections.Counter(profondeur(w['wbs_id']) for w in t['PROJWBS'])
    charge = collections.Counter(x['wbs_id'] for x in taches)
    vides = sum(1 for w in t['PROJWBS'] if not charge.get(w['wbs_id']))
    rap.dire(f"  {len(t['PROJWBS'])} nœuds, profondeur maximale {max(prof)}, "
             f"{vides} nœud(s) sans aucune activité.")
    rap.tableau(['Profondeur', 'Nœuds'], [[k, prof[k]] for k in sorted(prof)], (0, 1))

    # ---------------------------------------------------------------- chemin déterminant
    rap.titre('10. Chemin déterminant, tel que P6 l\'a calculé')
    pilotes = [x for x in taches if x.get('driving_path_flag') == 'Y']
    rap.dire(f'  {len(pilotes)} activité(s) portent le drapeau de chemin déterminant '
             f'({pct(len(pilotes), n).strip()}).')
    if pilotes:
        dpar = collections.Counter(x['task_type'] for x in pilotes)
        rap.tableau(['Type', 'Nombre'], [[TYPE_TACHE.get(k, k), v] for k, v in dpar.most_common()], (1,))
        lags_crit = [l for l in liens if l['task_id'] in {x['task_id'] for x in pilotes}
                     and reel(l['lag_hr_cnt']) > 0]
        rap.dire('', f'  {len(lags_crit)} lien(s) à décalage positif aboutissent sur le chemin',
                 '  déterminant : autant de jours de projet sans tâche ni ressource en face.')
    return t


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('xer')
    ap.add_argument('-o', '--out', help='fichier de sortie (défaut : sortie standard)')
    args = ap.parse_args()

    rap = Rapport()
    rap.dire('AUDIT D\'UN PLANNING P6', '=' * 78)
    analyser(args.xer, rap)
    texte = rap.texte()
    if args.out:
        open(args.out, 'w', encoding='utf-8').write(texte)
        print(f'{args.out} écrit — {len(texte.splitlines())} lignes', file=sys.stderr)
    else:
        print(texte)


if __name__ == '__main__':
    main()
