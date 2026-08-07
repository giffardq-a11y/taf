"""Planning de post-tension au format Dywidag, calé sur les coulées du solveur.

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

La mise en page reprend le modèle : un bloc par bassin, deux lignes par bassin, trois
opérations par ligne, une colonne par poste, et une page par tranche de 63 jours comme dans le
fichier d'origine.
"""
import argparse
import json
from datetime import date, timedelta

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

# Lignes du modèle : un bassin, ses deux lignes de production, dans l'ordre du fichier Dywidag.
BASSINS = [('Basin A', [(1, 'PL-1'), (2, 'PL-2')]),
           ('Basin B', [(3, 'PL-3'), (4, 'PL-4')]),
           ('Basin C', [(5, 'PL-5'), (6, 'SPE')])]
OPERATIONS = ['Threading', 'Stressing', 'Grouting']
COULEUR = {'Threading': 'FFC7CE', 'Stressing': 'FFEB9C', 'Grouting': 'C6EFCE'}
BORD = Border(*[Side(style='thin', color='FFB0B0B0')] * 4)
JOURS_PAR_PAGE = 63          # comme le modèle Dywidag
POSTES = ['D', 'N']


def planifier(elements, durees, retard_j=2):
    """Pour chaque élément : le poste de départ de sa post-tension, et ses trois opérations.

    Renvoie une liste de {ligne, id, op, debut, fin} en numéros de poste absolus, comptés
    depuis le premier jour du planning. Un poste = une demi-journée ; le jour J occupe les
    postes 2J et 2J+1.
    """
    # Seules les lignes PL sont retenues. Un élément spécial ne se coule pas par segments : le
    # solveur ne lui donne aucune date de coulée, il ne suit que ses passages d'aire. Y lire un
    # départ de post-tension reviendrait à en inventer un — la ligne SPE reste donc en place
    # dans la grille, mais vide, et le fait est signalé plutôt que masqué.
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


def ecrire(barres, dst, origine, nb_jours, durees, meta):
    wb = Workbook()
    ws = wb.active
    ws.title = 'Post tensioning'
    gras = Font(bold=True, size=9)
    petit = Font(size=8)

    ws['A1'] = 'Post tensioning — calé sur les coulées du solveur'
    ws['A1'].font = Font(bold=True, size=12)
    ws['A2'] = (f"Départ : {meta['retard']} jours après le démarrage de la coulée de l'élément "
                f"suivant sur la même ligne (règle Dywidag). "
                f"Durées en postes — Threading {durees['Threading']}, Stressing "
                f"{durees['Stressing']}, Grouting {durees['Grouting']} : paramètres à confirmer.")
    ws['A2'].font = petit
    ws['A3'] = (f"Scénario : {meta['classeur']}, date de référence {meta['dateRef']}, "
                f"{meta['kpi']}")
    ws['A3'].font = petit

    ligne_xl = 5
    pages = (nb_jours + JOURS_PAR_PAGE - 1) // JOURS_PAR_PAGE
    for page in range(pages):
        j0 = page * JOURS_PAR_PAGE
        j1 = min(j0 + JOURS_PAR_PAGE, nb_jours)
        d0 = origine + timedelta(days=j0)
        d1 = origine + timedelta(days=j1 - 1)
        ws.cell(ligne_xl, 1, f'{d0:%d/%m/%Y} → {d1:%d/%m/%Y}   ·   page {page + 1} / {pages}').font = gras
        ligne_xl += 1

        # En-têtes : numéro de jour sur deux colonnes, puis le poste D / N.
        tete = ligne_xl
        for j in range(j0, j1):
            col = 4 + (j - j0) * 2
            c = ws.cell(tete, col, j + 1)
            c.font = petit
            c.alignment = Alignment(horizontal='center')
            ws.merge_cells(start_row=tete, start_column=col, end_row=tete, end_column=col + 1)
            if (j + 1) % 7 == 0:                     # repère de fin de semaine, comme le modèle
                for k in (0, 1):
                    ws.cell(tete, col + k).fill = PatternFill('solid', fgColor='FFC7CE')
            for k, p in enumerate(POSTES):
                cp = ws.cell(tete + 1, col + k, p)
                cp.font = petit
                cp.alignment = Alignment(horizontal='center')
        ligne_xl += 2

        for nom_bassin, lignes in BASSINS:
            debut_bassin = ligne_xl
            for num, nom_ligne in lignes:
                for op in OPERATIONS:
                    ws.cell(ligne_xl, 2, nom_ligne if op == OPERATIONS[0] else '').font = petit
                    ws.cell(ligne_xl, 3, op).font = petit
                    for j in range(j0, j1):
                        for k in range(2):
                            ws.cell(ligne_xl, 4 + (j - j0) * 2 + k).border = BORD
                    # Les barres de cette ligne et de cette opération.
                    for b in barres:
                        if b['ligne'] != num or b['op'] != op:
                            continue
                        p0 = (b['jour'] - origine).days * 2 + b['poste0']
                        for p in range(p0, p0 + b['nb']):
                            j, k = divmod(p, 2)
                            if not (j0 <= j < j1):
                                continue
                            c = ws.cell(ligne_xl, 4 + (j - j0) * 2 + k)
                            c.fill = PatternFill('solid', fgColor=COULEUR[op])
                            c.border = BORD
                            if p == p0:
                                c.value = b['id'].replace('STE-', '').replace('SPE-', 'S')
                                c.font = Font(size=7)
                                c.alignment = Alignment(horizontal='left')
                    ligne_xl += 1
            ws.cell(debut_bassin, 1, nom_bassin).font = gras
            ws.merge_cells(start_row=debut_bassin, start_column=1,
                           end_row=ligne_xl - 1, end_column=1)
        ligne_xl += 2

    ws.column_dimensions['A'].width = 10
    ws.column_dimensions['B'].width = 8
    ws.column_dimensions['C'].width = 11
    for col in range(4, 4 + JOURS_PAR_PAGE * 2):
        ws.column_dimensions[get_column_letter(col)].width = 2.6
    ws.freeze_panes = 'D1'
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

    debuts = [b['jour'] for b in barres]
    origine = min(debuts)
    fin = max(b['jour'] + timedelta(days=(b['poste0'] + b['nb'] + 1) // 2) for b in barres)
    nb_jours = (fin - origine).days + 1
    k = D['kpi']
    meta = {'classeur': D['classeur'], 'dateRef': D['dateRef'], 'retard': args.retard,
            'kpi': f"{k['retards']} élément(s) en retard, {k['bloques']} bloqué(s), "
                   f"fin de production {k['finProduction']}"}
    ecrire(barres, args.out, origine, nb_jours, durees, meta)

    par_op = {op: sum(1 for b in barres if b['op'] == op) for op in OPERATIONS}
    print(f"{args.out} écrit — {len(barres) // 3} élément(s) post-tendus, "
          f"{nb_jours} jours du {origine:%d/%m/%Y} au {fin:%d/%m/%Y}.")
    print(f"   opérations : {par_op}")
    spe = [e['id'] for e in D['elements'] if e['ligne'] == 6]
    if spe:
        print(f"   ligne SPE laissée vide ({len(spe)} éléments) : le solveur ne date pas la "
              f"coulée d'un élément spécial, il n'en suit que les passages d'aire.")
    if sans_suivant:
        print(f"   {len(sans_suivant)} dernier(s) élément(s) de ligne sans suivant — départ pris "
              f"sur leur propre fin de coulée : {', '.join(sans_suivant)}")


if __name__ == '__main__':
    main()
