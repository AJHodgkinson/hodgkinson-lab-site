#!/usr/bin/env python3
"""
Build script for the Hodgkinson Lab website.

Reads content from data/*.yml, renders it into templates/*.html
using Jinja2, and writes plain static HTML files into docs/
(the folder GitHub Pages serves from).

Usage:
    python3 build.py

Requires: Python 3.8+, jinja2, pyyaml
    pip install jinja2 pyyaml
"""
import datetime
import shutil
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = Path(__file__).parent
DATA_DIR = ROOT / "data"
TEMPLATES_DIR = ROOT / "templates"
ASSETS_DIR = ROOT / "assets"
OUTPUT_DIR = ROOT / "docs"

PAGES = [
    ("index.html", "index.html", None, None),
    ("research.html", "research.html", "Research", "Mitochondrial genomics and RNA processing research at the Hodgkinson Lab, King's College London."),
    ("people.html", "people.html", "People", "Meet the Hodgkinson Lab research group and alumni."),
    ("publications.html", "publications.html", "Publications", "Publications from the Hodgkinson Lab, King's College London."),
    ("positions.html", "positions.html", "Positions", "PhD and postdoc opportunities in the Hodgkinson Lab."),
    ("software.html", "software.html", "Software", "Open-source software from the Hodgkinson Lab: PAC, MitoNuclearCOEXPlorer, MitoRNACleave and ASE Detector."),
    ("contact.html", "contact.html", "Contact", "Contact the Hodgkinson Lab, Department of Medical & Molecular Genetics, King's College London."),
]


def load_yaml(name):
    path = DATA_DIR / name
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main():
    site = load_yaml("site.yml")
    people = load_yaml("people.yml")
    alumni = load_yaml("alumni.yml")
    publications = load_yaml("publications.yml")
    software = load_yaml("software.yml")

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=select_autoescape(["html"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True)

    context_base = {
        "site": site,
        "people": people,
        "alumni": alumni,
        "publications": publications,
        "software": software,
        "current_year": datetime.date.today().year,
    }

    for template_name, out_file, page_title, meta_description in PAGES:
        template = env.get_template(template_name)
        html = template.render(
            **context_base,
            page_file=out_file,
            page_title=page_title,
            meta_description=meta_description,
        )
        (OUTPUT_DIR / out_file).write_text(html, encoding="utf-8")
        print(f"  built {out_file}")

    # Copy static assets as-is
    shutil.copytree(ASSETS_DIR, OUTPUT_DIR / "assets")

    # CNAME file so GitHub Pages knows the custom domain
    (OUTPUT_DIR / "CNAME").write_text("www.hodgkinsonlab.org\n", encoding="utf-8")

    # .nojekyll tells GitHub Pages to serve the folder as-is (no Jekyll processing)
    (OUTPUT_DIR / ".nojekyll").write_text("", encoding="utf-8")

    print(f"\nDone. Static site written to {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
