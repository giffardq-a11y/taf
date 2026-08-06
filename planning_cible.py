"""Écrit le planning d'occupation du site, dans la forme du Target schedule utilisé sur place.

    node planning_runner.js classeur.xlsx 2026-08-05 > plan.json
    python3 planning_cible.py plan.json Target_schedule_solveur.xlsx

Une ligne par ressource, une colonne par demi-semaine, une barre fusionnée par occupation :
c'est la lecture du planning d'atelier, pas un diagramme d'activités. Les ressources que le
solveur ne modélise pas gardent leur ligne, vide et signalée — le tableau reste superposable à
l'original, et ce qui manque se voit.
"""
import json, sys
from datetime import date, timedelta
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.cell.cell import MergedCell
from openpyxl.utils import get_column_letter

SRC, DST = sys.argv[1], sys.argv[2]
D = json.load(open(SRC))
ELEMENTS = D['elements']

# --- Ressources du planning, dans l'ordre de l'original ---------------------------------
# ('libellé', source, paramètre). source vaut None quand la ressource n'est pas modélisée :
# la ligne existe quand même, pour que le planning reste superposable à celui du chantier.
GRILLE = []
# L'après-coulée se fait sur deux fronts distincts : « Repairs + Integrated outfitting », en
# aval de la zone de casting et avant le mouvement vers l'Upper Basin, puis « Outfitting UB »
# une fois l'élément déplacé. La phase d'outfitting du solveur est la première — celle qui suit
# immédiatement la coulée, sur la ligne. La seconde n'est pas modélisée et garde sa ligne vide.
for n in range(1, 6):
    GRILLE.append((f'Line {n} - STE Casting', 'beton', n))
    GRILLE.append((f'Line {n} - STE Repairs + Integrated out', 'outfitting', n))
    GRILLE.append((f'Line {n} - Outfitting UB', None, None))
GRILLE += [
    ('Cage Prefabrication Area', 'zone', 1),   # CPA
    ('Casting Pit 1', 'zone', 2),              # CP1
    ('Casting Pit 2', 'zone', 3),              # CP2
    ('Casting Pit 3', 'zone', 4),              # CP3
    ('Outfitting buffer area', 'zone', 5),     # UB1 — l'aire tampon est dans le Basin C
    ('Upper Basin 1', 'zone', 6),              # UB2
    ('Upper Basin 2', 'zone', 7),              # UB3
    ('MPP Repair', None, None),
]
GRILLE += [(f'Lower basin {p}', 'basin', p) for p in range(1, 7)]
GRILLE += [('Harbour Parking SPE', 'stockageSPE', None)]
GRILLE += [(f'Harbour Parking {p}', 'parking', p) for p in range(1, 7)]
GRILLE += [
    ('Hookup', 'hookup', None),
    ('Ballast jetty', 'ballast', None),
    ('Trench verification', None, None),
    ('Trench rectification (leveling layer)', None, None),
    ('Gravel bed', None, None),
    ('Immersion', 'immersion', None),
    ('Locking fill & Backfill', None, None),
]

COULEURS = {
    'beton': 'FFFF00', 'outfitting': '00B050', 'zone': 'A39FE9', 'basin': '9DC3E6',
    'stockageSPE': 'C9B6EC', 'parking': 'D9D9D9', 'hookup': '7FC6CE', 'ballast': 'ED9B33',
    'immersion': 'FF0000',
}
POLICE = 'Arial'
TRAIT = Side(style='thin', color='BFBFBF')
BORDURE = Border(left=TRAIT, right=TRAIT, top=TRAIT, bottom=TRAIT)
MOIS_FR = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

def jour(s):
    return date.fromisoformat(s) if s else None

def etiquette(ident):
    # « STE-61 » devient « TE-61 », comme sur le planning du chantier ; les SPE gardent le leur.
    return ident[1:] if ident.startswith('STE-') else ident

# --- Occupations : (ligne de la grille, début, fin, étiquette) ---------------------------
def occupations():
    out = []
    for e in ELEMENTS:
        lab = etiquette(e['id'])
        def barre(libelle, bornes):
            d, f = jour(bornes[0]), jour(bornes[1])
            if d and f and f > d:
                out.append((libelle, d, f, lab))
        barre(f"Line {e['ligne']} - STE Casting", e['beton']) if e['ligne'] <= 5 else None
        if e['ligne'] <= 5:
            barre(f"Line {e['ligne']} - STE Repairs + Integrated out", e['outfitting'])
        if e['zones']:
            # Une zone SPE est occupée jusqu'à l'entrée dans la suivante ; la dernière, jusqu'au
            # float-up. Le planning ne date pas de sortie, la simulation si.
            zs = {int(k): jour(v) for k, v in e['zones'].items()}
            for z in sorted(zs):
                libelle = next((g[0] for g in GRILLE if g[1] == 'zone' and g[2] == z), None)
                if not libelle:
                    continue
                fin = zs.get(z + 1) or jour(e['floatUp'][0]) or jour(e['outfitting'][1])
                if fin and fin > zs[z]:
                    out.append((libelle, zs[z], fin, lab))
        if e['basinNum'] and e['basinPlace']:
            barre(f"Lower basin {(e['basinNum'] - 1) * 2 + e['basinPlace']}", e['basin'])
        if e['stockageSPENum']:
            barre('Harbour Parking SPE', e['stockageSPE'])
        if e['parkingNum']:
            barre(f"Harbour Parking {e['parkingNum']}", e['parking'])
        barre('Hookup', e['hookup'])
        barre('Ballast jetty', e['ballast'])
        if e['immersion']:
            d = jour(e['immersion'])
            out.append(('Immersion', d, d + timedelta(days=1), lab))
    return out

