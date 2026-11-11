#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Consolida a pesquisa (pesquisa/links-*.json) em dados/apps.json.

- valida campos obrigatórios, categorias e formato dos links;
- completa com ícone (Simple Icons), destaque e texto de segurança;
- grava dados/apps.json no formato que o gerador espera.

Uso: python scripts/consolida.py
"""
from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DADOS = RAIZ / "dados"
FONTES = [
    RAIZ / "pesquisa" / "links-a.json",
    RAIZ / "pesquisa" / "links-b.json",
    RAIZ / "pesquisa" / "links-c.json",
]
CATEGORIAS = json.loads((DADOS / "categorias.json").read_text(encoding="utf-8"))

# apps descartados da pesquisa, com o motivo (não entram no catálogo)
DESCARTADOS = {
    "drift-hunters": "sem site oficial do desenvolvedor — só portais e espelhos, o que fere a regra "
                     "de link oficial; candidatos substitutos verificados em links-c.json",
}

# slug do site -> slug do ícone no Simple Icons (None = monograma)
ICONES = {
    "libreoffice": "libreoffice",
    "onlyoffice": "onlyoffice",
    "joplin": "joplin",
    "obsidian": "obsidian",
    "zotero": "zotero",
    "vlc": "vlcmediaplayer",
    "kdenlive": "kdenlive",
    "handbrake": "handbrake",
    "obs-studio": "obsstudio",
    "audacity": "audacity",
    "foobar2000": "foobar2000",
    "gimp": "gimp",
    "krita": "krita",
    "inkscape": "inkscape",
    "darktable": "darktable",
    "blender": "blender",
    "freecad": "freecad",
    "vscode": "visualstudiocode",
    "git": "git",
    "notepadpp": "notepadplusplus",
    "python": "python",
    "dbeaver": "dbeaver",
    "github-desktop": "github",
    "7zip": "7zip",
    "sharex": "sharex",
    "rufus": "rufus",
    "ventoy": "ventoy",
    "autohotkey": "autohotkey",
    "bitwarden": "bitwarden",
    "keepassxc": "keepassxc",
    "veracrypt": "veracrypt",
    "protonvpn": "protonvpn",
    "bleachbit": "bleachbit",
    "tor-browser": "torproject",
    "brave": "brave",
    "firefox": "firefox",
    "telegram": "telegram",
    "discord": "discord",
    "whatsapp": "whatsapp",
    "signal": "signal",
    "thunderbird": "thunderbird",
    "qbittorrent": "qbittorrent",
    "filezilla": "filezilla",
    "syncthing": "syncthing",
    "ollama": "ollama",
    "epic-games": "epicgames",
    "steam": "steam",
    "0ad": "0ad",
    "supertuxkart": "supertuxkart",
    "openttd": "openttd",
}

DESTAQUES = [
    "libreoffice", "vlc", "davinci-resolve", "obs-studio",
    "gimp", "7zip", "vscode", "qbittorrent",
]

ESPERADOS = {
    # grupo A
    "libreoffice", "onlyoffice", "sumatrapdf", "pdf24", "joplin", "obsidian", "zotero",
    "vlc", "davinci-resolve", "shotcut", "kdenlive", "handbrake", "obs-studio", "audacity",
    "foobar2000", "gimp", "krita", "inkscape", "paintnet", "darktable", "blender", "freecad",
    "vscode", "git", "notepadpp", "python", "dbeaver", "github-desktop",
    # grupo B
    "7zip", "everything", "powertoys", "sharex", "rufus", "ventoy", "cpuz", "hwinfo",
    "crystaldiskinfo", "wiztree", "autohotkey", "bitwarden", "keepassxc", "veracrypt",
    "protonvpn", "bleachbit", "tor-browser", "brave", "firefox", "telegram", "discord",
    "whatsapp", "signal", "thunderbird", "qbittorrent", "filezilla", "putty", "freefilesync",
    "syncthing", "duplicati", "ollama", "lmstudio", "jan", "epic-games", "steam",
    # grupo C (jogos verificados manualmente; drift-hunters descartado)
    "0ad", "supertuxkart", "openttd",
}

CAMPOS_OBRIG = ("slug", "nome", "fabricante", "categoria", "site_oficial", "url_download",
                "tipo_download", "resumo", "descricao", "destaques", "licenca", "gratis",
                "requisitos")


def limpa(txt):
    if txt is None:
        return None
    if not isinstance(txt, str):
        return txt
    txt = re.sub(r"\s+", " ", txt).strip()
    return txt or None


def valida(app: dict, erros: list[str]) -> None:
    slug = app.get("slug", "?")
    for campo in CAMPOS_OBRIG:
        if app.get(campo) in (None, "", [], {}):
            erros.append(f"{slug}: campo obrigatório ausente -> {campo}")
    if app.get("categoria") not in CATEGORIAS:
        erros.append(f"{slug}: categoria inválida -> {app.get('categoria')}")
    if app.get("tipo_download") not in ("direto", "pagina"):
        erros.append(f"{slug}: tipo_download inválido -> {app.get('tipo_download')}")
    for campo in ("url_download", "url_download_final", "site_oficial"):
        valor = app.get(campo)
        if valor and not str(valor).startswith("https://"):
            erros.append(f"{slug}: {campo} não é https -> {valor}")
    resumo = app.get("resumo") or ""
    if not (60 <= len(resumo) <= 210):
        erros.append(f"{slug}: resumo com {len(resumo)} caracteres (esperado 60-210)")
    desc = app.get("descricao") or ""
    if len(desc) < 180:
        erros.append(f"{slug}: descricao curta ({len(desc)} caracteres)")
    if not isinstance(app.get("destaques"), list) or len(app["destaques"]) < 2:
        erros.append(f"{slug}: destaques precisam ser lista com 2+ itens")
    if app.get("so") and not isinstance(app["so"], list):
        erros.append(f"{slug}: so precisa ser lista")


def main() -> int:
    apps: list[dict] = []
    erros: list[str] = []
    vistos: set[str] = set()

    for fonte in FONTES:
        if not fonte.exists():
            print(f"! fonte ausente: {fonte}", file=sys.stderr)
            continue
        dados = json.loads(fonte.read_text(encoding="utf-8"))
        for bruto in dados.get("apps", []):
            app = {k: limpa(v) if isinstance(v, str) else v for k, v in bruto.items()}
            app["slug"] = (app.get("slug") or "").strip().lower()
            if app["slug"] in DESCARTADOS:
                print(f"descartado: {app['slug']} — {DESCARTADOS[app['slug']]}", file=sys.stderr)
                continue
            if app["slug"] in vistos:
                erros.append(f"{app['slug']}: duplicado")
                continue
            vistos.add(app["slug"])
            app.setdefault("so", ["windows"])
            app["so"] = [s for s in app["so"] if s in ("windows", "mac", "linux", "web")] or ["windows"]
            app["destaques"] = [limpa(d) for d in (app.get("destaques") or []) if limpa(d)][:4]
            app["icone"] = ICONES.get(app["slug"])
            app["destaque"] = app["slug"] in DESTAQUES
            app["url_verificado_em"] = app.get("url_verificado_em") or dados.get("verificado_em") or date.today().isoformat()
            valida(app, erros)
            apps.append(app)

    faltando = ESPERADOS - vistos
    if faltando:
        erros.append("apps não pesquisados: " + ", ".join(sorted(faltando)))
    extras = vistos - ESPERADOS
    if extras:
        print("aviso: apps fora da pauta: " + ", ".join(sorted(extras)), file=sys.stderr)

    if erros:
        print(f"{len(erros)} problema(s) nos dados:", file=sys.stderr)
        for e in erros[:80]:
            print(" -", e, file=sys.stderr)
        if len(erros) > 80:
            print(f" ... e mais {len(erros) - 80}", file=sys.stderr)

    apps.sort(key=lambda a: a["nome"].lower())
    saida = {
        "atualizado": date.today().isoformat(),
        "total": len(apps),
        "apps": apps,
    }
    (DADOS / "apps.json").write_text(
        json.dumps(saida, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"dados/apps.json: {len(apps)} apps, {len(erros)} erro(s) de validação")
    return 1 if erros else 0


if __name__ == "__main__":
    sys.exit(main())
