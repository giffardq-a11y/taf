"""Lit les deux classeurs TEMPO (ferraillage/logistique jusqu'au casting pit) et les
transforme en tables plates, exploitables par un futur simulateur.

    python3 lire_tempo.py General_Tempo_Staggering.xlsx STE__TEMPO__N3_Takt_Plan__V0_1.xlsx

Deux classeurs, deux niveaux de détail, un seul référentiel de codes :

  - Le classeur « N3 » (`STE_TEMPO_N3_...`) porte la feuille `Data` — le référentiel de
    tous les codes utilisés partout ailleurs (zones, équipes, ressources/sous-traitants,
    segments, étapes) — et 29 feuilles de tâches, une par zone, nommées
    `PeP__<zone>` / `CP__<zone>` / `PoP__<zone>`. Chaque feuille liste, tâche par tâche,
    l'effectif requis sur des fenêtres horaires de la journée (5 fenêtres de ~5h en zone
    CP — dont une « OT », hors tempo, qui sert de tampon —, 4 fenêtres de 6h en zone PoP).
  - Le classeur « N1 » (`General_Tempo_Staggering`) porte le calage haut niveau : pour
    chaque ligne (L1 à L5) et chaque catégorie (Walls, BS, LASCA, Buffer, CP), le nombre
    de postes (shifts) par segment béton S1 à S9, plus la position de démarrage de la
    ligne dans le calendrier absolu des « tempos ».

Le lien entre les deux : Ws (somme S1..S9 d'une catégorie, niveau N1) est censé retomber,
une fois les tâches N3 de cette catégorie sommées sur la même fenêtre, sur le même total —
c'est un repère de cohérence à vérifier, pas une garantie ; les deux classeurs sont
alimentés séparément et peuvent diverger tant qu'ils n'ont pas été rapprochés.

N'invente aucune règle : ce module ne fait que lire et mettre à plat. L'interprétation
métier (quelle ressource est la plus rare, quel tampon est vraiment intouchable...) reste
à faire ailleurs, sur la base de ces tables.
"""
import argparse
import re
import sys
import unicodedata
import warnings

from openpyxl import load_workbook

warnings.filterwarnings('ignore', module='openpyxl')


def _normalise(v):
    """Le tableur mélange des caractères visuellement identiques mais distincts en
    Unicode — la colonne « Ω » y est écrite avec le signe Ohm (U+2126), pas la lettre
    grecque Omega (U+03A9). Sans cette normalisation, la colonne de fin de grille horaire
    n'est jamais reconnue et la comparaison déborde sur les colonnes de métadonnées."""
    return unicodedata.normalize('NFKC', v) if isinstance(v, str) else v

_DUREE_RE = re.compile(r'(?:(\d+(?:[.,]\d+)?)\s*h)?\s*(?:(\d+)\s*min)?')


def _duree_minutes(texte):
    """« 1h10 min », « 30 min », « 1-3h » -> minutes. Une plage (« 1-3h ») renvoie sa
    borne haute — le pire cas, pas une moyenne inventée — avec le texte d'origine
    conservé à côté pour qui veut la borne basse."""
    if not texte:
        return None
    texte = texte.strip()
    if '-' in texte and 'h' in texte:
        borne_haute = texte.split('-')[-1]
        return _duree_minutes(borne_haute)
    m = _DUREE_RE.fullmatch(texte)
    if not m or not any(m.groups()):
        return None
    h = float(m.group(1).replace(',', '.')) if m.group(1) else 0
    mn = int(m.group(2)) if m.group(2) else 0
    return round(h * 60 + mn)