OCC = occupations()
if not OCC:
    sys.exit('aucune occupation à tracer — le solveur n\'a rien produit')

# --- Axe du temps : une semaine = deux colonnes, comme sur le planning du chantier --------
DEB = min(o[1] for o in OCC)
DEB -= timedelta(days=DEB.weekday())          # caler sur le lundi
FIN = max(o[2] for o in OCC)
NB_SEM = (FIN - DEB).days // 7 + 2
COL0 = 2                                       # colonne A = libellés, la grille commence en B

# Une colonne vaut une demi-semaine : c'est la résolution de l'original, et elle sépare des
# occupations successives qu'une colonne hebdomadaire écraserait l'une sur l'autre — le hook-up
# ne dure que trois jours et demi.
PAS_JOURS = 3.5

def colonne(d):
    """Colonne de la demi-semaine contenant d."""
    return COL0 + int((d - DEB).days // PAS_JOURS)

wb = Workbook()
ws = wb.active
ws.title = 'Target schedule'

R_TITRE, R_MOIS, R_SEM, R_DATE, R0 = 1, 4, 5, 6, 8

p = D['parametres']
ws.cell(R_TITRE, 1, f"Target schedule — solveur de cadence").font = Font(name=POLICE, size=14, bold=True)
ws.cell(2, 1, f"{D['classeur']} · date de référence {jour(D['dateRef']).strftime('%d/%m/%Y')}"
              f" · séquence {p['variante']}{' optimisée' if p['optimiseur'] else ' du classeur'}"
              f" · {'arrêt au plus tôt' if p['arretAuPlusTot'] else 'flux tendu'}"
              f"{' · accélération en cours de cycle' if p['accelererEnCoursCycle'] else ''}"
              f"{' · staggering' if p['staggering'] else ''}").font = Font(name=POLICE, size=9, italic=True)
k = D['kpi']
ws.cell(3, 1, f"{k['retards']} élément(s) en retard · {k['bloques']} bloqué(s) ·"
              f" {k['changements']} changement(s) de cadence · production finie le "
              f"{jour(k['finProduction']).strftime('%d/%m/%Y') if k['finProduction'] else '—'}"
       ).font = Font(name=POLICE, size=9, bold=True)

# En-tête : mois fusionnés sur leurs semaines, numéro de semaine, lundi de la semaine.
ws.cell(R_MOIS, 1, 'Month').font = Font(name=POLICE, size=9, bold=True)
ws.cell(R_SEM, 1, 'Week').font = Font(name=POLICE, size=9, bold=True)
ws.cell(R_DATE, 1, 'Semaine du').font = Font(name=POLICE, size=9, bold=True)
mois_debut, mois_cle = COL0, None
for s in range(NB_SEM):
    d = DEB + timedelta(weeks=s)
    c = COL0 + s * 2
    cle = (d.year, d.month)
    if mois_cle is None:
        mois_cle = cle
    elif cle != mois_cle:
        ws.merge_cells(start_row=R_MOIS, start_column=mois_debut, end_row=R_MOIS, end_column=c - 1)
        cel = ws.cell(R_MOIS, mois_debut, f'{MOIS_FR[mois_cle[1] - 1]}-{str(mois_cle[0])[2:]}')
        cel.font = Font(name=POLICE, size=9, bold=True)
        cel.alignment = Alignment(horizontal='center')
        cel.fill = PatternFill('solid', fgColor='EDEDED')
        mois_debut, mois_cle = c, cle
    ws.merge_cells(start_row=R_SEM, start_column=c, end_row=R_SEM, end_column=c + 1)
    cs = ws.cell(R_SEM, c, d.isocalendar()[1])
    cs.font = Font(name=POLICE, size=8)
    cs.alignment = Alignment(horizontal='center')
    ws.merge_cells(start_row=R_DATE, start_column=c, end_row=R_DATE, end_column=c + 1)
    cd = ws.cell(R_DATE, c, d)
    cd.number_format = 'DD/MM'
    cd.font = Font(name=POLICE, size=8, color='777777')
    cd.alignment = Alignment(horizontal='center')
ws.merge_cells(start_row=R_MOIS, start_column=mois_debut, end_row=R_MOIS, end_column=COL0 + NB_SEM * 2 - 1)
cel = ws.cell(R_MOIS, mois_debut, f'{MOIS_FR[mois_cle[1] - 1]}-{str(mois_cle[0])[2:]}')
cel.font = Font(name=POLICE, size=9, bold=True)
cel.alignment = Alignment(horizontal='center')
cel.fill = PatternFill('solid', fgColor='EDEDED')

# --- Lignes de ressources et barres d'occupation -----------------------------------------
rang = {}
for i, (libelle, source, _) in enumerate(GRILLE):
    r = R0 + i
    rang[libelle] = r
    cel = ws.cell(r, 1, libelle)
    cel.font = Font(name=POLICE, size=9, bold=source is not None,
                    italic=source is None, color='000000' if source else '999999')
    ws.row_dimensions[r].height = 15
    for c in range(COL0, COL0 + NB_SEM * 2):
        ws.cell(r, c).border = BORDURE

hors = [g[0] for g in GRILLE if g[1] is None]
# Deux occupations d'une même ressource peuvent tomber dans la même semaine : la colonne
# hebdomadaire ne les sépare pas. On rogne alors la seconde sur ce qui reste de libre, et on
# compte ce qu'on n'a pas pu tracer — un chiffre annoncé vaut mieux qu'une barre disparue.
occupe, rognees, perdues, simultanees = {}, 0, [], []
for libelle, d, f, lab in sorted(OCC, key=lambda o: (o[0], o[1])):
    r = rang.get(libelle)
    if not r:
        continue
    source = next(g[1] for g in GRILLE if g[0] == libelle)
    c1 = colonne(d)
    c2 = max(c1, colonne(f - timedelta(days=1)))
    pris = occupe.setdefault(r, set())
    while c1 <= c2 and c1 in pris:
        c1 += 1
        rognees += 1
    fin_libre = c1
    while fin_libre + 1 <= c2 and (fin_libre + 1) not in pris:
        fin_libre += 1
    c2 = fin_libre
    if c1 > c2 or c1 in pris:
        # Occupation entièrement recouverte : deux éléments occupent la ressource en même temps.
        # C'est réel — les lignes d'une paire entrent en bassin ensemble, donc leurs hook-up
        # aussi. Une ligne unique ne peut pas les empiler : on accole les deux étiquettes plutôt
        # que d'en perdre une.
        hote = ws.cell(r, colonne(d))
        while isinstance(hote, MergedCell):
            hote = ws.cell(r, hote.column - 1)
        if hote.value and lab not in str(hote.value):
            hote.value = f'{hote.value}/{lab}'
            simultanees.append((libelle, lab))
        continue
    pris.update(range(c1, c2 + 1))
    for c in range(c1, c2 + 1):
        cel = ws.cell(r, c)
        cel.fill = PatternFill('solid', fgColor=COULEURS[source])
        cel.border = BORDURE
    ws.merge_cells(start_row=r, start_column=c1, end_row=r, end_column=c2)
    cel = ws.cell(r, c1, lab)
    cel.font = Font(name=POLICE, size=8, bold=True,
                    color='FFFFFF' if source in ('immersion', 'outfitting') else '000000')
    cel.alignment = Alignment(horizontal='center', vertical='center')

# --- Légende ------------------------------------------------------------------------------
rl = R0 + len(GRILLE) + 2
ws.cell(rl, 1, 'Légende').font = Font(name=POLICE, size=9, bold=True)
LIB = {'beton': 'Casting', 'outfitting': 'Outfitting', 'zone': 'Ligne SPE (CPA→UB3)',
       'basin': 'Lower basin', 'stockageSPE': 'Stockage SPE', 'parking': 'Harbour parking',
       'hookup': 'Hookup', 'ballast': 'Ballast jetty', 'immersion': 'Immersion'}
c = COL0
for cle, lib in LIB.items():
    ws.merge_cells(start_row=rl, start_column=c, end_row=rl, end_column=c + 1)
    cel = ws.cell(rl, c)
    cel.fill = PatternFill('solid', fgColor=COULEURS[cle])
    cel.border = BORDURE
    ws.cell(rl, c + 2, lib).font = Font(name=POLICE, size=8)
    c += 9
ws.cell(rl + 2, 1, 'Lignes en gris : ressources que le solveur ne modélise pas — '
                   + ', '.join(hors)).font = Font(name=POLICE, size=8, italic=True, color='999999')

ws.column_dimensions['A'].width = 34
for s in range(NB_SEM * 2):
    ws.column_dimensions[get_column_letter(COL0 + s)].width = 2.6
ws.freeze_panes = ws.cell(R0, COL0)
ws.sheet_view.zoomScale = 70
wb.save(DST)
print(f'{DST} écrit — {len(GRILLE)} ressources, {NB_SEM} semaines '
      f'({DEB.strftime("%d/%m/%Y")} → {FIN.strftime("%d/%m/%Y")}), {len(OCC)} barres, '
      f'{len(hors)} lignes hors solveur')
if rognees or perdues or simultanees:
    print(f'  {rognees} barre(s) rognées d\'une demi-semaine (occupations qui se suivent de près), '
          f'{len(simultanees)} accolée(s) à une barre simultanée, {len(perdues)} non tracée(s)')
    if perdues:
        print('  non tracées : ' + ', '.join(f'{l} {i}' for l, i in perdues[:8]))
