"""
Configuration for PG Essay Chinese Mirror.
"""

from pathlib import Path

# --- Paths ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
ESSAYS_DIR = DATA_DIR / "essays"
TEMPLATES_DIR = PROJECT_ROOT / "templates"
DOCS_DIR = PROJECT_ROOT / "docs"

# --- Site ---
SITE_TITLE = "保罗·格雷厄姆文集"
SITE_SUBTITLE = "Paul Graham Essays in Chinese"
SITE_DISCLAIMER = "本站为 paulgraham.com 的中文翻译镜像，仅供学习交流。原文版权归 Paul Graham 所有。"
FONT_STACK = "'Microsoft YaHei', 'PingFang SC', 'Noto Sans SC', 'Hiragino Sans GB', Verdana, sans-serif"