def lire_sequence_pptx_tableaux(chemin_pptx, index_diapo):
    """Extrait les tableaux « tâche | durée | effectif » d'une diapositive PowerPoint —
    le niveau le plus fin rencontré à ce jour (ex. le détail du skidding, minute par
    minute). Un tableau par bloc (repéré par son titre, cellule 1×1 de la première ligne :
    « Skidding to Lasca », « Skidding to Buffer »...).

    `index_diapo` est le numéro de diapositive, 1-indexé comme dans PowerPoint.
    """
    from pptx import Presentation
    p = Presentation(chemin_pptx)
    slide = list(p.slides)[index_diapo - 1]
    out = []
    for shape in slide.shapes:
        if not shape.has_table:
            continue
        tbl = shape.table
        titre = tbl.rows[0].cells[0].text.strip()
        for row in list(tbl.rows)[1:]:
            cells = [c.text.strip() for c in row.cells]
            if not cells[0] or cells[0].startswith(titre.split(' ')[0]):
                continue
            tache, duree, effectif = (cells + ['', '', ''])[:3]
            if not tache:
                continue
            out.append({
                'sequence': titre, 'tache': tache, 'duree_texte': duree,
                'duree_min': _duree_minutes(duree),
                'effectif': int(effectif) if effectif.strip().isdigit() else effectif or None,
            })
    return out

# --- Colonnes fixes en tête de chaque feuille de tâches N3, avant la grille horaire ---
COLONNES_TACHE = ['zone', 'unite', 'element', 'segment', 'etape', 'tube', 'base_ou_special',
                   'equipe', 'tache']
# Repérées par leur libellé d'en-tête plutôt que par un numéro de colonne fixe : la largeur
# de la grille horaire varie d'une feuille à l'autre, ces colonnes de fin ne le font pas.
COLONNES_METADATA = {
    'Ω': 'omega', 'Type of Ressources': 'ressource', 'Sub - Team': 'sous_equipe',
    'Sub-Team': 'sous_equipe', 'Sub-Tems': 'sous_equipe', 'Total hours': 'heures_total',
    'Crane hours': 'heures_grue', 'Machine hour': 'heures_grue',
    'Crane Usage': 'taux_grue', 'Machine usage': 'taux_grue',
    'COMMENTS': 'commentaire', 'Comment': 'commentaire', 'Future?': 'futur',
}


def _erreur_excel(v):
    """Une formule en erreur (#DIV/0! etc.) revient comme une chaîne : on la neutralise
    plutôt que de la faire passer pour une donnée."""
    return None if isinstance(v, str) and v.startswith('#') else v


def _plage_fenetre(libelle):
    """« 21\\n1:45 » -> (21.0, 1.75) : la borne de fin peut être plus petite que celle de
    début, la fenêtre traversant minuit — l'appelant en tient compte, ce n'est pas une
    erreur de saisie."""
    if not libelle or '\n' not in str(libelle):
        return None
    a, b = str(libelle).split('\n', 1)
    def h(s):
        s = s.strip()
        if ':' in s:
            hh, mm = s.split(':')
            return int(hh) + int(mm) / 60
        return float(s)
    try:
        return h(a), h(b)
    except ValueError:
        return None


def lire_reference(chemin_n3, feuille='Data'):
    """Renvoie le référentiel de codes de la feuille `Data` : un dict par colonne
    (zone, equipe, ressource, ...), chacun une liste de (code, libellé) sans les trous."""
    wb = load_workbook(chemin_n3, data_only=True)
    ws = wb[feuille]
    entetes = [ws.cell(1, c).value for c in range(1, ws.max_column + 1)]
    out = {h: [] for h in entetes if h}
    for r in range(2, ws.max_row + 1):
        for c, h in enumerate(entetes, start=1):
            if not h:
                continue
            v = ws.cell(r, c).value
            if v not in (None, ''):
                out[h].append(v)
    return out


def _feuilles_taches(wb):
    return [n for n in wb.sheetnames if re.match(r'^(PeP|CP|PoP)__', n)]


