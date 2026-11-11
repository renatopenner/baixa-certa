#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Confere os links de download de dados/apps.json e grava o resultado.

Para cada app: segue redirecionamentos, pega o status HTTP final, o
content-type, a URL final e (quando disponível) o tamanho do arquivo.
Atualiza os campos no próprio apps.json:
    status_http, url_download_final, content_type, tamanho_arquivo,
    url_verificado_em

Uso:
    python scripts/verifica_links.py            # confere tudo
    python scripts/verifica_links.py vlc gimp   # confere só estes slugs
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ARQ = RAIZ / "dados" / "apps.json"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
FMT = "%{http_code}|%{content_type}|%{url_effective}|%{size_download}"


def cabeçalho(url: str) -> dict:
    r = subprocess.run(
        ["curl.exe", "-sSL", "--compressed", "--max-time", "45", "-A", UA,
         "-r", "0-0", "-o", "NUL", "-w", FMT, url],
        capture_output=True, text=True, errors="replace",
    )
    saida = (r.stdout or "").strip().splitlines()
    linha = saida[-1] if saida else ""
    partes = linha.split("|")
    if len(partes) < 4:
        return {"status": 0, "tipo": "", "final": url, "bytes": None}
    status, tipo, final, tamanho = partes[0], partes[1], partes[2], partes[3]
    try:
        status_i = int(status)
    except ValueError:
        status_i = 0
    return {
        "status": status_i,
        "tipo": tipo,
        "final": final or url,
        "bytes": int(tamanho) if tamanho.isdigit() and int(tamanho) > 1 else None,
    }


def tamanho_por_head(url: str) -> str | None:
    """Tenta o Content-Length do HEAD do arquivo, para exibir o tamanho real."""
    r = subprocess.run(
        ["curl.exe", "-sSIL", "--max-time", "30", "-A", UA, url],
        capture_output=True, text=True, errors="replace",
    )
    tamanhos = [int(x) for x in re.findall(r"(?im)^content-length:\s*(\d+)", r.stdout or "")]
    if not tamanhos:
        return None
    mb = max(tamanhos) / (1024 * 1024)
    return (f"{mb / 1024:.1f} GB" if mb >= 1024 else f"{mb:.0f} MB" if mb >= 10 else f"{mb:.1f} MB")


def main(argv: list[str]) -> int:
    dados = json.loads(ARQ.read_text(encoding="utf-8"))
    hoje = date.today().isoformat()
    alvos = set(argv) if argv else None
    problemas = 0

    for a in dados["apps"]:
        if alvos and a["slug"] not in alvos:
            continue
        url = a.get("url_download") or a.get("url_download_final")
        r = cabeçalho(url)
        status = r["status"]
        ok = 200 <= status < 400
        if not ok:
            problemas += 1
        a["status_http"] = status
        a["url_download_final"] = r["final"]
        a["content_type"] = r["tipo"]
        a["url_verificado_em"] = hoje
        # se a URL respondeu com HTML, é página e não arquivo
        if ok and "text/html" in (r["tipo"] or ""):
            a["tipo_download"] = "pagina"
        elif ok and any(k in (r["tipo"] or "") for k in
                        ("octet-stream", "msdownload", "x-msi", "dmg", "zip",
                         "x-apple-diskimage", "7z", "x-7z", "gzip", "x-tar")):
            a["tipo_download"] = "direto"
        if r["bytes"] and not a.get("tamanho_arquivo"):
            b = r["bytes"]
            a["tamanho_arquivo"] = (f"{b / 1024 / 1024:.0f} MB" if b >= 1024 * 1024 else f"{b / 1024:.0f} KB")
        if a["tipo_download"] == "direto" and not a.get("tamanho_arquivo"):
            t = tamanho_por_head(r["final"])
            if t:
                a["tamanho_arquivo"] = t
        marca = "OK " if ok else "ERRO"
        print(f"[{marca}] {a['slug']:<16} {status} {r['tipo'][:28]:<28} {r['final'][:90]}")

    dados["atualizado"] = hoje
    ARQ.write_text(json.dumps(dados, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\n{len([a for a in dados['apps'] if not alvos or a['slug'] in alvos])} links conferidos, "
          f"{problemas} com problema. atualizado={hoje}")
    return 1 if problemas else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
