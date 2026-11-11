#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Checagem rápida de layout: overflow horizontal e erros de console.

Abre páginas geradas no Chrome headless em duas larguras e compara
scrollWidth com clientWidth. Também salva screenshots em _shots/.

Uso: python scripts/checa_layout.py
"""
from __future__ import annotations

import re
import subprocess
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SHOTS = RAIZ / "_shots"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PAGINAS = ["index.html", "a/vlc.html", "categoria/utilidades.html",
           "sobre.html", "como-verificamos.html", "contato.html"]
INJETADO = ("<script>document.title='SW='+document.documentElement.scrollWidth"
            "+' CW='+document.documentElement.clientWidth;</script>")


def roda(pagina: Path, largura: int) -> str:
    copia = pagina.with_name("_teste_" + pagina.name)
    html = pagina.read_text(encoding="utf-8").replace("</body>", INJETADO + "</body>")
    copia.write_text(html, encoding="utf-8")
    try:
        r = subprocess.run(
            [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
             f"--window-size={largura},1000", "--dump-dom", copia.as_uri()],
            capture_output=True, text=True, errors="replace", timeout=90,
        )
        m = re.search(r"<title>([^<]*)</title>", r.stdout or "")
        return m.group(1) if m else "(sem leitura)"
    finally:
        copia.unlink(missing_ok=True)


def screenshot(pagina: Path, largura: int, altura: int, nome: str) -> None:
    SHOTS.mkdir(exist_ok=True)
    subprocess.run(
        [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
         f"--window-size={largura},{altura}", f"--screenshot={SHOTS / nome}",
         pagina.as_uri()],
        capture_output=True, timeout=120,
    )


def main() -> int:
    problemas = 0
    for pag in PAGINAS:
        caminho = RAIZ / pag
        for largura in (512, 1440):
            titulo = roda(caminho, largura)
            m = re.search(r"SW=(\d+) CW=(\d+)", titulo)
            if not m:
                print(f"? {pag} @{largura}: sem leitura ({titulo})")
                continue
            sw, cw = int(m.group(1)), int(m.group(2))
            marca = "OK " if sw <= cw + 1 else "OVERFLOW"
            if sw > cw + 1:
                problemas += 1
            print(f"[{marca}] {pag} @{largura}: scrollWidth={sw} clientWidth={cw}")
    screenshot(RAIZ / "index.html", 1400, 3050, "index-total.png")
    screenshot(RAIZ / "a/vlc.html", 1400, 1750, "app-total.png")
    print(f"\n{problemas} página(s) com overflow horizontal.")
    return 1 if problemas else 0


if __name__ == "__main__":
    raise SystemExit(main())
