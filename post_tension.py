"""Planning de post-tension en Gantt classique, calé sur les coulées du solveur.

    node planning_runner.js classeur.xlsx 2026-08-05 > plan.json
    python3 post_tension.py plan.json Post_tension.xlsx [--threading 6] [--stressing 4] [--grouting 2]

La règle vient du modèle fourni par Dywidag, cellule E31 : « post tensioning start two days
after casting of SE next element ». La post-tension d'un élément commence donc **deux jours
après le démarrage de la coulée de l'élément suivant sur la même ligne** — le temps que le
poussage ait dégagé l'élément et que le suivant soit engagé. Pour le dernier élément d'une
ligne, faute de suivant, on part de sa propre fin de coulée, plus deux jours.

Les trois opérations s'enchaînent dans l'ordre du modèle : enfilage, mise en tension,
injection. Elles se comptent en **postes** (D = jour, N = nuit), granularité de la grille
Dywidag ; leurs durées sont des paramètres, pas des constantes du chantier — le modèle ne les
porte pas et le solveur ne les connaît pas. Les valeurs par défaut sont des repères à remplacer
par celles de Dywidag ; tout le reste — les dates, l'ordre, la ligne, le bassin — vient du
solveur et n'est pas à discuter ici.

La ligne SPE reste hors planning : le solveur ne date pas la coulée d'un élément spécial, il
n'en suit que les passages d'aire — y lire un départ de post-tension reviendrait à en inventer
un.

Sortie : un Gantt classique, une ligne par élément, dates de début/fin par opération, numéro
d'élément en clair — pas la grille postes-par-jour du modèle Dywidag.
"""
import argparse
import json
from datetime import date, timedelta

from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
from openpyxl.chart.shapes import GraphicalProperties
from openpyxl.drawing.line import LineProperties
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

LIGNE_NOM = {1: 'PL-1', 2: 'PL-2', 3: 'PL-3', 4: 'PL-4', 5: 'PL-5'}
OPERATIONS = ['Threading', 'Stressing', 'Grouting']
COULEUR = {'Threading': 'FFC7CE', 'Stressing': 'FFEB9C', 'Grouting': 'C6EFCE'}
BORD = Border(*[Side(style='thin', color='FFB0B0B0')] * 4)


def planifier(elements, durees, retard_j=2):
    """Pour chaque élément d'une ligne PL : ses trois opérations, en postes absolus.

    Renvoie une liste de {ligne, id, op, jour, poste0, nb} — `jour` est la date (calendaire) où
    démarre le poste 0 de l'opération, `poste0` son décalage en postes (demi-journées) au sein
    de ce jour-là, `nb` sa durée en postes. Un poste = une demi-journée ; le jour J occupe les
    postes 2J et 2J+1.
    """
    # Seules les lignes PL sont retenues. La ligne SPE n'a pas de date de coulée dans le
    # solveur (il ne suit que ses passages d'aire) : lui inventer un départ de post-tension
    # serait une donnée fabriquée, elle reste donc absente de cette sortie.
    par_ligne = {}
    for e in elements:
        if e['ligne'] <= 5 and e['beton'][0]:
            par_ligne.setdefault(e['ligne'], []).append(e)
    for lst in par_ligne.values():
        lst.sort(key=lambda e: e['beton'][0])

    barres, sans_suivant = [], []
    for ligne, lst in par_ligne.items():
        for i, e in enumerate(lst):
            suivant = lst[i + 1] if i + 1 < len(lst) else None
            if suivant:
                depart = date.fromisoformat(suivant['beton'][0])
            else:
                depart = date.fromisoformat(e['beton'][1] or e['beton'][0])
                sans_suivant.append(e['id'])
            depart += timedelta(days=retard_j)
            poste = 0
            for op in OPERATIONS:
                barres.append({'ligne': ligne, 'id': e['id'], 'op': op,
                               'jour': depart, 'poste0': poste, 'nb': durees[op]})
                poste += durees[op]
    return barres, sans_suivant