def lire_taches_n3(chemin_n3):
    """Met à plat les 29 feuilles de tâches. Renvoie (taches, charges) :

    - `taches` : une entrée par ligne de tâche, avec ses colonnes fixes et ses métadonnées
      (Ω, ressource, sous-équipe, heures, grue, commentaire) — une tâche peut n'avoir aucune
      charge horaire chiffrée (un jalon, marqué 'x' dans la grille) sans que la ligne
      elle-même n'y perde son sens.
    - `charges` : une entrée par (tâche, fenêtre horaire non vide) avec l'effectif requis —
      c'est la table qu'un simulateur consomme pas à pas.

    `tempo` (l'index absolu du « jour tempo », T1, T2...) est lu ligne 2 de chaque feuille
    et reporté par propagation vers la droite ; `tampon` indique si la fenêtre est marquée
    « OT » (hors tempo, cf. la réunion du 10/08 : la fenêtre 2h-6h n'est utilisée qu'en
    tampon, pas par défaut).
    """
    wb = load_workbook(chemin_n3, data_only=True)
    taches, charges = [], []
    for nom_feuille in _feuilles_taches(wb):
        ws = wb[nom_feuille]
        ligne_entete = 4
        entetes = [_normalise(ws.cell(ligne_entete, c).value) for c in range(1, ws.max_column + 1)]
        # Colonnes de métadonnées : celles qui suivent la grille horaire, repérées par leur
        # libellé exact (voir COLONNES_METADATA), en s'arrêtant à la première rencontrée.
        col_meta_debut = next((c for c, h in enumerate(entetes, start=1) if h in COLONNES_METADATA), None)
        col_fenetres = list(range(len(COLONNES_TACHE) + 1, (col_meta_debut or ws.max_column + 1)))

        # Ligne 2 : index tempo absolu (T1, T2...), posé sur la première colonne de chaque
        # bloc de jour et à propager vers la droite jusqu'au prochain repère.
        tempo_par_col = {}
        dernier_tempo = None
        for c in col_fenetres:
            v = ws.cell(2, c).value
            if v:
                m = re.match(r'T(\d+)', str(v))
                dernier_tempo = int(m.group(1)) if m else v
            tempo_par_col[c] = dernier_tempo

        # Ligne 3 : « OT » marque une fenêtre tampon, propagée comme le tempo mais retenue
        # seulement quand elle vaut explicitement OT (les autres blocs ne se marquent pas,
        # ce n'est pas une absence de donnée mais une fenêtre « normale »).
        tampon_par_col = {}
        for c in col_fenetres:
            v = ws.cell(3, c).value
            tampon_par_col[c] = (str(v).strip() == 'OT') if v else False

        fenetre_par_col = {c: _plage_fenetre(ws.cell(ligne_entete, c).value) for c in col_fenetres}

        for r in range(ligne_entete + 1, ws.max_row + 1):
            zone = ws.cell(r, 1).value
            if zone in (None, ''):
                continue
            desc = [ws.cell(r, c).value for c in range(1, len(COLONNES_TACHE) + 1)]
            tache = dict(zip(COLONNES_TACHE, desc))
            tache['feuille'] = nom_feuille
            tache['ligne_excel'] = r
            for c in range(col_meta_debut or 0, ws.max_column + 1):
                h = entetes[c - 1]
                cle = COLONNES_METADATA.get(h)
                if cle:
                    tache[cle] = _erreur_excel(ws.cell(r, c).value)
            taches.append(tache)

            for c in col_fenetres:
                v = _erreur_excel(ws.cell(r, c).value)
                if v is None:
                    continue
                jalon = isinstance(v, str)
                charges.append({
                    'feuille': nom_feuille, 'ligne_excel': r, 'zone': zone,
                    'tempo': tempo_par_col[c], 'tampon': tampon_par_col[c],
                    'fenetre': fenetre_par_col[c], 'jalon': jalon,
                    'effectif': None if jalon else v,
                })
    return taches, charges


