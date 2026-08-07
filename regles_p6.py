"""Déduit les règles de fonctionnement d'un planning P6 répétitif, par fouille de motifs.

    python3 regles_p6.py planning.xer --portee TUX-MAR,TUX-FLO -o regles.txt

Le principe. Un planning de tunnel immergé répète le même enchaînement pour chaque élément :
89 fois la même dizaine d'activités, reliées de la même façon. Lire les 1 800 activités une par
une n'apprend rien ; les replier sur leur modèle apprend tout.

On retire donc de chaque nom d'activité le jeton d'élément — `TE-76`, `STE-68/69`, `SPE-04` —
et ce qui reste est le **rôle** : « Gravel Bed », « Immersion », « Locking fill ». Le planning
devient un graphe de quelques dizaines de rôles au lieu de milliers d'activités. Chaque relation
entre deux rôles porte alors un **support** : sur combien d'éléments elle existe réellement.

  support 89/89  → règle dure du planning ;
  support 80/89  → une règle et neuf dérogations, et ce sont les dérogations qui intéressent ;
  support  3/89  → bruit, ou vrai cas particulier.

Le décalage d'élément (Δ) dit si le lien va d'un élément à lui-même (Δ=0) ou à son voisin dans
l'ordre de pose (Δ=±1) : c'est ainsi qu'on retrouve les règles de cadence et d'enchaînement.

Ce que le script ne fait pas : décider. Une règle à 89/89 peut être une contrainte physique ou
un copier-coller reproduit 89 fois sans que personne ne l'ait jamais rejugé. Le recueil dit ce
qui est ; c'est au planificateur de dire ce qui doit être.
"""
import argparse
import collections
import re
import statistics
import sys

from lire_xer import lire, reel, date

BESOINS = {
    'TASK': ['task_id', 'wbs_id', 'clndr_id', 'task_code', 'task_name', 'task_type',
             'status_code', 'target_drtn_hr_cnt', 'total_float_hr_cnt', 'cstr_type',
             'cstr_date', 'cstr_type2', 'early_start_date', 'target_start_date'],
    'TASKPRED': ['task_id', 'pred_task_id', 'pred_type', 'lag_hr_cnt'],
    'PROJWBS': ['wbs_id', 'parent_wbs_id', 'wbs_name'],
    'CALENDAR': ['clndr_id', 'clndr_name', 'day_hr_cnt'],
}

# Jeton d'élément dans un nom d'activité : TE-76, STE-68, SPE-04, SP10, et les formes doubles
# « STE-68/69 » d'une activité qui porte sur une paire.
RX_EL = re.compile(r'\b(S?TE|SPE?)[-. ]?(\d{1,3})(?:\s*/\s*(\d{1,3}))?\b', re.I)
TYPE_LIEN = {'PR_FS': 'FD', 'PR_SS': 'DD', 'PR_FF': 'FF', 'PR_SF': 'DF'}
CSTR_NOM = {'CS_MANDSTART': 'début obligatoire', 'CS_MANDFIN': 'fin obligatoire',
            'CS_MSO': 'démarrage imposé', 'CS_MSOA': 'fin au plus tôt le',
            'CS_MSOB': 'fin au plus tard le', 'CS_MEO': 'début au plus tôt le',
            'CS_MEOB': 'début au plus tard le', 'CS_ALAP': 'au plus tard'}


def role_et_elements(nom):
    """Renvoie (rôle, [numéros d'élément cités]). Le rôle est le nom débarrassé de ses jetons."""
    elems = []
    for m in RX_EL.finditer(nom):
        elems.append(int(m.group(2)))
        if m.group(3):
            elems.append(int(m.group(3)))
    role = RX_EL.sub('<EL>', nom)
    role = re.sub(r'\b\d+\b', '#', role)          # les autres nombres : phases, étapes, parts
    role = re.sub(r'\s+', ' ', role).strip(' -:').strip()
    return role, elems


def jours(tache, cals):
    c = cals.get(tache.get('clndr_id'))
    h = reel(c['day_hr_cnt']) if c else 8.0
    return reel(tache['target_drtn_hr_cnt']) / (h if h > 0 else 8.0)


