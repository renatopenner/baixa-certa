#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Monta dados/top100.json: os 100 apps mais usados, na ordem do ranking.

A ordem vem de uma lista curada (popularidade no mercado); apps que não existem
no catálogo são ignorados e os que sobrarem entram no fim, em ordem alfabética,
até fechar 100.

Uso: python scripts/monta_top100.py
"""
from __future__ import annotations

import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DADOS = RAIZ / "dados"

# ranking curado — do mais usado para o menos usado
RANKING = [
    # navegadores e comunicação
    "chrome", "whatsapp-messenger", "instagram", "facebook", "tiktok", "youtube", "gmail",
    "google-maps", "telegram-messenger", "microsoft-edge", "firefox", "netflix", "spotify",
    "zoom", "microsoft-teams", "slack", "discord", "signal-messenger", "messenger", "viber",
    "opera", "brave", "vivaldi", "tor-browser", "webex", "teamviewer", "anydesk",
    # escritório e nuvem
    "microsoft-365", "google-drive", "onedrive", "dropbox", "mega", "notion", "trello",
    "evernote", "todoist", "acrobat-reader", "foxit-reader", "wps-office", "libreoffice",
    "onlyoffice", "pdf24", "sumatrapdf", "joplin", "obsidian", "nextcloud-desktop",
    "zotero", "anki",
    # imagem e design
    "adobe-photoshop", "illustrator", "adobe-lightroom", "indesign",
    "adobe-acrobat-pro", "canva", "figma", "coreldraw", "gimp", "krita", "inkscape",
    "paintnet", "imageglass", "irfanview", "darktable", "capture-one", "rawtherapee",
    "digikam", "affinity-photo", "affinity-designer", "blender", "freecad", "autocad",
    "sketchup-pro", "revit", "solidworks",
    # vídeo, áudio e mídia
    "adobe-premiere-pro", "after-effects", "davinci-resolve", "capcut", "obs-studio",
    "streamlabs", "filmora", "camtasia", "bandicam", "shotcut", "kdenlive", "handbrake",
    "vlc", "potplayer", "mpc-hc", "kodi", "plex", "jellyfin-media-player", "audacity",
    "audition", "animate", "aimp", "musicbee", "foobar2000", "deezer", "kmplayer",
    # utilitários
    "winrar", "7zip", "everything", "powertoys", "sharex", "rufus", "ventoy", "balenaetcher",
    "cpuz", "gpuz", "hwinfo", "crystaldiskinfo", "crystaldiskmark", "wiztree", "treesize",
    "windirstat", "autohotkey", "ditto", "quicklook", "ccleaner", "revo-uninstaller-pro",
    "driver-booster", "msi-afterburner", "hwmonitor", "memtest86", "aomei-backupper",
    "minitool-partition-wizard", "virtualbox", "localsend", "rustdesk",
    # segurança
    "avast", "kaspersky", "bitdefender", "malwarebytes-premium", "nordvpn", "expressvpn",
    "protonvpn", "bitwarden", "keepassxc", "1password", "veracrypt", "cryptomator",
    "bleachbit", "wireshark", "glasswire",
    # dev
    "vscode", "visual-studio", "intellij-idea", "pycharm", "android-studio", "docker-desktop",
    "nodejs", "java-jdk", "python", "git", "github-desktop", "postman", "xampp",
    "mysql-workbench", "ssms", "pgadmin", "dbeaver", "sourcetree", "notepadpp", "powershell",
    "windows-terminal", "winscp", "putty", "filezilla", "bruno", "cursor",
    "unity-hub", "unreal-engine",
    # internet, backup e rede
    "qbittorrent", "freefilesync", "syncthing", "duplicati", "calibre", "thunderbird",
    # IA local
    "chatgpt", "claude", "ollama", "lmstudio", "jan",
    # jogos
    "steam", "epic-games", "gog-galaxy", "battle-net", "ea-app", "ubisoft-connect",
    "rockstar-launcher", "xbox-app", "roblox", "minecraft", "valorant", "league-of-legends",
    "0ad", "supertuxkart", "openttd",
    # celular (apps que só existem na aba Celular)
    "fdroid", "keepassdx", "aegis-authenticator", "tailscale-android",
    "open-camera", "material-files", "waze", "termux",
]


def main() -> int:
    apps = json.loads((DADOS / "apps.json").read_text(encoding="utf-8"))["apps"]
    existentes = {a["slug"]: a for a in apps}
    vistos: set[str] = set()
    ranking: list[str] = []
    for slug in RANKING:
        if slug in existentes and slug not in vistos:
            ranking.append(slug)
            vistos.add(slug)
        if len(ranking) == 100:
            break
    if len(ranking) < 100:
        # completa com apps de destaque e depois alfabético
        resto = sorted(
            (a for a in apps if a["slug"] not in vistos),
            key=lambda a: (not a.get("destaque"), a["nome"].lower()),
        )
        for a in resto:
            ranking.append(a["slug"])
            vistos.add(a["slug"])
            if len(ranking) == 100:
                break
    saida = {
        "atualizado": "2026-11-12",
        "total": len(ranking),
        "itens": ranking,
    }
    (DADOS / "top100.json").write_text(
        json.dumps(saida, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"top100.json: {len(ranking)} apps")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