def par_element(barres):
    """Regroupe les barres par élément : {ligne, id, Threading: (début, fin), ...}, triés par
    ligne puis par début de post-tension. Début/fin sont des dates calendaires (jour du poste
    concerné) — l'unité d'affichage d'un Gantt classique, pas le poste lui-même."""
    par_id = {}
    for b in barres:
        d = par_id.setdefault(b['id'], {'ligne': b['ligne'], 'id': b['id']})
        debut = b['jour'] + timedelta(days=b['poste0'] // 2)
        fin = b['jour'] + timedelta(days=(b['poste0'] + b['nb'] - 1) // 2)
        d[b['op']] = (debut, fin)
    lignes = sorted(par_id.values(), key=lambda d: (d['ligne'], d['Threading'][0]))
    return lignes


def ecrire(elements_g, dst, meta, durees):
    wb = Workbook()
    ws = wb.active
    ws.title = 'Post tensioning'
    gras = Font(bold=True, size=9)
    petit = Font(size=8)
    centre = Alignment(horizontal='center')

    ws['A1'] = 'Post tensioning — Gantt calé sur les coulées du solveur'
    ws['A1'].font = Font(bold=True, size=12)
    ws['A2'] = (f"Départ : {meta['retard']} jours après le démarrage de la coulée de l'élément "
                f"suivant sur la même ligne (règle Dywidag, cellule E31). "
                f"Durées en postes — Threading {durees['Threading']}, Stressing "
                f"{durees['Stressing']}, Grouting {durees['Grouting']} : paramètres à confirmer.")
    ws['A2'].font = petit
    ws['A3'] = (f"Scénario : {meta['classeur']}, date de référence {meta['dateRef']}, "
                f"{meta['kpi']}. Ligne SPE hors tableau : pas de date de coulée solveur.")
    ws['A3'].font = petit

    entete = 5
    colonnes = ['Ligne', 'Élément', 'Threading début', 'Threading fin',
                'Stressing début', 'Stressing fin', 'Grouting début', 'Grouting fin']
    for c, nom in enumerate(colonnes, start=1):
        cell = ws.cell(entete, c, nom)
        cell.font = gras
        cell.alignment = centre
        cell.border = BORD

    origine = min(d['Threading'][0] for d in elements_g)
    r = entete + 1
    for d in elements_g:
        ws.cell(r, 1, LIGNE_NOM[d['ligne']]).font = petit
        ws.cell(r, 2, d['id']).font = Font(size=8, bold=True)
        col = 3
        for op in OPERATIONS:
            debut, fin = d[op]
            ws.cell(r, col, debut).number_format = 'dd/mm/yyyy'
            ws.cell(r, col + 1, fin).number_format = 'dd/mm/yyyy'
            for k in (0, 1):
                c = ws.cell(r, col + k)
                c.font = petit
                c.border = BORD
                c.fill = PatternFill('solid', fgColor=COULEUR[op])
            col += 2
        r += 1
    fin_tableau = r - 1

    for c, larg in enumerate([8, 11, 12, 12, 12, 12, 12, 12], start=1):
        ws.column_dimensions[get_column_letter(c)].width = larg
    ws.freeze_panes = 'A6'

    # Colonnes de calcul (masquées) pour le Gantt : décalage depuis l'origine et durée de
    # chaque opération, en jours — le format « barre empilée » d'Excel dessine le Gantt à
    # partir de ces nombres, la première série (le décalage) restant invisible.
    base_calc = 12
    ws.cell(entete, base_calc, 'Repère').font = gras
    ws.cell(entete, base_calc + 1, 'Décalage (j)').font = gras
    for k, op in enumerate(OPERATIONS):
        ws.cell(entete, base_calc + 2 + k, f'{op} (j)').font = gras
    r = entete + 1
    for d in elements_g:
        ws.cell(r, base_calc, f"{LIGNE_NOM[d['ligne']]} · {d['id']}")
        ws.cell(r, base_calc + 1, (d['Threading'][0] - origine).days)
        for k, op in enumerate(OPERATIONS):
            debut, fin = d[op]
            ws.cell(r, base_calc + 2 + k, (fin - debut).days + 1)
        r += 1
    for c in range(base_calc, base_calc + 2 + len(OPERATIONS)):
        ws.column_dimensions[get_column_letter(c)].hidden = True

    chart = BarChart()
    chart.type = 'bar'          # barres horizontales : axe des catégories = éléments
    chart.grouping = 'stacked'
    chart.overlap = 100
    chart.title = 'Post-tension — Gantt (une barre par élément)'
    chart.y_axis.title = None
    chart.x_axis.title = 'Jours depuis le début du programme de post-tension'
    chart.x_axis.number_format = '0'
    chart.height = max(10, 0.5 * len(elements_g))
    chart.width = 32

    cats = Reference(ws, min_col=base_calc, min_row=entete + 1, max_row=fin_tableau)
    offset = Reference(ws, min_col=base_calc + 1, min_row=entete, max_row=fin_tableau)
    chart.add_data(offset, titles_from_data=True)
    for k, op in enumerate(OPERATIONS):
        ref = Reference(ws, min_col=base_calc + 2 + k, min_row=entete, max_row=fin_tableau)
        chart.add_data(ref, titles_from_data=True)
    chart.set_categories(cats)

    # Première série (décalage) invisible : c'est elle qui pousse le début de chaque barre au
    # bon jour sans être dessinée, l'artifice classique du Gantt en barres empilées Excel.
    chart.series[0].graphicalProperties = GraphicalProperties(
        noFill=True, ln=LineProperties(noFill=True))
    for k, op in enumerate(OPERATIONS):
        chart.series[k + 1].graphicalProperties = GraphicalProperties(solidFill=COULEUR[op])

    ancre = f'K{entete + len(elements_g) + 4}'
    ws.add_chart(chart, ancre)

    wb.save(dst)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('plan', help='JSON produit par planning_runner.js')
    ap.add_argument('out')
    ap.add_argument('--threading', type=int, default=6, help='durée en postes (défaut 6)')
    ap.add_argument('--stressing', type=int, default=4, help='durée en postes (défaut 4)')
    ap.add_argument('--grouting', type=int, default=2, help='durée en postes (défaut 2)')
    ap.add_argument('--retard', type=int, default=2,
                    help='jours entre la coulée du suivant et le début de post-tension (défaut 2)')
    args = ap.parse_args()

    D = json.load(open(args.plan))
    durees = {'Threading': args.threading, 'Stressing': args.stressing, 'Grouting': args.grouting}
    barres, sans_suivant = planifier(D['elements'], durees, args.retard)
    if not barres:
        raise SystemExit('Aucun élément avec une date de coulée : rien à planifier.')

    elements_g = par_element(barres)
    k = D['kpi']
    meta = {'classeur': D['classeur'], 'dateRef': D['dateRef'], 'retard': args.retard,
            'kpi': f"{k['retards']} élément(s) en retard, {k['bloques']} bloqué(s), "
                   f"fin de production {k['finProduction']}"}
    ecrire(elements_g, args.out, meta, durees)

    debut = min(d['Threading'][0] for d in elements_g)
    fin = max(d['Grouting'][1] for d in elements_g)
    print(f"{args.out} écrit — {len(elements_g)} élément(s) post-tendus, Gantt du "
          f"{debut:%d/%m/%Y} au {fin:%d/%m/%Y}.")
    spe = [e['id'] for e in D['elements'] if e['ligne'] == 6]
    if spe:
        print(f"   ligne SPE laissée hors tableau ({len(spe)} éléments) : le solveur ne date pas "
              f"la coulée d'un élément spécial, il n'en suit que les passages d'aire.")
    if sans_suivant:
        print(f"   {len(sans_suivant)} dernier(s) élément(s) de ligne sans suivant — départ pris "
              f"sur leur propre fin de coulée : {', '.join(sans_suivant)}")


if __name__ == '__main__':
    main()
