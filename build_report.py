#!/usr/bin/env python3
"""Assemble la page de restitution autonome à partir de index.html.

La page produite embarque le moteur de solveur extrait de `index.html` et une copie
locale de SheetJS, de sorte qu'elle fonctionne sans aucune ressource externe : on y
recharge un classeur et le calcul est relancé sur place.

Le solveur n'est jamais recopié à la main — il est prélevé entre les marqueurs
SOLVEUR-CORE-DEBUT / SOLVEUR-CORE-FIN de `index.html`, qui reste la seule source.

    python3 build_report.py [--xlsx chemin/vers/xlsx.full.min.js] [-o sortie.html]
"""

import argparse
import base64
import pathlib
import re
import sys
import urllib.request

RACINE = pathlib.Path(__file__).parent
CDN_XLSX = "https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.mini.min.js"


def extraire_noyau(source: str) -> str:
    m = re.search(
        r"/\* ==== SOLVEUR-CORE-DEBUT ====.*?/\* ==== SOLVEUR-CORE-FIN ==== \*/",
        source,
        re.S,
    )
    if not m:
        sys.exit("Marqueurs SOLVEUR-CORE introuvables dans index.html.")
    return m.group(0)


def echapper_controles(js: str) -> str:
    r"""Échappe les caractères de contrôle bruts du bundle SheetJS.

    On inline le build « mini », suffisant pour lire du .xlsx/.xlsm : le build « full »
    embarque les tables de pages de code héritées, truffées de U+FFFD, que la publication
    de la page rejette comme du contenu corrompu.

    Le bundle minifié contient des octets de contrôle littéraux dans ses tables de
    pages de code. Tels quels ils font échouer la publication de la page ; sous forme
    d'échappements \xNN à l'intérieur des littéraux de chaîne, le code est équivalent.
    """
    garder = {"\n", "\r", "\t"}
    return "".join(
        c if (ord(c) >= 0x20 or c in garder) else f"\\x{ord(c):02x}" for c in js
    )


def charger_xlsx(chemin: str | None) -> str:
    if chemin:
        p = pathlib.Path(chemin)
        if not p.is_file():
            sys.exit(f"Bibliothèque SheetJS introuvable : {p}")
        return p.read_text(encoding="utf-8")
    for candidat in [
        RACINE / "vendor" / "xlsx.mini.min.js",
        RACINE / "node_modules" / "xlsx" / "dist" / "xlsx.mini.min.js",
    ]:
        if candidat.is_file():
            return candidat.read_text(encoding="utf-8")
    print(f"Téléchargement de SheetJS depuis {CDN_XLSX}…", file=sys.stderr)
    with urllib.request.urlopen(CDN_XLSX, timeout=60) as r:
        return r.read().decode("utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--xlsx", help="chemin vers xlsx.full.min.js à inliner")
    ap.add_argument("-o", "--out", default="rapport.html", help="fichier de sortie")
    ap.add_argument(
        "--gabarit", default="report_template.html", help="gabarit de la page"
    )
    ap.add_argument(
        "--plan",
        default="vendor_plan.png",
        help="image de fond du plan, cadrée sur x 4→64 %% / y 42→84 %% du plan général",
    )
    args = ap.parse_args()

    index = (RACINE / "index.html").read_text(encoding="utf-8")
    gabarit = (RACINE / args.gabarit).read_text(encoding="utf-8")

    noyau = extraire_noyau(index)
    xlsx = echapper_controles(charger_xlsx(args.xlsx))

    plan = "null"
    chemin_plan = RACINE / args.plan
    if chemin_plan.is_file():
        b64 = base64.b64encode(chemin_plan.read_bytes()).decode("ascii")
        mime = "image/png" if chemin_plan.suffix.lower() == ".png" else "image/jpeg"
        plan = (
            '{href: "data:%s;base64,%s", x: 4, y: 42, w: 60, h: 42}' % (mime, b64)
        )
    else:
        print(f"Pas de fond de plan ({chemin_plan}) — schéma seul.", file=sys.stderr)

    for jeton in ("/*__XLSX__*/", "/*__SOLVEUR__*/"):
        if jeton not in gabarit:
            sys.exit(f"Jeton {jeton} absent du gabarit {args.gabarit}.")

    page = (
        gabarit.replace("/*__XLSX__*/", xlsx)
        .replace("/*__SOLVEUR__*/", noyau)
        .replace("/*__PLAN__*/ null", plan)
    )

    sortie = RACINE / args.out
    sortie.write_text(page, encoding="utf-8")
    print(
        f"{sortie} écrit — {len(page) / 1024:.0f} Ko "
        f"(solveur {len(noyau) / 1024:.0f} Ko, SheetJS {len(xlsx) / 1024:.0f} Ko, "
        f"plan {len(plan) / 1024:.0f} Ko)"
    )


if __name__ == "__main__":
    main()