def lire_n1(chemin_n1, feuille):
    """Lit le calage haut niveau (postes par segment et par catégorie, pour chaque ligne)
    d'une feuille du classeur N1. Le nom exact de la feuille se choisit à l'appel — le
    classeur porte plusieurs versions (V0 à V4) en plus de la retenue ; ce module ne
    devine pas laquelle fait foi.

    Renvoie une liste de {ligne, demarrage, categorie, segments (S1..S9), postes_semaine,
    postes_hors_semaine, postes_total, jours_total}. `demarrage` est l'entrée telle que
    trouvée dans le classeur (ex. « L4 - T25 ») — pas encore interprétée.
    """
    wb = load_workbook(chemin_n1, data_only=True)
    ws = wb[feuille]
    out = []
    r = 1
    while r <= ws.max_row:
        # L'intitulé « Line N [- Option ...] » se trouve en colonne R (18), pas en tête
        # de ligne : la feuille est construite comme un schéma annoté, pas un tableau.
        v = ws.cell(r, 18).value
        if isinstance(v, str) and v.strip().lower().startswith('line'):
            demarrage = ws.cell(r + 3, 19).value  # ex. "L4 - T25"
            # Cinq catégories connues, chacune sur une ligne, séparées d'une ligne vide :
            # Walls, BS, LASCA, Buffer, CP dans cet ordre depuis l'en-tête S1..S9.
            r_cat = r + 5
            while True:
                nom_cat = ws.cell(r_cat, 18).value
                if not nom_cat:
                    break
                # Au-delà des 5 catégories chiffrées (Walls, BS, LASCA, Buffer, CP), la
                # même colonne porte des repères sans données (PP, BP + FU & SG,
                # CRO - MPL, CAS - Prep) — de simples annotations du schéma, pas des
                # catégories à compter.
                if ws.cell(r_cat, 15).value is None:
                    r_cat += 2
                    continue
                segs = [ws.cell(r_cat, c).value for c in range(1, 10)]
                out.append({
                    'ligne': v.strip(), 'demarrage': demarrage, 'categorie': nom_cat,
                    'segments': segs,
                    'skidding': ws.cell(r_cat, 10).value, 'basique': ws.cell(r_cat, 11).value,
                    'special': ws.cell(r_cat, 12).value,
                    'postes_semaine': ws.cell(r_cat, 13).value,
                    'postes_hors_semaine': ws.cell(r_cat, 14).value,
                    'postes_total': ws.cell(r_cat, 15).value,
                    'jours_total': ws.cell(r_cat, 16).value,
                    'verif': ws.cell(r_cat, 17).value,
                })
                r_cat += 2
            r = r_cat
        else:
            r += 1
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('n1', help='General_Tempo_Staggering.xlsx')
    ap.add_argument('n3', help='STE__TEMPO__N3_Takt_Plan__V0_1.xlsx')
    ap.add_argument('--feuille-n1', default=None,
                     help="feuille N1 à lire (défaut : la dernière feuille '... 5 Lines - V*' du classeur)")
    args = ap.parse_args()

    ref = lire_reference(args.n3)
    print(f"Référentiel : {', '.join(f'{k} ({len(v)})' for k, v in ref.items())}")

    taches, charges = lire_taches_n3(args.n3)
    print(f"\nTâches N3 : {len(taches)} lignes de tâches sur {len({t['feuille'] for t in taches})} feuilles, "
          f"{len(charges)} cases d'effectif renseignées.")
    jalons = sum(1 for c in charges if c['jalon'])
    print(f"  dont {jalons} jalons (marqueur 'x', sans effectif) et {len(charges) - jalons} charges chiffrées.")
    zones = sorted({t['zone'] for t in taches})
    print(f"  zones couvertes : {', '.join(zones)}")

    wb1 = load_workbook(args.n1, data_only=True)
    feuille_n1 = args.feuille_n1 or sorted(
        [n for n in wb1.sheetnames if '5 Lines' in n])[-1]
    n1 = lire_n1(args.n1, feuille_n1)
    print(f"\nN1 ('{feuille_n1}') : {len(n1)} entrées ligne×catégorie.")
    for e in n1:
        print(f"  {e['ligne']:22s} {e['categorie']:8s} postes/segment={e['segments']} "
              f"total={e['postes_total']} vérif={e['verif']}")


if __name__ == '__main__':
    main()
