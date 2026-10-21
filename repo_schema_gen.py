#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 11:32:47 2026

@author: hakim
"""

from pathlib import Path

IGNORE = {".git", ".venv", "__pycache__", ".pytest_cache", "htmlcov", ".idea"}

def to_markdown(root: Path, prefix="", depth=0, max_depth=3):
    lines = []
    if depth > max_depth:
        return lines
    entries = sorted(
        [e for e in root.iterdir() if e.name not in IGNORE and not e.name.endswith(".pyc")],
        key=lambda e: (e.is_file(), e.name.lower()),
    )
    for entry in entries:
        lines.append(f"{prefix}- {entry.name}{'/' if entry.is_dir() else ''}")
        if entry.is_dir():
            lines.extend(to_markdown(entry, prefix + "  ", depth + 1, max_depth))
    return lines

md = "\n".join(to_markdown(Path(".")))
Path("SCHEMA.md").write_text(f"# Schéma du projet\n\n{md}\n", encoding="utf-8")
print("✅ SCHEMA.md généré")