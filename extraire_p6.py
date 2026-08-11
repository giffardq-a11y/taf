"""Extrait du planning P6 les activités récapitulatives qui alimentent le Gantt, et elles seules.

    python3 extraire_p6.py TUXERev2LinkedActivities.xlsx donnees_p6.txt

Le solveur n'en voit rien : ces dates ne servent qu'à remplir des lignes du planning
d'occupation que la simulation ne calcule pas — travaux marins et finitions. Le plan de
production, lui, reste entièrement issu du solveur.

Les finitions sont lues dans l'arborescence WBS (second onglet), au **plus bas niveau
présent**, qui est déjà par élément et porte ses propres dates de début et de fin. C'est donc
une tâche récapitulative du planning, non une agrégation d'activités faite ici. Les travaux
marins, eux, n'ont pas de nœud WBS qui les isole : ils restent lus dans les activités.
"""
import re, sys
from collections import defaultdict
from openpyxl import load_workbook

SRC, DST = sys.argv[1], sys.argv[2]

# Familles de finition, par leur nom de nœud WBS. Le plus bas niveau de chacune est par
# élément — ou par joint, pour les travaux qui se font entre deux éléments.
FAMILLES_WBS = {
    'Immersion Joint Removal': 'bhrem',           # dépose des bulkheads au joint d'immersion
    'Immersion Joint infill Concrete': 'infill',
    'Omega seal installation': 'omega',
    'Removal of TE System': 'tesys',
    'Drainage Installation': 'drain',
    'Walkways': 'walk',
}
# Travaux marins et jalons, sans nœud WBS propre : repérés sur le nom d'activité.
PAR_NOM = [
    (re.compile(r'^Gravel Bed', re.I), 'gravel'),
    (re.compile(r'Leveling Layer Installation', re.I), 'level'),
    (re.compile(r'^(Locking fill|Backfill)', re.I), 'lock'),
    (re.compile(r'Element ready for floatup', re.I), 'readyfu'),
]

# Jeton d'élément dans un code WBS. Le planning en use plusieurs formes : « 77 » pour un
# élément standard, « SP10 » ou « SPE08 » pour un spécial, « 77-78 » ou « 76-SP10 » pour un
# joint, « TPR-77 » pour le joint de tête. Les travaux de joint gardent leurs deux numéros —
# c'est bien ce qu'ils désignent, l'espace entre deux éléments.
RX_PART = r'(?:SPE?0*\d{1,2}|\d{1,2})'
RX_JETON = re.compile(r'^(?:TPR-)?(%s)(?:-(%s))?$' % (RX_PART, RX_PART), re.I)

def normaliser(p):
    m = re.match(r'^SPE?0*(\d{1,2})$', p, re.I)
    return ('S%02d' % int(m.group(1))) if m else ('%02d' % int(p))

def jeton_wbs(code, famille):
    seg = str(code).strip().split('.')
    # Les walkways vivent sous FIT.<n>.<élément>.4.2 ; les autres finitions sous
    # FIN.FUN.TN<n>.<élément ou joint>.<n>, où le jeton est l'avant-dernier segment.
    if famille == 'walk' and len(seg) > 3 and seg[1] == 'FIT':
        cand = [seg[3], seg[-2]]
    else:
        cand = [seg[-2]] if len(seg) >= 2 else []
    for c in cand:
        m = RX_JETON.match(c)
        if m:
            a = normaliser(m.group(1))
            return (a + '-' + normaliser(m.group(2))) if m.group(2) else a
    return None

# Identifiant d'élément dans un nom d'activité, pour les travaux marins.
RX_ID = re.compile(r'\b(S?TE|SPE?)[\s.\-]*0*(\d{1,2})\b', re.I)

def id_activite(nom):
    m = RX_ID.search(nom)
    if not m:
        return None
    n = int(m.group(2))
    return ('SPE-%02d' if m.group(1).upper().startswith('SP') else 'STE-%02d') % n

def jour(v):
    return v.date().isoformat() if hasattr(v, 'date') else None

wb = load_workbook(SRC, read_only=True, data_only=True)
bornes = {}
inv = {'sans jeton': 0, 'sans date': 0}

# --- Finitions : nœuds WBS du second onglet ---
for r in wb['Feuil1'].iter_rows(min_row=2, values_only=True):
    if r[0] is None:
        continue
    fam = FAMILLES_WBS.get(str(r[1] or '').strip())
    if not fam:
        continue
    jet = jeton_wbs(r[0], fam)
    d, f = jour(r[4]), jour(r[5])
    if not jet:
        inv['sans jeton'] += 1
        continue
    if not d or not f:
        inv['sans date'] += 1
        continue
    bornes[(jet, fam)] = (d, f)

# --- Travaux marins : bornes des activités, faute d'un nœud WBS qui les isole ---
marins = defaultdict(lambda: [None, None])
for r in wb['TASK'].iter_rows(min_row=3, values_only=True):
    if r[3] is None:
        continue
    nom = str(r[3])
    cat = next((c for rx, c in PAR_NOM if rx.search(nom)), None)
    if not cat:
        continue
    ident = id_activite(nom)
    d, f = jour(r[4]), jour(r[5])
    if not ident or not d or not f:
        inv['sans date'] += 1
        continue
    n = int(ident.split('-')[1])
    jet = ('S%02d' % n) if ident.startswith('SPE-') else ('%02d' % n)
    b = marins[(jet, cat)]
    if b[0] is None or d < b[0]:
        b[0] = d
    if b[1] is None or f > b[1]:
        b[1] = f
for k, v in marins.items():
    bornes[k] = tuple(v)

lignes = ['%s|%s|%s|%s' % (j, c, d, f) for (j, c), (d, f) in sorted(bornes.items())]
open(DST, 'w').write(';'.join(lignes))

par_cat = defaultdict(int)
for (j, c) in bornes:
    par_cat[c] += 1
print(f'{DST} écrit — {len(bornes)} tâches récapitulatives, {inv["sans jeton"]} sans jeton, '
      f'{inv["sans date"]} sans date')
for c in sorted(par_cat):
    print(f'   {c:8} : {par_cat[c]:3} jetons')
