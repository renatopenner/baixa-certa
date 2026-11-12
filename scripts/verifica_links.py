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
import sys
import time
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ARQ = RAIZ / "dados" / "apps.json"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")


def cabeçalho(url: str) -> dict:
    """Status, content-type e URL final (segue redirects), com timeout confiável."""
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*",
                                               "Range": "bytes=0-0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return {"status": resp.status,
                    "tipo": resp.headers.get("Content-Type", "") or "",
                    "final": resp.geturl(),
                    "bytes": resp.headers.get("Content-Length") and
                    int(resp.headers.get("Content-Length")) or None}
    except urllib.error.HTTPError as exc:
        tipo = exc.headers.get("Content-Type", "") if exc.headers else ""
        return {"status": exc.code, "tipo": tipo or "", "final": exc.geturl() or url,
                "bytes": None}
    except Exception:
        return {"status": 0, "tipo": "", "final": url, "bytes": None}


def tamanho_por_head(url: str) -> str | None:
    """Tenta o Content-Length do HEAD do arquivo, para exibir o tamanho real."""
    req = urllib.request.Request(url, headers={"User-Agent": UA}, method="HEAD")
    try:
        with urllib.request.urlopen(req, timeout=25) as resp:
            tamanho = resp.headers.get("Content-Length")
    except Exception:
        return None
    if not tamanho or not tamanho.isdigit():
        return None
    mb = int(tamanho) / (1024 * 1024)
    return (f"{mb / 1024:.1f} GB" if mb >= 1024 else f"{mb:.0f} MB" if mb >= 10 else f"{mb:.1f} MB")


def url_estavel(final: str, original: str) -> str:
    """Não grava URL assinada/temporária (expira e suja a página do app)."""
    baixo = (final or "").lower()
    temporaria = (
        "sig=" in baixo or "x-amz-" in baixo or "release-assets.githubusercontent.com" in baixo
        or "expires=" in baixo or "response-content-disposition=" in baixo
    )
    return original if (not final or temporaria) else final


def main(argv: list[str]) -> int:
    dados = json.loads(ARQ.read_text(encoding="utf-8"))
    hoje = date.today().isoformat()
    alvos = set(argv) if argv else None
    problemas = 0
    anterior = {a["slug"]: (a.get("status_http"), a.get("url_download_final"),
                            a.get("content_type"), a.get("tipo_download"))
                for a in dados["apps"]}

    for a in dados["apps"]:
        if alvos and a["slug"] not in alvos:
            continue
        url = a.get("url_download") or a.get("url_download_final")
        r = cabeçalho(url)
        if r["status"] == 0:  # timeout/limite de conexão: tenta mais uma vez
            time.sleep(2)
            r = cabeçalho(url)
        if r["status"] == 0:
            # segue inconclusivo: mantém o último resultado bom em vez de zerar
            status_ant, final_ant, tipo_ant, tipo_dl_ant = anterior[a["slug"]]
            if status_ant and 200 <= int(status_ant) < 400:
                a["status_http"] = status_ant
                a["url_download_final"] = final_ant
                a["content_type"] = tipo_ant
                a["tipo_download"] = tipo_dl_ant
                print(f"[TIMEOUT] {a['slug']:<16} mantido status anterior {status_ant}")
                continue
        status = r["status"]
        ok = 200 <= status < 400
        # 403/400/429 = site oficial barrando robô, não quer dizer link morto
        bloqueio = status in (400, 403, 406, 429)
        if not ok and not bloqueio:
            problemas += 1
        a["status_http"] = status
        a["url_download_final"] = url_estavel(r["final"], url)
        a["content_type"] = r["tipo"]
        a["url_verificado_em"] = hoje
        # se a URL respondeu com HTML, é página e não arquivo
        if ok and "text/html" in (r["tipo"] or ""):
            a["tipo_download"] = "pagina"
        elif ok and any(k in (r["tipo"] or "") for k in
                        ("octet-stream", "msdownload", "x-msi", "dmg", "zip",
                         "android", "x-apple-diskimage", "7z", "x-7z", "gzip", "x-tar")):
            a["tipo_download"] = "direto"
        # tamanho só faz sentido para arquivo (e nunca a partir de range de 1 byte)
        if a["tipo_download"] != "direto" or a.get("tamanho_arquivo") in ("0 KB", "0 MB"):
            if not r["bytes"] or r["bytes"] <= 1024:
                a["tamanho_arquivo"] = None if a["tipo_download"] != "direto" else a.get("tamanho_arquivo")
        if (r["bytes"] and r["bytes"] > 1024 and a["tipo_download"] == "direto"
                and not a.get("tamanho_arquivo")):
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
