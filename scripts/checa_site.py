#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""QA do site gerado: links internos, imagens, H1, JSON-LD, metas e IDs repetidos.

Uso: python scripts/checa_site.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

RAIZ = Path(__file__).resolve().parent.parent
PAGINAS = sorted([RAIZ / "index.html", RAIZ / "404.html",
                  *RAIZ.glob("categoria/*.html"), *RAIZ.glob("a/*.html"),
                  *(RAIZ / nome for nome in ("sobre.html", "como-verificamos.html", "contato.html"))])

RE_ATTR = re.compile(r'(?:href|src)="([^"]+)"')
RE_ID = re.compile(r'\bid="([^"]+)"')
RE_H1 = re.compile(r"<h1[ >]", re.I)
RE_LD = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)
RE_TITLE = re.compile(r"<title>(.*?)</title>", re.S)
RE_DESC = re.compile(r'<meta name="description" content="([^"]*)"')
RE_CANON = re.compile(r'<link rel="canonical" href="([^"]+)"')


def main() -> int:
    erros: list[str] = []
    avisos: list[str] = []
    total_links = 0

    for pagina in PAGINAS:
        if not pagina.exists():
            erros.append(f"página ausente: {pagina.relative_to(RAIZ)}")
            continue
        html = pagina.read_text(encoding="utf-8")
        rel = pagina.relative_to(RAIZ).as_posix()

        # H1 e metas
        if not RE_H1.search(html):
            erros.append(f"{rel}: sem <h1>")
        titulo = (RE_TITLE.search(html) or [None, ""])[1].strip()
        descricao = (RE_DESC.search(html) or [None, ""])[1].strip()
        canonical = (RE_CANON.search(html) or [None, ""])[1].strip()
        if not titulo:
            erros.append(f"{rel}: sem <title>")
        elif len(titulo) > 75:
            avisos.append(f"{rel}: title com {len(titulo)} caracteres")
        if not descricao:
            erros.append(f"{rel}: sem meta description")
        elif not (60 <= len(descricao) <= 165):
            avisos.append(f"{rel}: description com {len(descricao)} caracteres")
        if not canonical.startswith("https://baixa.pennertech.com.br/"):
            erros.append(f"{rel}: canonical inesperado -> {canonical}")

        # IDs repetidos
        ids = RE_ID.findall(html)
        repetidos = {i for i in ids if ids.count(i) > 1}
        if repetidos:
            erros.append(f"{rel}: id repetido -> {', '.join(sorted(repetidos))}")

        # links/recursos internos
        for alvo in RE_ATTR.findall(html):
            if alvo.startswith(("http://", "https://", "mailto:", "tel:", "#", "data:")):
                continue
            caminho = alvo.split("#")[0].split("?")[0]
            if not caminho:
                continue
            total_links += 1
            destino = (pagina.parent / caminho).resolve()
            if not destino.exists():
                erros.append(f"{rel}: alvo interno não existe -> {alvo}")

        # JSON-LD
        for bloco in RE_LD.findall(html):
            try:
                json.loads(bloco)
            except json.JSONDecodeError as exc:
                erros.append(f"{rel}: JSON-LD inválido ({exc})")

    # sitemap
    sitemap = (RAIZ / "sitemap.xml").read_text(encoding="utf-8")
    locs = re.findall(r"<loc>([^<]+)</loc>", sitemap)
    for url in locs:
        caminho = urlparse(url).path.lstrip("/")
        if not (RAIZ / caminho).exists():
            erros.append(f"sitemap: arquivo não existe -> {url}")
    paginas_indexaveis = [p for p in PAGINAS if p.name != "404.html"]
    if len(locs) < len(paginas_indexaveis):
        avisos.append(f"sitemap com {len(locs)} URLs para {len(paginas_indexaveis)} páginas")

    print(f"{len(PAGINAS)} páginas, {total_links} links internos, {len(locs)} URLs no sitemap")
    for a in avisos:
        print("  aviso:", a)
    if erros:
        print(f"\n{len(erros)} erro(s):")
        for e in erros:
            print("  -", e)
        return 1
    print("QA ok: sem erros")
    return 0


if __name__ == "__main__":
    sys.exit(main())
