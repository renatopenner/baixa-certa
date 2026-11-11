#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Baixa os ícones oficiais das marcas (Simple Icons) para img/apps/.

Lê o campo "icone" de cada app em dados/apps.json — é o slug do ícone no
Simple Icons (ex.: "libreoffice", "vlcmediaplayer"). Sem o campo (ou 404), o
site usa o monograma com as iniciais do app.

Uso: python scripts/icones.py
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DADOS = RAIZ / "dados" / "apps.json"
SAIDA = RAIZ / "img" / "apps"
CDN = "https://cdn.simpleicons.org/{slug}"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) BaixaCerta/1.0"


def baixa(slug: str, cor: str | None = None) -> bytes | None:
    url = CDN.format(slug=slug) + (f"/{cor}" if cor else "")
    r = subprocess.run(
        ["curl.exe", "-sSL", "--max-time", "30", "-A", UA, "-w", "\n%{http_code}", url],
        capture_output=True,
    )
    saida = r.stdout
    if not saida:
        return None
    corpo, _, status = saida.rpartition(b"\n")
    if status.strip() != b"200" or not corpo.strip().startswith(b"<svg"):
        return None
    return corpo


def cor_do_svg(svg: bytes) -> str:
    import re
    m = re.search(rb'fill="#([0-9a-fA-F]{6})"', svg)
    return m.group(1).decode() if m else "000000"


def luminancia(hexcor: str) -> float:
    r, g, b = (int(hexcor[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def main() -> int:
    apps = json.loads(DADOS.read_text(encoding="utf-8"))["apps"]
    SAIDA.mkdir(parents=True, exist_ok=True)
    baixados = falhas = 0
    for a in apps:
        slug_icone = a.get("icone")
        destino = SAIDA / f"{a['slug']}.svg"
        if not slug_icone:
            if destino.exists():
                destino.unlink()
            continue
        svg = baixa(slug_icone)
        if svg is None:
            print(f"  ! {a['slug']}: ícone '{slug_icone}' não encontrado no Simple Icons")
            falhas += 1
            continue
        # ícone quase branco fica invisível no fundo claro: refaz em tinta
        if luminancia(cor_do_svg(svg)) > 0.88:
            alt = baixa(slug_icone, "0a1a2b")
            if alt:
                svg = alt
        destino.write_bytes(svg)
        baixados += 1
    print(f"ícones: {baixados} baixados, {falhas} sem ícone (usarão monograma)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