def resume(vals):
    if not vals:
        return '—'
    v = sorted(vals)
    med = statistics.median(v)
    if abs(v[0] - v[-1]) < 0.05:
        return f'{med:.0f} j'
    return f'{med:.0f} j (de {v[0]:.0f} à {v[-1]:.0f})'


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('xer')
    ap.add_argument('--portee', default='TUX-MAR,TUX-FLO',
                    help='préfixes de code d\'activité définissant le périmètre (séparés par des virgules)')
    ap.add_argument('--support-min', type=int, default=3,
                    help='ne montrer que les liens vus sur au moins tant d\'éléments')
    ap.add_argument('-o', '--out')
    args = ap.parse_args()

    prefixes = tuple(p.strip() for p in args.portee.split(',') if p.strip())
    t = lire(args.xer, BESOINS)
    cals = {c['clndr_id']: c for c in t['CALENDAR']}
    wbs = {w['wbs_id']: w for w in t['PROJWBS']}
    par_id = {x['task_id']: x for x in t['TASK']}

    dans = {x['task_id']: x for x in t['TASK'] if x['task_code'].startswith(prefixes)}
    L = []
    L.append('RÈGLES DE FONCTIONNEMENT DÉDUITES DU PLANNING P6')
    L.append('=' * 78)
    L.append(f'Périmètre : {", ".join(prefixes)} — {len(dans)} activités sur {len(t["TASK"])}.')

    # ---------------------------------------------------- ordre de pose réel
    # Le numéro d'un élément n'est pas son rang de pose : sur ce chantier TE-79 précède TE-76.
    # Comparer deux activités par différence de numéros ne veut donc rien dire. On reconstruit
    # l'ordre à partir des dates d'immersion, et tous les décalages se comptent en rangs.
    imm = {}
    for x in t['TASK']:
        if not re.match(r'^Immersion\s*-\s*', x['task_name'], re.I):
            continue
        _, els = role_et_elements(x['task_name'])
        d = date(x['early_start_date']) or date(x['target_start_date'])
        if els and d and (els[0] not in imm or d < imm[els[0]]):
            imm[els[0]] = d
    rang = {e: i for i, (e, _) in enumerate(sorted(imm.items(), key=lambda kv: kv[1]))}

    # -------------------------------------------------------------- rôles
    roles = collections.defaultdict(list)
    role_de = {}
    for x in dans.values():
        r, els = role_et_elements(x['task_name'])
        roles[r].append((x, els))
        role_de[x['task_id']] = r
    L.append(f'{len(roles)} rôles distincts après retrait des jetons d\'élément.')
    L.append('')
    L.append("Un « rôle » est ce qui reste d'un nom d'activité une fois son numéro d'élément")
    L.append("effacé. Le support est le nombre d'éléments sur lesquels le rôle, ou le lien,")
    L.append('existe réellement.')

    # -------------------------------------------------------------- catalogue des rôles
    L.append('')
    L.append('=' * 78)
    L.append('1. LES RÔLES ET LEURS DURÉES')
    L.append('=' * 78)
    L.append('')
    L.append(f"{'Rôle':<58}{'Nb':>5}  {'Durée médiane':<22}{'Calendrier'}")
    L.append('─' * 78)
    for r, lst in sorted(roles.items(), key=lambda kv: -len(kv[1])):
        if len(lst) < args.support_min:
            continue
        ds = [jours(x, cals) for x, _ in lst if reel(x['target_drtn_hr_cnt']) > 0]
        cnoms = collections.Counter((cals.get(x['clndr_id'], {}).get('clndr_name') or '?')
                                    for x, _ in lst)
        cn, cv = cnoms.most_common(1)[0]
        marque = '' if cv == len(lst) else f' (+{len(cnoms) - 1})'
        L.append(f'{r[:57]:<58}{len(lst):>5}  {resume(ds):<22}{cn[:30]}{marque}')
    petits = [r for r, l in roles.items() if len(l) < args.support_min]
    if petits:
        L.append('')
        L.append(f'{len(petits)} rôle(s) vus sur moins de {args.support_min} éléments, non listés '
                 f'(cas particuliers ou variantes de nom).')

    # -------------------------------------------------------------- enchaînement interne
    L.append('')
    L.append('=' * 78)
    L.append("2. L'ENCHAÎNEMENT, RÔLE PAR RÔLE")
    L.append('=' * 78)
    L.append('')
    L.append("Δ = décalage de RANG DE POSE entre le prédécesseur et le successeur — pas de")
    L.append("numéro d'élément : sur ce chantier l'ordre de pose ne suit pas la numérotation.")
    L.append("Δ=0 : le lien reste sur le même élément. Δ=-1 : le successeur travaille sur")
    L.append("l'élément posé juste avant, autrement dit le lien porte une règle d'enchaînement")
    L.append('entre éléments consécutifs.')
    L.append('')

    liens_int = collections.defaultdict(lambda: {'n': 0, 'els': set(), 'lags': [], 'delta': collections.Counter()})
    interfaces_ent = collections.defaultdict(lambda: {'n': 0, 'els': set()})
    interfaces_sor = collections.defaultdict(lambda: {'n': 0, 'els': set()})
    for l in t['TASKPRED']:
        a, b = l['pred_task_id'], l['task_id']
        da, db = a in dans, b in dans
        if not da and not db:
            continue
        if da and db:
            ra, rb = role_de[a], role_de[b]
            _, ea = role_et_elements(par_id[a]['task_name'])
            _, eb = role_et_elements(par_id[b]['task_name'])
            cle = (ra, rb, l['pred_type'])
            d = liens_int[cle]
            d['n'] += 1
            d['els'].add(eb[0] if eb else None)
            d['lags'].append(reel(l['lag_hr_cnt']))
            if ea and eb and ea[0] in rang and eb[0] in rang:
                d['delta'][rang[eb[0]] - rang[ea[0]]] += 1
        elif db:                                   # entre dans le périmètre
            dehors = par_id.get(a, {})
            rn, _ = role_et_elements(dehors.get('task_name', '?'))
            d = interfaces_ent[(rn, role_de[b])]
            d['n'] += 1
        else:                                      # en sort
            dehors = par_id.get(b, {})
            rn, _ = role_et_elements(dehors.get('task_name', '?'))
            d = interfaces_sor[(role_de[a], rn)]
            d['n'] += 1

    # Regroupé par rôle prédécesseur, pour se lire comme une procédure.
    par_pred = collections.defaultdict(list)
    for (ra, rb, ty), d in liens_int.items():
        par_pred[ra].append((rb, ty, d))
    for ra in sorted(par_pred, key=lambda r: -len(roles.get(r, []))):
        if len(roles.get(ra, [])) < args.support_min:
            continue
        suites = sorted(par_pred[ra], key=lambda s: -s[2]['n'])
        suites = [s for s in suites if s[2]['n'] >= args.support_min]
        if not suites:
            continue
        L.append(f'▸ {ra[:74]}   ({len(roles[ra])} occurrences)')
        for rb, ty, d in suites:
            lags = d['lags']
            lag = '' if all(abs(v) < 1e-9 for v in lags) else \
                  f"  lag {statistics.median(lags) / 8:+.0f} j"
            dd = d['delta'].most_common(1)
            delta = f"  Δ={dd[0][0]:+d}" if dd and dd[0][0] != 0 else ''
            L.append(f'    → {rb[:56]:<57} {TYPE_LIEN.get(ty, ty)}  ×{d["n"]:<4}{delta}{lag}')
        L.append('')

    # -------------------------------------------------------------- cycle type
    L.append('=' * 78)
    L.append("3. LE CYCLE TYPE D'UN ÉLÉMENT")
    L.append('=' * 78)
    L.append('')
    L.append("Pour chaque élément, ses activités du périmètre rangées par date, puis la position")
    L.append("médiane de chaque rôle sur l'ensemble des éléments. C'est la recette telle qu'elle")
    L.append('est réellement exécutée, et non telle qu\'un document la décrit.')
    L.append('')
    par_element = collections.defaultdict(list)
    for r, lst in roles.items():
        for x, els in lst:
            d = date(x['early_start_date']) or date(x['target_start_date'])
            if els and d and els[0] in rang:
                par_element[els[0]].append((d, r, jours(x, cals)))
    pos = collections.defaultdict(list)
    for el, lst in par_element.items():
        lst.sort()
        for i, (_, r, _) in enumerate(lst):
            pos[r].append(i / max(1, len(lst) - 1))
    ordre = sorted((r for r in pos if len(roles[r]) >= max(args.support_min, 10)),
                   key=lambda r: statistics.median(pos[r]))
    L.append(f"{'#':>3}  {'Rôle':<56}{'Éléments':>9}  Durée médiane")
    L.append('─' * 78)
    for i, r in enumerate(ordre, 1):
        ds = [jours(x, cals) for x, _ in roles[r] if reel(x['target_drtn_hr_cnt']) > 0]
        L.append(f'{i:>3}  {r[:55]:<56}{len(roles[r]):>9}  {resume(ds)}')
    L.append('')
    L.append(f'   {len(par_element)} éléments portent un cycle marin complet ou partiel.')

    # -------------------------------------------------------------- interfaces
    L.append('=' * 78)
    L.append('4. INTERFACES AVEC LE RESTE DU PLANNING')
    L.append('=' * 78)
    L.append('')
    L.append("Ce qui déclenche le périmètre, et ce qu'il déclenche. C'est là que se joue le")
    L.append('raccordement entre la production en usine et les travaux en mer.')
    for titre, dico in [('Entrent dans le périmètre', interfaces_ent),
                        ('Sortent du périmètre', interfaces_sor)]:
        L.append('')
        L.append(f'── {titre} ' + '─' * max(0, 74 - len(titre)))
        for (a, b), d in sorted(dico.items(), key=lambda kv: -kv[1]['n'])[:18]:
            if d['n'] < args.support_min:
                continue
            L.append(f'   {a[:44]:<45} → {b[:26]:<27} ×{d["n"]}')

    # -------------------------------------------------------------- contraintes
    L.append('')
    L.append('=' * 78)
    L.append('5. CONTRAINTES ET CALENDRIERS DU PÉRIMÈTRE')
    L.append('=' * 78)
    L.append('')
    cs = collections.Counter()
    detail = collections.defaultdict(list)
    for x in dans.values():
        for k in ('cstr_type', 'cstr_type2'):
            if x.get(k):
                cs[x[k]] += 1
                detail[x[k]].append(x)
    if cs:
        for k, v in cs.most_common():
            L.append(f'   {CSTR_NOM.get(k, k):<32} ×{v}')
            for x in detail[k][:6]:
                d = date(x.get('cstr_date'))
                L.append(f'       {x["task_code"]:<24} {x["task_name"][:40]:<41}'
                         f'{d.strftime("%d/%m/%Y") if d else ""}')
    else:
        L.append('   Aucune contrainte de date dans ce périmètre.')

    L.append('')
    L.append('── Calendriers employés ' + '─' * 55)
    cc = collections.Counter(x['clndr_id'] for x in dans.values())
    for k, v in cc.most_common(10):
        c = cals.get(k, {})
        L.append(f'   {(c.get("clndr_name") or k)[:56]:<57} {reel(c.get("day_hr_cnt", 8)):>3.0f} h/j  ×{v}')
    # Traversées de calendrier à l'intérieur du périmètre : source classique de jours fantômes.
    croises = sum(1 for l in t['TASKPRED']
                  if l['task_id'] in dans and l['pred_task_id'] in dans
                  and dans[l['task_id']]['clndr_id'] != dans[l['pred_task_id']]['clndr_id'])
    total = sum(1 for l in t['TASKPRED'] if l['task_id'] in dans and l['pred_task_id'] in dans)
    L.append('')
    L.append(f'   {croises} lien(s) interne(s) sur {total} relient deux calendriers différents.')

    texte = '\n'.join(L) + '\n'
    if args.out:
        open(args.out, 'w', encoding='utf-8').write(texte)
        print(f'{args.out} écrit — {len(L)} lignes', file=sys.stderr)
    else:
        print(texte)


if __name__ == '__main__':
    main()
