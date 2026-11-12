#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Busca o ícone de cada app para img/apps/, em camadas:

1. `dados/icones.json` → overrides manuais ({"slug": {"logo": "URL"}} ou {"wiki": "Título"});
2. Simple Icons (campo `icone` de cada app) → SVG colorido;
3. imagem principal do artigo da Wikipédia (logo oficial) → PNG/SVG 256px;
4. favicon oficial do domínio (128px);
5. sem nada → o site usa monograma com gradiente.

Uso: python scripts/icones.py [slug ...]
"""
from __future__ import annotations

import io
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import quote, urlparse

RAIZ = Path(__file__).resolve().parent.parent
DADOS = RAIZ / "dados" / "apps.json"
OVERRIDES = RAIZ / "dados" / "icones.json"
SAIDA = RAIZ / "img" / "apps"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
EXT = (".svg", ".png", ".webp", ".jpg")

WIKI_API = ("https://en.wikipedia.org/w/api.php?action=query&format=json&redirects=1"
            "&prop=pageimages&piprop=thumbnail|name&pithumbsize=256&titles=")


def baixa(url: str, timeout: int = 40) -> bytes | None:
    """GET com timeout confiável (urllib, não depende do curl)."""
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read()
    except Exception:
        return None


def limpa_destino(slug: str) -> None:
    for ext in EXT:
        p = SAIDA / f"{slug}{ext}"
        if p.exists():
            p.unlink()


def salva(slug: str, dados: bytes | None) -> bool:
    """Grava a imagem validando o tipo. Devolve True se salvou."""
    if not dados or len(dados) < 200:
        return False
    if dados.lstrip()[:4] == b"<svg":
        if b"<svg" not in dados[:500]:
            return False
        (SAIDA / f"{slug}.svg").write_bytes(dados)
        return True
    if dados[:8] == b"\x89PNG\r\n\x1a\n" or dados[:2] == b"\xff\xd8" or dados[:4] == b"\x00\x00\x01\x00":
        try:
            from PIL import Image
            import io
            img = Image.open(io.BytesIO(dados))
            largura, altura = img.size
            if largura < 24 or altura < 24:
                return False
            if not (0.45 <= largura / altura <= 2.2):
                return False
            if largura > 512 or altura > 512:
                img = img.resize((256, int(256 * altura / largura)), Image.LANCZOS)
            img.convert("RGBA").save(SAIDA / f"{slug}.png")
            return True
        except Exception:
            return False
    return False


def simple_icons(slug_icone: str) -> bytes | None:
    svg = baixa(f"https://cdn.simpleicons.org/{slug_icone}")
    if not svg or not svg.lstrip().startswith(b"<svg"):
        return None
    m = re.search(rb'fill="#([0-9a-fA-F]{6})"', svg)
    if m:
        r, g, b = (int(m.group(1)[i:i + 2], 16) / 255 for i in (0, 2, 4))
        if 0.2126 * r + 0.7152 * g + 0.0722 * b > 0.88:  # ícone quase branco
            alt = baixa(f"https://cdn.simpleicons.org/{slug_icone}/0a1a2b")
            if alt:
                return alt
    return svg


def wikipedia(titulo: str) -> bytes | None:
    api = WIKI_API + quote(titulo.replace(" ", "_"))
    corpo = baixa(api, timeout=25)
    if not corpo:
        return None
    try:
        dados = json.loads(corpo)
        paginas = dados["query"]["pages"]
        for pag in paginas.values():
            thumb = (pag.get("thumbnail") or {}).get("source")
            if thumb:
                return baixa(thumb)
    except Exception:
        return None
    return None


def favicon(url_site: str) -> bytes | None:
    host = urlparse(url_site or "").hostname
    if not host:
        return None
    return baixa(f"https://www.google.com/s2/favicons?domain={host}&sz=128", timeout=25)


def main(argv: list[str]) -> int:
    apps = json.loads(DADOS.read_text(encoding="utf-8"))["apps"]
    overrides = json.loads(OVERRIDES.read_text(encoding="utf-8")) if OVERRIDES.exists() else {}
    alvos = set(argv) if argv else None
    SAIDA.mkdir(parents=True, exist_ok=True)

    origem = {"override": 0, "simple": 0, "wiki": 0, "favicon": 0, "monograma": 0}
    for a in apps:
        if alvos and a["slug"] not in alvos:
            continue
        slug = a["slug"]
        limpa_destino(slug)
        conf = overrides.get(slug) or {}
        salvo = False

        if conf.get("logo"):
            salvo = salva(slug, baixa(conf["logo"]))
            if salvo:
                origem["override"] += 1
        # Wikipédia marcada à mão vence o Simple Icons (ícones de produto: Ps, Ai, Id…)
        if not salvo and conf.get("wiki"):
            salvo = salva(slug, wikipedia(conf["wiki"]))
            if salvo:
                origem["wiki"] += 1
        if not salvo and a.get("icone"):
            salvo = salva(slug, simple_icons(a["icone"]))
            if salvo:
                origem["simple"] += 1
        if not salvo and not conf.get("wiki"):
            titulo = a["nome"].replace(" para Windows", "").replace(" Desktop", "").replace(" Suite", "")
            salvo = salva(slug, wikipedia(titulo))
            if salvo:
                origem["wiki"] += 1
        if not salvo:
            salvo = salva(slug, favicon(a.get("site_oficial") or a.get("url_download")))
            if salvo:
                origem["favicon"] += 1
        if not salvo:
            origem["monograma"] += 1
            print(f"  · monograma: {slug}")

    print("\norigem dos ícones:", ", ".join(f"{k}={v}" for k, v in origem.items()))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
