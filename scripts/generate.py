#!/usr/bin/env python3
"""
Generate static HTML site from translated essay JSON files.

Usage:
    python scripts/generate.py
"""

import json
import re
import sys
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import (
    DOCS_DIR,
    ESSAYS_DIR,
    FONT_STACK,
    SITE_DISCLAIMER,
    SITE_SUBTITLE,
    SITE_TITLE,
    TEMPLATES_DIR,
)

MONTH_ORDER = {
    "January": 1, "February": 2, "March": 3, "April": 4,
    "May": 5, "June": 6, "July": 7, "August": 8,
    "September": 9, "October": 10, "November": 11, "December": 12,
}


def parse_date_sort_key(date_str: str) -> tuple:
    if not date_str:
        return (0, 0, 0)
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", date_str)
    if m:
        return (int(m.group(1)), int(m.group(2)), int(m.group(3)))
    parts = date_str.strip().split()
    if len(parts) == 2:
        month = MONTH_ORDER.get(parts[0], 0)
        try:
            return (int(parts[1]), month, 0)
        except ValueError:
            pass
    return (0, 0, 0)


def load_essays() -> list[dict]:
    essays = []
    if not ESSAYS_DIR.exists():
        return essays
    for filepath in ESSAYS_DIR.glob("*.json"):
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)
        if data.get("translation_status") != "complete":
            continue
        if not data.get("paragraphs_zh"):
            continue
        essays.append(data)
    essays.sort(key=lambda e: parse_date_sort_key(e.get("date", "")), reverse=True)
    return essays


def generate():
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=False,
    )
    template_vars = {
        "site_title": SITE_TITLE,
        "site_subtitle": SITE_SUBTITLE,
        "site_disclaimer": SITE_DISCLAIMER,
        "font_stack": FONT_STACK,
    }
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    essays = load_essays()
    if not essays:
        print("No translated essays found.")
        return

    essay_template = env.get_template("essay.html")
    for essay in essays:
        html = essay_template.render(essay=essay, **template_vars)
        with open(DOCS_DIR / f"{essay['slug']}.html", "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  {essay['slug']}.html - {essay.get('title_zh', essay['title'])}")

    index_template = env.get_template("index.html")
    html = index_template.render(essays=essays, **template_vars)
    for name in ["index.html", "articles.html"]:
        with open(DOCS_DIR / name, "w", encoding="utf-8") as f:
            f.write(html)

    print(f"\n{len(essays)} essay pages + index generated in {DOCS_DIR}/")


if __name__ == "__main__":
    generate()
