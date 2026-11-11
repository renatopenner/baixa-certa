#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador estático do Baixa Certa.

Lê dados/apps.json + dados/categorias.json e escreve:
  index.html, categoria/*.html, a/*.html, sobre.html, como-verificamos.html,
  contato.html, 404.html, sitemap.xml, robots.txt

Uso:
  python scripts/gerar.py            # gera o site
  python scripts/gerar.py --check    # apenas valida os dados
"""
from __future__ import annotations

import html
import json
import re
import sys
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DADOS = RAIZ / "dados"
URL_BASE = "https://baixa.pennertech.com.br"
SITE = "Baixa Certa"
MARCA = "Baixa Certa · Penner Tech"
DESCRICAO_PADRAO = (
    "Portal de aplicativos gratuitos com download direto do site oficial do fabricante. "
    "Sem instalador empacotado, sem cadastro e sem propaganda enganosa."
)

# --------------------------------------------------------------------------- #
# ícones (SVG inline, traço)
# --------------------------------------------------------------------------- #
def _svg(corpo: str, cls: str = "i", extra: str = "") -> str:
    return (
        f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        f'stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" '
        f'aria-hidden="true" {extra}>{corpo}</svg>'
    )


ICONES = {
    "busca": _svg('<circle cx="11" cy="11" r="7"/><path d="m20 20-3.6-3.6"/>'),
    "download": _svg('<path d="M12 3v12"/><path d="m7 11 5 5 5-5"/><path d="M5 21h14"/>'),
    "check": _svg('<path d="m20 6-11 11-5-5"/>'),
    "seta": _svg('<path d="M5 12h14"/><path d="m13 6 6 6-6 6"/>'),
    "info": _svg('<circle cx="12" cy="12" r="9"/><path d="M12 16v-4.5M12 8h.01"/>'),
    "escudo": _svg('<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>'),
    "cadeado": _svg('<rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>'),
    "relogio": _svg('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>'),
    "link": _svg('<path d="M10 13a5 5 0 0 0 7 0l3-3a5 5 0 0 0-7-7l-1.5 1.5"/>'
                 '<path d="M14 11a5 5 0 0 0-7 0l-3 3a5 5 0 0 0 7 7L12.5 19.5"/>'),
    "doc": _svg('<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>'
                '<path d="M14 2v6h6"/><path d="M8 13h8M8 17h5"/>'),
    "play": _svg('<circle cx="12" cy="12" r="9"/><path d="m10 8.5 5.5 3.5L10 15.5z"/>'),
    "image": _svg('<rect x="3" y="3" width="18" height="18" rx="2"/>'
                  '<circle cx="9" cy="9" r="1.8"/><path d="m21 15-5-5L5 21"/>'),
    "code": _svg('<path d="m16 18 6-6-6-6"/><path d="m8 6-6 6 6 6"/>'),
    "tools": _svg('<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77'
                  'a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91'
                  'a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>'),
    "globe": _svg('<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/>'
                  '<path d="M12 3a15 15 0 0 1 4 9 15 15 0 0 1-4 9 15 15 0 0 1-4-9 15 15 0 0 1 4-9z"/>'),
    "backup": _svg('<path d="M21 12a9 9 0 1 1-3-6.7"/><path d="M21 3v6h-6"/>'
                   '<path d="M12 8v5l3 2"/>'),
    "spark": _svg('<path d="m12 3 1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9z"/>'
                  '<path d="M18.5 15.5 19 17l1.5.5L19 18l-.5 1.5-.5-1.5L16.5 18l1.5-.5z"/>'),
    "game": _svg('<rect x="2" y="6.5" width="20" height="11" rx="4"/>'
                 '<path d="M7 12h4M9 10v4"/><path d="M15.5 10.5h.01M17.8 12.8h.01"/>'),
    "windows": _svg('<rect x="3" y="4" width="8" height="7" rx="1"/><rect x="13" y="4" width="8" height="7" rx="1"/>'
                     '<rect x="3" y="13" width="8" height="7" rx="1"/><rect x="13" y="13" width="8" height="7" rx="1"/>'),
    "mac": _svg('<path d="M16 3.5c-1 .1-2.2.8-2.9 1.8-.6.9-1.1 2.2-.9 3.5 1.2.1 2.4-.6 3.1-1.6.7-.9 1.1-2.2.9-3.5z"/>'
                '<path d="M18.7 15.5c-.6 1.3-1.4 2.6-2.5 3.8-1 1.1-2 1.7-3.1 1.7-1 0-1.7-.4-2.6-.7-.9-.3-1.7-.6-2.6-.6'
                's-1.8.3-2.7.6c-.9.3-1.6.7-2.5.7-1.2 0-2.3-.8-3.3-2C-.4 15.6 1 10.7 3.7 9c1.2-.7 2.4-1.1 3.6-1.1'
                '1.1 0 1.9.4 2.7.7.8.3 1.5.6 2.4.6.8 0 1.5-.3 2.4-.6.9-.3 1.8-.7 3-.7 1 0 2 .3 3 .9-2.4 1.4-2 4.9-2.1 6.7z"/>'),
    "linux": _svg('<rect x="5" y="9" width="14" height="11" rx="4"/>'
                  '<path d="M9 3.8c0-1.1 1.3-1.9 3-1.9s3 .8 3 1.9c0 1.4-.8 2.1-.8 3.2h-4.4c0-1.1-.8-1.8-.8-3.2z"/>'
                  '<path d="M8 14h.01M16 14h.01"/><path d="M9 20v1.5M15 20v1.5"/>'),
}

# --------------------------------------------------------------------------- #
# utilidades
# --------------------------------------------------------------------------- #
def esc(valor) -> str:
    return html.escape(str(valor if valor is not None else ""), quote=True)


def slug_ok(txt: str) -> str:
    return re.sub(r"[^a-z0-9-]+", "-", txt.lower()).strip("-")


def carrega_json(caminho: Path):
    with open(caminho, encoding="utf-8") as fh:
        return json.load(fh)


def data_br(iso: str | None) -> str:
    if not iso:
        return ""
    try:
        return date.fromisoformat(iso).strftime("%d/%m/%Y")
    except ValueError:
        return iso


def plataformas(so: list[str]) -> str:
    nomes = {"windows": "Windows", "mac": "macOS", "linux": "Linux",
             "android": "Android", "ios": "iOS", "web": "Navegador"}
    ordem = ["windows", "mac", "linux", "android", "ios", "web"]
    return " · ".join(nomes[p] for p in ordem if p in so)


def plataformas_curto(so: list[str]) -> str:
    nomes = {"windows": "Windows", "mac": "macOS", "linux": "Linux",
             "android": "Android", "ios": "iOS", "web": "Web"}
    ordem = ["windows", "mac", "linux", "android", "ios", "web"]
    return " · ".join(nomes[p] for p in ordem if p in so)


def loja_do_link(url: str) -> str:
    """Identifica loja oficial para escolher o rótulo do botão."""
    u = (url or "").lower()
    if "play.google.com" in u:
        return "play"
    if "apps.apple.com" in u or "itunes.apple.com" in u:
        return "appstore"
    if "f-droid.org" in u:
        return "fdroid"
    return ""


def url_app(app: dict) -> str:
    return (app.get("url_download_final") or app.get("url_download") or "").strip()


def eh_direto(app: dict) -> bool:
    return (app.get("tipo_download") or "pagina").lower() == "direto"


def iniciais(nome: str) -> str:
    partes = [p for p in re.split(r"[\s\-\.]+", nome) if p and p[0].isalnum()]
    if not partes:
        return "?"
    if len(partes) == 1:
        return partes[0][:2].upper()
    return (partes[0][0] + partes[1][0]).upper()


def plural(n: int, singular: str, plural_: str) -> str:
    return f"{n} {singular if n == 1 else plural_}"


def resumo(texto: str, limite: int = 158) -> str:
    """Corta um texto no limite (palavra inteira) para meta description."""
    texto = " ".join((texto or "").split())
    if len(texto) <= limite:
        return texto
    corte = texto[:limite].rsplit(" ", 1)[0].rstrip(",.;:")
    return corte + "…"


def icone_app(app: dict, raiz: str = "", classe: str = "") -> str:
    """SVG local do app (img/apps/<slug>.svg) ou monograma."""
    arq = RAIZ / "img" / "apps" / f"{app['slug']}.svg"
    if arq.exists():
        return (
            f'<img src="{raiz}img/apps/{app["slug"]}.svg" alt="" width="40" height="40" '
            f'loading="lazy" decoding="async" class="{classe}">'
        )
    return f'<span class="mono" aria-hidden="true">{esc(iniciais(app["nome"]))}</span>'


# --------------------------------------------------------------------------- #
# componentes
# --------------------------------------------------------------------------- #
def logo_marca(sufixo: str = "topo") -> str:
    """Logo da marca. O id do gradiente é único por posição (cabeçalho/rodapé)."""
    gid = f"lgBx-{sufixo}"
    return (
        '<svg viewBox="0 0 48 48" role="img" aria-label="Baixa Certa">'
        f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="#0a7cbf"/><stop offset="1" stop-color="#12b5d0"/></linearGradient></defs>'
        '<rect width="48" height="48" rx="13" fill="url(#%s)"/>' % gid
        + '<path d="M24 12.5v14.2" stroke="#fff" stroke-width="4" stroke-linecap="round"/>'
        '<path d="m17.2 21.4 6.8 6.8 6.8-6.8" stroke="#fff" stroke-width="4" stroke-linecap="round" '
        'stroke-linejoin="round"/>'
        '<path d="M15 34.6h18" stroke="#fff" stroke-width="3.4" stroke-linecap="round" opacity=".9"/>'
        "</svg>"
    )


def head(titulo: str, descricao: str, canonical: str, raiz: str, og_tipo: str = "website",
         extra_head: str = "") -> str:
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(titulo)}</title>
<meta name="description" content="{esc(descricao)}">
<link rel="canonical" href="{esc(canonical)}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="#ffffff">
<meta name="author" content="Penner Tech">
<meta property="og:type" content="{esc(og_tipo)}">
<meta property="og:site_name" content="{SITE}">
<meta property="og:locale" content="pt_BR">
<meta property="og:title" content="{esc(titulo)}">
<meta property="og:description" content="{esc(descricao)}">
<meta property="og:url" content="{esc(canonical)}">
<meta property="og:image" content="{URL_BASE}/img/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(titulo)}">
<meta name="twitter:description" content="{esc(descricao)}">
<meta name="twitter:image" content="{URL_BASE}/img/og-image.png">
<link rel="icon" href="{raiz}img/favicon.svg" type="image/svg+xml">
<link rel="icon" href="{raiz}img/favicon-64.png" type="image/png" sizes="64x64">
<link rel="apple-touch-icon" href="{raiz}img/apple-touch-icon.png">
<link rel="stylesheet" href="{raiz}css/estilo.css?v=1">
<script defer src="{raiz}js/site.js?v=1"></script>
{extra_head}</head>"""


def topo(raiz: str, ativo: str = "") -> str:
    def cls(nome: str) -> str:
        return ' class="on"' if ativo == nome else ""

    return f"""<body>
<header class="topo">
  <div class="wrap topo-in">
    <a class="marca" href="{raiz}index.html" aria-label="Baixa Certa — início">
      {logo_marca('topo')}
      <span class="marca-txt"><b>BAIXA</b><em>CERTA</em></span>
    </a>
    <nav class="menu" aria-label="Principal">
      <a href="{raiz}index.html"{cls('inicio')}>Início</a>
      <a href="{raiz}index.html#categorias">Categorias</a>
      <a href="{raiz}categoria/celular.html"{cls('celular')}>Celular</a>
      <a href="{raiz}como-verificamos.html"{cls('verificamos')}>Como verificamos</a>
      <a href="{raiz}sobre.html"{cls('sobre')}>Sobre</a>
      <a href="{raiz}contato.html"{cls('contato')}>Contato</a>
    </nav>
    <a class="btn btn-ghost btn-mini topo-cta" href="{raiz}index.html#catalogo">Ver catálogo</a>
  </div>
</header>"""


def rodape(raiz: str, apps: list[dict], categorias: dict, atualizado: str) -> str:
    links_cat = "\n".join(
        f'<li><a href="{raiz}categoria/{s}.html">{esc(c["curto"])}</a></li>'
        for s, c in categorias.items()
    )
    return f"""<footer class="rodape">
  <div class="wrap">
    <div class="rodape-topo">
      <div>
        <a class="marca" href="{raiz}index.html" aria-label="Baixa Certa — início">
          {logo_marca('rodape')}
          <span class="marca-txt"><b>BAIXA</b><em>CERTA</em></span>
        </a>
        <p class="desc">Os {len(apps)} aplicativos gratuitos que eu instalo e recomendo — com link
        direto para o site oficial do fabricante. Um projeto
        <a href="https://loja.pennertech.com.br/" target="_blank" rel="noopener">Penner Tech</a>.</p>
      </div>
      <div>
        <h4>Categorias</h4>
        <ul class="cats">
        {links_cat}
        </ul>
      </div>
      <div>
        <h4>O site</h4>
        <ul>
          <li><a href="{raiz}index.html#catalogo">Todos os apps</a></li>
          <li><a href="{raiz}como-verificamos.html">Como verificamos</a></li>
          <li><a href="{raiz}sobre.html">Sobre o Baixa Certa</a></li>
          <li><a href="{raiz}contato.html">Contato e sugestões</a></li>
        </ul>
      </div>
      <div>
        <h4>Penner Tech</h4>
        <ul>
          <li><a href="https://loja.pennertech.com.br/" target="_blank" rel="noopener">Loja e recomendações</a></li>
          <li><a href="https://www.youtube.com/@renatopenner2037" target="_blank" rel="noopener">YouTube</a></li>
          <li><a href="https://www.instagram.com/pennerrenato/" target="_blank" rel="noopener">Instagram</a></li>
        </ul>
      </div>
    </div>
    <div class="rodape-base">
      <p><strong>Baixa Certa</strong> não hospeda arquivos: cada botão leva ao download publicado
      pelo próprio fabricante. Marcas e programas pertencem aos seus donos. Links verificados em
      {esc(data_br(atualizado))}.</p>
      <p class="penner">{ICONES['escudo']} Feito por Penner Tech · Belém/PA</p>
    </div>
  </div>
</footer>
</body>
</html>
"""


def card_app(app: dict, raiz: str, categoria_nome: str) -> str:
    url = url_app(app)
    loja = loja_do_link(url)
    if eh_direto(app):
        tipo_tag = '<span class="tag tag-ok">Link direto</span>'
        rotulo = "Baixar"
    else:
        rotulo_loja = {"play": "Play Store", "appstore": "App Store", "fdroid": "F-Droid"}
        tipo_tag = (f'<span class="tag tag-link">{rotulo_loja[loja]}</span>' if loja
                    else '<span class="tag tag-link">Página oficial</span>')
        rotulo = "Abrir" if loja in ("play", "appstore") else "Baixar no site"
    gratis_tag = '<span class="tag">Grátis</span>'
    fab = app["fabricante"]
    if app["categoria"] == "celular":
        fab = f"{fab} · {plataformas_curto(app.get('so') or [])}"
    busca = f"{app['nome']} {app['fabricante']} {categoria_nome} {app['resumo']} {' '.join(app.get('destaques', []))}"
    return f"""<article class="app" data-cat="{esc(app['categoria'])}" data-busca="{esc(busca)}">
  <div class="app-cab">
    <a class="app-ico" href="{raiz}a/{app['slug']}.html" tabindex="-1" aria-hidden="true">
      {icone_app(app, raiz)}
    </a>
    <div class="app-tit">
      <h3><a href="{raiz}a/{app['slug']}.html">{esc(app['nome'])}</a></h3>
      <div class="app-fab">{esc(fab)}</div>
    </div>
  </div>
  <p class="app-res">{esc(app['resumo'])}</p>
  <div class="app-pe">
    <div class="app-tags">{gratis_tag}{tipo_tag}<span class="tag">{esc(categoria_nome)}</span></div>
    <a class="btn btn-baixar" href="{esc(url)}" target="_blank" rel="noopener" title="{esc(app['nome'])} — download oficial">{rotulo}</a>
  </div>
</article>"""


def card_destaque(app: dict, raiz: str, categoria_nome: str) -> str:
    url = url_app(app)
    loja = loja_do_link(url)
    if eh_direto(app):
        rotulo = "Baixar agora"
    elif loja in ("play", "appstore"):
        rotulo = "Abrir na loja"
    else:
        rotulo = "Ver no site oficial"
    return f"""<article class="destaque">
  <a class="ico" href="{raiz}a/{app['slug']}.html" tabindex="-1" aria-hidden="true">{icone_app(app, raiz)}</a>
  <div class="corpo">
    <h3><a href="{raiz}a/{app['slug']}.html" style="color:inherit">{esc(app['nome'])}</a></h3>
    <p class="res">{esc(app['resumo'])}</p>
    <div class="pe">
      <span class="tag tag-ok">Grátis</span>
      <span class="tag">{esc(categoria_nome)}</span>
      <a class="btn btn-baixar" href="{esc(url)}" target="_blank" rel="noopener">{rotulo}</a>
    </div>
  </div>
</article>"""


def chips_categorias(categorias: dict, contagem: dict, raiz: str,
                     ativa: str = "todos", modo: str = "filtro") -> str:
    """modo='filtro' (index, filtra na tela) ou 'links' (páginas de categoria)."""
    total = sum(v for k, v in contagem.items() if k != "todos")
    itens = []
    if modo == "links":
        todos_on = ' on' if ativa == "todos" else ""
        itens.append(
            f'<a class="chip{todos_on}" href="{raiz}index.html#catalogo">Todos '
            f'<span class="n">{total}</span></a>'
        )
        for s, c in categorias.items():
            on = ' on' if ativa == s else ""
            itens.append(
                f'<a class="chip{on}" href="{s}.html">{esc(c["curto"])} '
                f'<span class="n">{contagem.get(s, 0)}</span></a>'
            )
    else:
        itens.append(
            f'<button type="button" class="chip{" on" if ativa == "todos" else ""}" '
            f'data-chip data-cat="todos">Todos <span class="n">{total}</span></button>'
        )
        for s, c in categorias.items():
            on = ' on' if ativa == s else ""
            itens.append(
                f'<button type="button" class="chip{on}" data-chip data-cat="{s}">{esc(c["curto"])} '
                f'<span class="n">{contagem.get(s, 0)}</span></button>'
            )
    return '<div class="chips" role="group" aria-label="Filtrar por categoria">' + "".join(itens) + "</div>"


def grade_apps(apps: list[dict], raiz: str, categorias: dict) -> str:
    blocos = "\n".join(
        card_app(a, raiz, categorias[a["categoria"]]["curto"]) for a in apps
    )
    return f'<div class="grade-apps" id="grade">\n{blocos}\n</div>'


def cta_baixar(app: dict, classe: str = "btn btn-baixar btn-grande") -> str:
    url = url_app(app)
    if eh_direto(app):
        rotulo = "Baixar direto do fabricante"
    else:
        rotulo = {"play": "Abrir na Play Store",
                  "appstore": "Abrir na App Store",
                  "fdroid": "Baixar no F-Droid"}.get(loja_do_link(url),
                                                     "Abrir página oficial de download")
    icone = ICONES["download"]
    return (
        f'<a class="{classe}" href="{esc(url)}" target="_blank" rel="noopener" '
        f'data-app="{esc(app["slug"])}">{icone}<span>{rotulo}</span></a>'
    )


# --------------------------------------------------------------------------- #
# páginas
# --------------------------------------------------------------------------- #
def pagina_index(apps, categorias, contagem, atualizado) -> str:
    destaques = [a for a in apps if a.get("destaque")][:10]
    if len(destaques) < 6:
        destaques = apps[:10]
    cards_dest = "\n".join(
        card_destaque(a, "", categorias[a["categoria"]]["curto"]) for a in destaques
    )
    cats = "\n".join(
        f"""<a class="cat-card" href="categoria/{s}.html">
  <span class="ico">{ICONES.get(c['icone'], ICONES['download'])}</span>
  <b>{esc(c['nome'])}</b>
  <span>{plural(contagem.get(s, 0), 'app', 'apps')}</span>
</a>"""
        for s, c in categorias.items()
    )
    topo_selos = [
        f"<li>{ICONES['escudo']}Só link do site oficial</li>",
        f"<li>{ICONES['cadeado']}Sem instalador empacotado</li>",
        f"<li>{ICONES['check']}Grátis de verdade, sem trial</li>",
        f"<li>{ICONES['relogio']}Links checados em {esc(data_br(atualizado))}</li>",
    ]
    json_ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebSite",
                "@id": URL_BASE + "/#site",
                "url": URL_BASE + "/",
                "name": SITE,
                "description": DESCRICAO_PADRAO,
                "inLanguage": "pt-BR",
                "publisher": {"@id": URL_BASE + "/#editora"},
                "potentialAction": {
                    "@type": "SearchAction",
                    "target": {"@type": "EntryPoint", "urlTemplate": URL_BASE + "/?q={search_term_string}"},
                    "query-input": "required name=search_term_string",
                },
            },
            {
                "@type": "Organization",
                "@id": URL_BASE + "/#editora",
                "name": "Penner Tech",
                "url": URL_BASE + "/",
                "logo": URL_BASE + "/img/og-image.png",
                "sameAs": ["https://loja.pennertech.com.br/"],
            },
            {
                "@type": "ItemList",
                "name": "Aplicativos gratuitos recomendados",
                "numberOfItems": len(apps),
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": i + 1,
                        "name": a["nome"],
                        "url": f"{URL_BASE}/a/{a['slug']}.html",
                    }
                    for i, a in enumerate(apps[:30])
                ],
            },
        ],
    }
    faq_pares = [
        ("Os apps daqui são todos gratuitos mesmo?",
         "Sim. Entram apenas programas com versão gratuita de uso real — open source ou freeware "
         "sem prazo. Quando existe limite (por exemplo, grátis para uso pessoal), isso aparece na "
         "ficha do app antes do botão de download."),
        ("Por que o botão às vezes abre o site do fabricante em vez do arquivo?",
         "Alguns fabricantes não publicam link direto estável: exigem formulário (caso do DaVinci "
         "Resolve) ou entregam o instalador por uma página dinâmica. Nesses casos o botão leva à "
         "página oficial de download, que é o caminho seguro — e não um espelho de terceiro."),
        ("É seguro baixar por aqui?",
         "O Baixa Certa não hospeda nem modifica arquivo nenhum: cada botão aponta para o domínio "
         "do próprio fabricante. Confira sempre o endereço na barra do navegador antes de executar "
         "o instalador, como faria em qualquer download."),
        ("Como vocês escolhem os apps?",
         "Uso, reputação e manutenção ativa. Programas abandonados, com histórico de adware ou de "
         "bundle indesejado ficam de fora. A metodologia completa está na página Como verificamos."),
        ("Faltou um app. Como sugiro?",
         "Manda pela página de contato com o nome do programa e o site oficial. Se ele cumprir os "
         "critérios, entra na próxima atualização do catálogo."),
        ("Por que alguns apps de celular não têm link da Play Store?",
         "Quando o desenvolvedor publica o APK no próprio site (F-Droid, GitHub ou página oficial), "
         "o Baixa Certa prefere esse caminho — é a fonte primária e não passa por loja. Instalar "
         "fora da loja exige liberar 'fontes desconhecidas' no Android, então confira o domínio na "
         "barra do navegador antes de abrir o arquivo."),
        ("Este site é afiliado dos programas?",
         "Não. Não recebo comissão dos fabricantes listados aqui e não há anúncio no site. O Baixa "
         "Certa é um projeto da Penner Tech, que vive da loja de recomendações de hardware — "
         "separada deste portal."),
    ]
    json_ld["@graph"].append({
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": pergunta,
             "acceptedAnswer": {"@type": "Answer", "text": resposta}}
            for pergunta, resposta in faq_pares
        ],
    })
    extra = (
        '<script type="application/ld+json">'
        + json.dumps(json_ld, ensure_ascii=False, separators=(",", ":"))
        + "</script>\n"
    )
    return (
        head(
            f"{SITE} — apps grátis com download oficial direto",
            "Baixe LibreOffice, DaVinci Resolve, VLC, OBS, GIMP e outros apps grátis com link "
            "direto no site oficial do fabricante. Sem cadastro, sem instalador falso.",
            URL_BASE + "/",
            "",
            extra_head=extra,
        )
        + topo("", "inicio")
        + f"""
<main>
  <section class="hero">
    <div class="wrap">
      <p class="kicker"><span class="ponto"></span>Download do site oficial, sem enrolação</p>
      <h1>Baixe <em>certo</em>.<br>O link é do fabricante.</h1>
      <p class="lead">Os {len(apps)} aplicativos gratuitos que eu instalo e recomendo, com
      <strong>link direto para o download oficial</strong>. Nada de instalador empacotado,
      cadastro obrigatório ou botão falso de "Baixar aqui".</p>
      <form class="busca" role="search" onsubmit="return false">
        <label class="busca-in">
          {ICONES['busca']}
          <span class="sr">Buscar aplicativo</span>
          <input id="buscaHero" type="search" placeholder="Busque por app ou tarefa: vídeo, PDF, senha, backup…" autocomplete="off" spellcheck="false">
          <kbd>/</kbd>
        </label>
        <p class="busca-sub">Comece pela busca ou <a href="#categorias">escolha uma categoria</a>.</p>
      </form>
      <ul class="selos">
        {''.join(topo_selos)}
      </ul>
      <div aria-hidden="true">
        <div class="hero-grade">
          {''.join(f'<span class="hero-ico">{icone_app(a)}</span>' for a in destaques[:8])}
        </div>
        <span class="hero-selo">{ICONES['check']} {plural(len(apps), 'app', 'apps')} verificados</span>
      </div>
    </div>
  </section>

  <section class="secao" style="padding-top:26px">
    <div class="wrap">
      <div class="secao-topo">
        <div>
          <span class="olho">Comece por aqui</span>
          <h2>Os que eu instalo em todo PC</h2>
          <p>Escolhas seguras para começar: grandes, gratuitas e mantidas por quem leva o projeto a sério.</p>
        </div>
        <a class="btn btn-ghost btn-mini" href="#catalogo">Ver os {len(apps)} apps</a>
      </div>
      <div class="destaques">
        {cards_dest}
      </div>
    </div>
  </section>

  <section class="secao secao-soft" id="categorias">
    <div class="wrap">
      <div class="secao-topo">
        <div>
          <span class="olho">Catálogo</span>
          <h2>Escolha pelo que você precisa fazer</h2>
          <p>Do escritório ao celular: {len(categorias)} categorias com a mesma regra — link oficial e versão gratuita.</p>
        </div>
      </div>
      <div class="grade-cats">
        {cats}
      </div>
    </div>
  </section>

  <section class="secao" id="catalogo">
    <div class="wrap">
      <div class="secao-topo">
        <div>
          <span class="olho">Todos os apps</span>
          <h2>Catálogo completo</h2>
          <p>Busque pelo nome, pelo que ele faz ou filtre por categoria. {len(apps)} aplicativos verificados.</p>
        </div>
      </div>
      <div class="catalogo-topo">
        <div class="busca" style="margin:0">
          <label class="busca-in">
            {ICONES['busca']}
            <span class="sr">Buscar no catálogo</span>
            <input id="buscaApp" type="search" placeholder="Buscar app, função ou fabricante…" autocomplete="off" spellcheck="false">
          </label>
        </div>
        <span class="contador" id="contador"><b>{len(apps)}</b> de {len(apps)} apps</span>
      </div>
      {chips_categorias(categorias, contagem, "")}
      <div style="height:22px"></div>
      {grade_apps(apps, "", categorias)}
      <div class="vazio oculto" id="vazio">
        <b>Nenhum app com esse filtro</b>
        Tente outra palavra ou <button class="chip" type="button" data-chip data-cat="todos">ver todos</button>
      </div>
    </div>
  </section>

  <section class="secao secao-soft">
    <div class="wrap">
      <div class="secao-topo">
        <div>
          <span class="olho">Como funciona</span>
          <h2>Três cliques e o instalador é o original</h2>
        </div>
      </div>
      <div class="passos">
        <article class="passo">
          <h3>Encontre o app</h3>
          <p>Busque pelo nome ou pela tarefa ("editar vídeo", "ler PDF") e veja a ficha com versão,
          tamanho, licença e sistema compatível.</p>
          <span class="nota">Cada app tem página própria com os detalhes.</span>
        </article>
        <article class="passo">
          <h3>Clique em baixar</h3>
          <p>O botão aponta direto para o instalador no servidor do fabricante — ou para a página
          oficial de download, quando o site exige formulário.</p>
          <span class="nota">Sem redirecionador, sem página de anúncio no meio.</span>
        </article>
        <article class="passo">
          <h3>Confira a origem</h3>
          <p>O arquivo vem do domínio do próprio projeto. Se o navegador mostrar outro domínio,
          não instale: volte e use o link do Baixa Certa.</p>
          <span class="nota">Dica: passe o mouse antes de clicar.</span>
        </article>
      </div>
    </div>
  </section>

  <section class="secao">
    <div class="wrap">
      <div class="secao-topo">
        <div>
          <span class="olho">Por que confiar</span>
          <h2>O que este site não faz</h2>
        </div>
      </div>
      <div class="confianca">
        <article class="conf">
          <span class="ico">{ICONES['link']}</span>
          <h3>Não hospeda arquivo</h3>
          <p>Nada de espelho próprio: o download sai do servidor do fabricante, que assina e
          atualiza o próprio instalador.</p>
        </article>
        <article class="conf">
          <span class="ico">{ICONES['cadeado']}</span>
          <h3>Não empacota instalador</h3>
          <p>Sem "instalador turbinado", sem oferta de programa extra e sem toolbar. É o arquivo
          original, como o desenvolvedor publicou.</p>
        </article>
        <article class="conf">
          <span class="ico">{ICONES['check']}</span>
          <h3>Não chama trial de grátis</h3>
          <p>Se é versão gratuita com limite, está escrito na ficha. Se é open source, tem a
          licença. Se é pago, não entra.</p>
        </article>
        <article class="conf">
          <span class="ico">{ICONES['relogio']}</span>
          <h3>Não deixa link morto</h3>
          <p>Cada link é checado periodicamente no servidor de origem e a data da última
          verificação fica visível.</p>
        </article>
      </div>
    </div>
  </section>

  <section class="secao secao-soft">
    <div class="wrap">
      <div class="secao-topo">
        <div>
          <span class="olho">Dúvidas</span>
          <h2>Perguntas que sempre aparecem</h2>
        </div>
      </div>
      <div class="faq">
        <details>
          <summary>Os apps daqui são todos gratuitos mesmo?</summary>
          <div class="resp">Sim. Entram apenas programas com versão gratuita de uso real — open source
          ou freeware sem prazo. Quando existe limite (por exemplo, "grátis para uso pessoal"), isso
          aparece na ficha do app antes do botão de download.</div>
        </details>
        <details>
          <summary>Por que o botão às vezes abre o site do fabricante em vez do arquivo?</summary>
          <div class="resp">Alguns fabricantes não publicam link direto estável: exigem formulário
          (caso do DaVinci Resolve) ou entregam o instalador por uma página dinâmica. Nesses casos o
          botão leva à página oficial de download, que é o caminho seguro — e não um espelho de
          terceiro.</div>
        </details>
        <details>
          <summary>É seguro baixar por aqui?</summary>
          <div class="resp">O Baixa Certa não hospeda nem modifica arquivo nenhum: cada botão aponta
          para o domínio do próprio fabricante. Confira sempre o endereço na barra do navegador antes
          de executar o instalador, como faria em qualquer download.</div>
        </details>
        <details>
          <summary>Como vocês escolhem os apps?</summary>
          <div class="resp">Uso, reputação e manutenção ativa. Programas abandonados, com histórico de
          adware ou de bundle indesejado ficam de fora. A metodologia completa está em
          <a href="como-verificamos.html">Como verificamos</a>.</div>
        </details>
        <details>
          <summary>Faltou um app. Como sugiro?</summary>
          <div class="resp">Manda pelo <a href="contato.html">contato</a> com o nome do programa e o
          site oficial. Se ele cumprir os critérios, entra na próxima atualização do catálogo.</div>
        </details>
        <details>
          <summary>Por que alguns apps de celular não têm link da Play Store?</summary>
          <div class="resp">Quando o desenvolvedor publica o APK no próprio site (F-Droid, GitHub ou
          página oficial), o Baixa Certa prefere esse caminho — é a fonte primária e não passa por
          loja. Instalar fora da loja exige liberar "fontes desconhecidas" no Android, então confira
          o domínio na barra do navegador antes de abrir o arquivo.</div>
        </details>
        <details>
          <summary>Este site é afiliado dos programas?</summary>
          <div class="resp">Não. Não recebo comissão dos fabricantes listados aqui e não há anúncio
          no site. O Baixa Certa é um projeto da Penner Tech, que vive da loja de recomendações de
          hardware — separada deste portal.</div>
        </details>
      </div>
    </div>
  </section>
</main>
"""
        + rodape("", apps, categorias, atualizado)
    )


def pagina_categoria(slug: str, cat: dict, apps: list[dict], categorias: dict, contagem: dict, atualizado: str) -> str:
    meus = [a for a in apps if a["categoria"] == slug]
    canonical = f"{URL_BASE}/categoria/{slug}.html"
    titulo = f"{cat['nome']} — apps grátis com download oficial | {SITE}"
    json_ld = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": cat["nome"],
        "url": canonical,
        "description": cat["descricao"],
        "inLanguage": "pt-BR",
        "isPartOf": {"@type": "WebSite", "url": URL_BASE + "/", "name": SITE},
        "mainEntity": {
            "@type": "ItemList",
            "numberOfItems": len(meus),
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "name": a["nome"],
                 "url": f"{URL_BASE}/a/{a['slug']}.html"}
                for i, a in enumerate(meus)
            ],
        },
    }
    extra = ('<script type="application/ld+json">'
             + json.dumps(json_ld, ensure_ascii=False, separators=(",", ":")) + "</script>\n")
    dica = ""
    if slug == "celular":
        dica = (
            f'<div class="aviso">{ICONES["info"]}'
            "<div><strong>Antes de instalar no Android:</strong> prefira o link da Play Store. "
            "Quando o app vem como APK oficial (F-Droid, GitHub ou site do desenvolvedor), o "
            "Android avisa sobre fontes desconhecidas — libere a instalação só para esse arquivo, "
            "confira o domínio na barra do navegador e desative a permissão depois.</div></div>"
        )
    return (
        head(titulo, resumo(cat["descricao"] + f" {len(meus)} apps com link oficial."), canonical, "../", extra_head=extra)
        + topo("../", "celular" if slug == "celular" else "")
        + f"""
<main>
  <div class="wrap">
    <nav class="breadcrumb" aria-label="Você está aqui">
      <a href="../index.html">Início</a><span class="sep">/</span>
      <span>{esc(cat['nome'])}</span>
    </nav>
    <section class="hero hero-simples">
      <p class="kicker"><span class="ponto"></span>{plural(len(meus), 'app', 'apps')} · link oficial</p>
      <h1>{esc(cat['nome'])}</h1>
      <p class="lead">{esc(cat['descricao'])}</p>
      <div class="busca" style="margin-top:26px">
        <label class="busca-in">
          {ICONES['busca']}
          <span class="sr">Buscar nesta categoria</span>
          <input id="buscaApp" type="search" placeholder="Buscar em {esc(cat['curto']).lower()}…" autocomplete="off">
        </label>
      </div>
      {chips_categorias(categorias, contagem, '../', slug, modo='links')}
    </section>
    {dica}
    <div style="height:8px"></div>
    {grade_apps(meus, '../', categorias)}
    <div class="vazio oculto" id="vazio">
      <b>Nada encontrado aqui</b>
      Tente outra palavra ou <a href="../index.html#categorias">veja todas as categorias</a>.
    </div>
    <div style="height:40px"></div>
    <div class="aviso">
      {ICONES['info']}
      <div><strong>Link oficial, sempre.</strong> Os botões desta página levam ao servidor do
      fabricante. O Baixa Certa não hospeda, não empacota e não modifica nenhum instalador.
      <a href="../como-verificamos.html">Veja a metodologia.</a></div>
    </div>
    <div style="height:50px"></div>
  </div>
</main>
"""
        + rodape("../", apps, categorias, atualizado)
    )


def pagina_app(app: dict, apps: list[dict], categorias: dict, atualizado: str) -> str:
    cat = categorias[app["categoria"]]
    canonical = f"{URL_BASE}/a/{app['slug']}.html"
    titulo = f"{app['nome']} — download grátis e oficial | {SITE}"
    descricao = app["resumo"][:157]
    plataformas_txt = plataformas(app.get("so") or [])
    campos = [
        ("Versão", app.get("versao")),
        ("Tamanho", app.get("tamanho_arquivo")),
        ("Licença", app.get("licenca")),
        ("Sistema", plataformas_txt),
        ("Arquitetura", app.get("arquitetura")),
        ("Gratuito", app.get("gratis")),
    ]
    dl = "".join(
        f"<dt>{esc(k)}</dt><dd>{esc(v)}</dd>" for k, v in campos if v
    )
    destaques = "".join(
        f"<li>{ICONES['check']}<span>{esc(d)}</span></li>" for d in app.get("destaques", [])
    )
    alternativas = [a for a in apps if a["categoria"] == app["categoria"] and a["slug"] != app["slug"]][:3]
    alts_html = "".join(
        f"""<a class="mini-app" href="{a['slug']}.html">
  <span class="ico">{icone_app(a, '../')}</span>
  <b>{esc(a['nome'])}</b>
</a>""" for a in alternativas
    )
    obs = ""
    if app.get("observacoes"):
        obs = f"""<div class="aviso">{ICONES['info']}
<div><strong>Antes de instalar:</strong> {esc(app['observacoes'])}</div></div>"""
    tags = [
        '<span class="tag tag-ok">Grátis</span>',
        ('<span class="tag tag-link">Link direto</span>' if eh_direto(app) else
         {'play': '<span class="tag tag-link">Play Store</span>',
          'appstore': '<span class="tag tag-link">App Store</span>',
          'fdroid': '<span class="tag tag-link">F-Droid</span>'}.get(
             loja_do_link(url_app(app)), '<span class="tag tag-link">Página oficial</span>')),
        f'<span class="tag">{esc(cat["curto"])}</span>',
        f'<span class="tag">{esc(plataformas_curto(app.get("so") or []))}</span>',
    ]
    url_declarada = app.get("url_download") or url_app(app)
    espelho = ""
    if app.get("url_download_final") and app["url_download_final"] != url_declarada:
        espelho = (" — esse endereço pode redirecionar para um espelho oficial do próprio projeto")
    status = int(app.get("status_http") or 200)
    if 200 <= status < 400:
        alvo = ("O clique baixa o instalador direto do servidor do fabricante."
                if eh_direto(app) else
                "O botão abre a página oficial onde o próprio fabricante entrega o download.")
        verificado = (
            f"Link testado em {esc(data_br(app.get('url_verificado_em') or atualizado))}. {alvo}"
        )
    else:
        verificado = (
            "O site oficial bloqueia checagem automática, então você baixa direto do endereço "
            "publicado pelo fabricante — confira o domínio na barra do navegador."
        )
    json_ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "SoftwareApplication",
                "name": app["nome"],
                "applicationCategory": cat["nome"],
                "applicationSubCategory": "Software gratuito",
                "operatingSystem": plataformas(app.get("so") or []),
                "softwareVersion": app.get("versao") or None,
                "softwareRequirements": app.get("requisitos") or None,
                "downloadUrl": url_app(app),
                "installUrl": url_app(app),
                "url": canonical,
                "description": app["descricao"],
                "publisher": {"@type": "Organization", "name": app["fabricante"]},
                "offers": {"@type": "Offer", "price": "0", "priceCurrency": "BRL"},
                "sameAs": app.get("site_oficial") or None,
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Início", "item": URL_BASE + "/"},
                    {"@type": "ListItem", "position": 2, "name": cat["nome"],
                     "item": f"{URL_BASE}/categoria/{app['categoria']}.html"},
                    {"@type": "ListItem", "position": 3, "name": app["nome"], "item": canonical},
                ],
            },
        ],
    }
    json_ld = json.loads(json.dumps(json_ld, ensure_ascii=False))
    for bloco in json_ld["@graph"]:
        for k in [k for k, v in bloco.items() if v is None]:
            del bloco[k]
    extra = ('<script type="application/ld+json">'
             + json.dumps(json_ld, ensure_ascii=False, separators=(",", ":")) + "</script>\n")
    return (
        head(titulo, descricao, canonical, "../", og_tipo="article", extra_head=extra)
        + topo("../", "")
        + f"""
<main>
  <div class="wrap">
    <nav class="breadcrumb" aria-label="Você está aqui">
      <a href="../index.html">Início</a><span class="sep">/</span>
      <a href="../categoria/{app['categoria']}.html">{esc(cat['nome'])}</a><span class="sep">/</span>
      <span>{esc(app['nome'])}</span>
    </nav>
    <section class="app-hero">
      <div>
        <div class="app-hero-ico">{icone_app(app, '../')}</div>
        <h1>{esc(app['nome'])}</h1>
        <p class="fab">por {esc(app['fabricante'])}</p>
        <p class="res">{esc(app['resumo'])}</p>
        <p class="desc">{esc(app['descricao'])}</p>
        <div class="tags">{''.join(tags)}</div>
      </div>
      <aside class="card-download">
        {cta_baixar(app)}
        <div class="ou">ou</div>
        <a class="oficial" href="{esc(app.get('site_oficial') or url_app(app))}" target="_blank" rel="noopener">
          {ICONES['link']} Site oficial do projeto
        </a>
        <dl>{dl}</dl>
        <div class="verificado">
          {ICONES['escudo']}
          <span>{esc(verificado)}</span>
        </div>
      </aside>
    </section>

    <article class="app-conteudo">
      {f'<h2>Por que vale a pena</h2><ul class="lista-check">{destaques}</ul>' if destaques else ''}

      {f'<h2>Requisitos</h2><div class="req">{ICONES["info"]}<span>{esc(app["requisitos"])}</span></div>' if app.get('requisitos') else ''}

      {obs}

      <h2>De onde vem o download</h2>
      <p>O botão desta página leva a este endereço:</p>
      <code class="url-dl">{esc(url_declarada)}</code>
      <p>{('Esse endereço é do projeto e pode redirecionar para um espelho oficial dele. ' if espelho else '')}O
      domínio é do fabricante, então o instalador não passou por nenhum intermediário. Confira o
      endereço na barra do navegador ao baixar.</p>
    </article>

    {f'''<section style="padding:10px 0 60px">
      <div class="secao-topo">
        <div>
          <span class="olho">Da mesma categoria</span>
          <h2>Alternativas gratuitas</h2>
        </div>
        <a class="btn btn-ghost btn-mini" href="../categoria/{app['categoria']}.html">Ver categoria</a>
      </div>
      <div class="alternativas">{alts_html}</div>
    </section>''' if alternativas else ''}
  </div>
</main>
"""
        + rodape("../", apps, categorias, atualizado)
    )


def pagina_institucional(arquivo: str, titulo: str, desc: str, corpo: str, apps, categorias, atualizado) -> str:
    canonical = f"{URL_BASE}/{arquivo}"
    return (
        head(f"{titulo} | {SITE}", desc, canonical, "")
        + topo("", "")
        + f"""
<main class="wrap">
  <section class="pagina">
    <h1>{esc(titulo)}</h1>
    <p class="lead">{esc(desc)}</p>
    <div class="prosa">
{corpo}
    </div>
    <div style="height:60px"></div>
  </section>
</main>
"""
        + rodape("", apps, categorias, atualizado)
    )


def gera_sitemap(apps, categorias, atualizado) -> str:
    urls = [(URL_BASE + "/", "1.0", "daily")]
    urls += [(f"{URL_BASE}/categoria/{s}.html", "0.9", "weekly") for s in categorias]
    urls += [(f"{URL_BASE}/{p}", "0.5", "monthly") for p in ("sobre.html", "como-verificamos.html", "contato.html")]
    urls += [(f"{URL_BASE}/a/{a['slug']}.html", "0.8", "weekly") for a in apps]
    itens = "\n".join(
        f"  <url><loc>{esc(u)}</loc><lastmod>{atualizado}</lastmod>"
        f"<changefreq>{freq}</changefreq><priority>{prio}</priority></url>"
        for u, prio, freq in urls
    )
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{itens}
</urlset>
"""


# --------------------------------------------------------------------------- #
# montagem
# --------------------------------------------------------------------------- #
def main(argv: list[str]) -> int:
    apps_raw = carrega_json(DADOS / "apps.json")
    categorias = carrega_json(DADOS / "categorias.json")
    apps = apps_raw["apps"]
    atualizado = apps_raw.get("atualizado") or date.today().isoformat()

    # validação
    erros = []
    slugs = set()
    for a in apps:
        for campo in ("slug", "nome", "fabricante", "categoria", "site_oficial", "url_download",
                      "tipo_download", "resumo", "descricao", "destaques", "licenca", "gratis"):
            if not a.get(campo):
                erros.append(f"{a.get('slug', '?')}: campo obrigatório vazio -> {campo}")
        if a.get("categoria") not in categorias:
            erros.append(f"{a['slug']}: categoria inexistente -> {a.get('categoria')}")
        if a["slug"] in slugs:
            erros.append(f"{a['slug']}: slug duplicado")
        slugs.add(a["slug"])
        if a.get("tipo_download") not in ("direto", "pagina"):
            erros.append(f"{a['slug']}: tipo_download inválido -> {a.get('tipo_download')}")
        if not (a.get("url_download") or "").startswith("https://"):
            erros.append(f"{a['slug']}: url_download precisa ser https")
    if erros:
        print("ERROS NOS DADOS:", file=sys.stderr)
        for e in erros:
            print(" -", e, file=sys.stderr)
        if "--check" in argv:
            return 1
    contagem = {s: sum(1 for a in apps if a["categoria"] == s) for s in categorias}
    contagem["todos"] = len(apps)

    # ordena: destaques primeiro, depois nome
    apps_sorted = sorted(apps, key=lambda a: (not a.get("destaque"), a["nome"].lower()))

    (RAIZ / "index.html").write_text(pagina_index(apps_sorted, categorias, contagem, atualizado), encoding="utf-8")
    (RAIZ / "categoria").mkdir(exist_ok=True)
    (RAIZ / "a").mkdir(exist_ok=True)
    for s, c in categorias.items():
        (RAIZ / "categoria" / f"{s}.html").write_text(
            pagina_categoria(s, c, apps_sorted, categorias, contagem, atualizado), encoding="utf-8")
    for a in apps_sorted:
        (RAIZ / "a" / f"{a['slug']}.html").write_text(
            pagina_app(a, apps_sorted, categorias, atualizado), encoding="utf-8")

    (RAIZ / "sitemap.xml").write_text(gera_sitemap(apps_sorted, categorias, atualizado), encoding="utf-8")
    (RAIZ / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n\nSitemap: " + URL_BASE + "/sitemap.xml\n", encoding="utf-8")

    if "--check" in argv:
        print(f"OK: {len(apps)} apps, {len(categorias)} categorias, {len(erros)} erros.")
        return 0 if not erros else 1

    # páginas institucionais
    textos = gerais(apps, categorias)
    for arquivo, (titulo, desc, corpo) in textos.items():
        (RAIZ / arquivo).write_text(
            pagina_institucional(arquivo, titulo, desc, corpo, apps, categorias, atualizado), encoding="utf-8")

    # 404
    (RAIZ / "404.html").write_text(
        head("Página não encontrada | " + SITE,
             "Página não encontrada no Baixa Certa. Volte ao catálogo de apps gratuitos com download oficial.",
             URL_BASE + "/404.html", "")
        + topo("", "")
        + """
<main class="wrap">
  <section class="pagina" style="padding:80px 0">
    <p class="kicker"><span class="ponto"></span>Erro 404</p>
    <h1>Essa página não existe.</h1>
    <p class="lead">O link pode ter mudado de lugar. O catálogo inteiro está na página inicial.</p>
    <p style="margin-top:28px"><a class="btn btn-baixar btn-grande" href="index.html">Ir para o catálogo</a></p>
  </section>
</main>
""",
        encoding="utf-8")
    (RAIZ / ".nojekyll").write_text("", encoding="utf-8")

    print(f"Gerado: index + {len(categorias)} categorias + {len(apps)} apps + {len(textos)} páginas + sitemap")
    return 0 if not erros else 0


def gerais(apps, categorias) -> dict:
    """Conteúdo das páginas institucionais."""
    total = len(apps)
    sobre = f"""
<p>O Baixa Certa é um catálogo de aplicativos gratuitos feito por quem instala software o dia
inteiro. A ideia é simples: <strong>um lugar só com os programas que valem a pena, apontando para o
download no site do próprio fabricante</strong>. Hoje são {total} apps, revisados um por um.</p>

<h2>Por que mais um portal de downloads?</h2>
<p>Porque a experiência de baixar programa no Brasil virou um labirinto. Os primeiros resultados da
busca costumam ser páginas com botão falso, instalador empacotado com cinco programas extras, versão
desatualizada ou arquivo modificado. O Baixa Certa existe para encurtar o caminho: você decide o que
precisa, clica e cai no servidor oficial — sem intermediário.</p>

<h2>Quem faz</h2>
<p>Sou Renato Penner, técnico de TI em Belém/PA e autor do canal e da loja
<a href="https://loja.pennertech.com.br/" target="_blank" rel="noopener">Penner Tech</a>. Testo os
programas que entram aqui antes de indicar, do mesmo jeito que faço com hardware na loja.</p>

<h2>Como o site se mantém</h2>
<div class="card-bloco">
<p><strong>Sem anúncio, sem afiliado, sem cadastro.</strong> O Baixa Certa não recebe comissão de
nenhum fabricante listado e não tem patrocínio. É um projeto do Penner Tech: a receita do canal e da
loja de recomendações de hardware paga a conta, e o portal fica independente.</p>
</div>

<h2>O que você não vai encontrar aqui</h2>
<ul>
  <li>Versão "portátil" modificada, crack, ativador ou serial — nada disso.</li>
  <li>Software pago disfarçado de grátis, trial com data curta ou demo limitada.</li>
  <li>Instalador próprio com programas extras marcados por padrão.</li>
  <li>Link de espelho ou agregador: o botão sempre vai ao domínio do fabricante.</li>
  <li>Cadastro, newsletter obrigatória, contagem regressiva ou botão piscando.</li>
</ul>

<h2>Créditos</h2>
<p>Logos e marcas pertencem aos respectivos donos e aparecem aqui apenas para identificar os
programas. Os ícones de marca são do projeto
<a href="https://simpleicons.org/" target="_blank" rel="noopener">Simple Icons</a> (CC BY 4.0),
renderizados localmente. O site é estático, sem cookies de rastreamento.</p>

<h2>Fale comigo</h2>
<p>Dúvida, correção de link, app que merece entrar: use a página de
<a href="contato.html">contato</a>. Leio tudo.</p>
"""
    metodos = """
<p>Portal de download só presta se o link for confiável. Este é o ritual que cada app passa antes de
aparecer no catálogo — e que se repete nas revisões periódicas.</p>

<h2>1. Só fonte primária</h2>
<p>O link de download tem que sair do domínio do próprio projeto (ex.: <code>videolan.org</code>,
<code>libreoffice.org</code>, <code>obsproject.com</code>). Agregadores, blogs, espelhos e
"repositórios de programas" ficam de fora, mesmo quando aparecem primeiro na busca.</p>

<h2>2. Checagem do link</h2>
<p>Cada botão é testado a partir do servidor: sigo os redirecionamentos e confirmo o código HTTP final
e o tipo do arquivo. Quando o fabricante publica só uma página com formulário (caso do DaVinci
Resolve) ou um redirecionamento dinâmico, o botão aponta para essa página oficial — e não para um
espelho.</p>

<h2>3. Versão e data</h2>
<p>A ficha do app mostra a versão conferida, o tamanho do instalador e a data da última verificação.
O catálogo é regenerado a partir de uma planilha de dados, então essas informações ficam sempre
visíveis e datadas.</p>

<h2>4. Grátis de verdade</h2>
<p>Entra app com versão gratuita de uso real: open source ou freeware sem prazo. Programas com
limite aparecem com a condição escrita na ficha ("grátis para uso pessoal", "versão gratuita com
recursos limitados"). Trial de 30 dias não entra.</p>

<h2>5. Reputação do instalador</h2>
<p>Se o instalador oficial oferece programas extras, telemetria agressiva ou conta obrigatória, isso
vai escrito no aviso da página — antes do botão. É o caso do instalador do FileZilla, que costuma
sugerir software adicional na instalação.</p>

<h2>6. Manutenção ativa</h2>
<p>Projeto abandonado, sem atualização de segurança, não entra. Se um app listado parar de receber
atualizações ou mudar de licença, ele sai do catálogo.</p>

<h2>7. Apps de celular (Android)</h2>
<p>Para celular, o link preferido é o <strong>APK publicado pelo próprio desenvolvedor</strong>
(site oficial, GitHub ou F-Droid); quando o app só existe na loja, usamos a página oficial na
Google Play. Nenhum APK vem de APKPure, APKMirror, Uptodown ou espelho. A ficha do app avisa sobre
anúncios, compras dentro do app, conta obrigatória e permissões sensíveis — e vale a mesma regra:
grátis de verdade, com a condição escrita.</p>

<h2>O que este site não faz</h2>
<div class="card-bloco">
<p><strong>Não hospeda arquivo.</strong> Não existe cópia no nosso servidor, não existe espelho,
não existe "download alternativo". O clique vai direto ao fabricante.</p>
<p><strong>Não modifica instalador.</strong> Nada de repack, nada de "versão otimizada", nada de
instalador silencioso.</p>
<p><strong>Não pede nada em troca.</strong> Sem cadastro, sem e-mail, sem cookie de rastreamento.</p>
</div>

<h2>Encontrou link quebrado?</h2>
<p>Me avise pelo <a href="contato.html">contato</a> com o nome do app. Corrijo e atualizo a data de
verificação. Se o fabricante aposentou a versão gratuita, o app sai do catálogo.</p>
"""
    contato = """
<p>Correção de link, app que deveria estar aqui, dúvida sobre instalação ou aviso de instalador
suspeito: é por aqui.</p>

<h2>E-mail</h2>
<div class="card-bloco">
<p><strong>contato@pennertech.com.br</strong> — respondo em até dois dias úteis.</p>
</div>

<h2>Redes</h2>
<ul>
  <li><a href="https://www.youtube.com/@renatopenner2037" target="_blank" rel="noopener">YouTube — @renatopenner2037</a> (vídeos e comentários)</li>
  <li><a href="https://www.instagram.com/pennerrenato/" target="_blank" rel="noopener">Instagram — @pennerrenato</a></li>
  <li><a href="https://loja.pennertech.com.br/contato.html" target="_blank" rel="noopener">Contato da loja Penner Tech</a></li>
</ul>

<h2>Antes de mandar</h2>
<ul>
  <li><strong>Sugestão de app:</strong> mande o nome e o link do site oficial. Se for pago, não entra.</li>
  <li><strong>Link quebrado:</strong> diga o app e o que aconteceu (erro, página errada, versão antiga).</li>
  <li><strong>Problema com instalador:</strong> mande o nome do arquivo baixado e de onde ele veio.</li>
</ul>

<h2>Aviso</h2>
<div class="card-bloco">
<p>O Baixa Certa não dá suporte técnico individual de instalação e não faz download por você.
Também não indico crack, ativação irregular ou versão modificada — esse tipo de pedido não é
respondido.</p>
</div>
"""
    return {
        "sobre.html": (
            "Sobre o Baixa Certa",
            "Um catálogo independente de apps gratuitos, com download direto no site oficial do fabricante. Conheça o projeto e os critérios.",
            sobre,
        ),
        "como-verificamos.html": (
            "Como verificamos os links e os apps",
            "Metodologia do Baixa Certa: fonte primária, checagem de HTTP, versão datada, licença gratuita e aviso de instalador com ofertas.",
            metodos,
        ),
        "contato.html": (
            "Contato e sugestões de apps",
            "Fale com o Baixa Certa: correção de link, sugestão de app gratuito e aviso de instalador suspeito.",
            contato,
        ),
    }


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
