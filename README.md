# Baixa Certa

Portal de aplicativos gratuitos com **download direto no site oficial do fabricante**.
Projeto da [Penner Tech](https://loja.pennertech.com.br/) — função: `baixa.pennertech.com.br`.

Sem anúncio, sem instalador empacotado, sem cadastro. O site não hospeda arquivo: cada botão leva
ao servidor do próprio desenvolvedor. **229 apps em 12 categorias**, incluindo a aba **Celular**
(Android, APK oficial ou Google Play), a aba **Pagos** (preço e link de compra do fabricante), a
página **Top 100** (ranking dos mais usados) e o **Top 5 de cada categoria** (melhor para cada
função). O site tem link fixo para a loja Penner Tech no cabeçalho e no rodapé.

## Como o site é feito

Site **estático** (HTML/CSS/JS puro), hospedado no GitHub Pages. Nada de banco de dados ou servidor:
as páginas são geradas a partir dos arquivos de dados abaixo.

```
dados/categorias.json      # as 12 categorias (nome, descrição, ícone)
dados/apps.json            # o catálogo (versão, links, licença, preço, textos)
dados/icones.json          # overrides de ícone (logo ou título da Wikipédia)
dados/melhores.json        # Top 5 de cada categoria: função + porquê
dados/top100.json          # ranking dos 100 mais usados (gerado)
pesquisa/links-a.json      # fonte da pesquisa (grupo A — escritório/mídia/imagem/dev)
pesquisa/links-b.json      # fonte da pesquisa (grupo B — utilidades/segurança/internet)
pesquisa/links-c.json      # jogos verificados manualmente (substituem o Drift Hunters)
pesquisa/links-d.json      # desktop do dia a dia (WinRAR, LocalSend, VirtualBox, Calibre…)
pesquisa/links-e.json      # aba Celular (Android — APK oficial ou Google Play)
pesquisa/links-f.json      # apps pagos (preço oficial conferido no site do fabricante)
pesquisa/links-g..j.json   # os 100 apps mais usados do mercado (navegador, mídia, jogos, dev…)
scripts/consolida.py       # pesquisa -> dados/apps.json (valida e completa)
scripts/verifica_links.py  # checa cada link com curl e atualiza apps.json
scripts/icones.py          # ícones: override -> Simple Icons -> Wikipédia -> favicon oficial
scripts/monta_top100.py    # gera dados/top100.json a partir do ranking curado
scripts/arte.py            # favicons + og-image
scripts/gerar.py           # gera index, categorias, top100, páginas de app, sitemap
scripts/checa_site.py      # QA: links internos, H1, JSON-LD, metas, IDs, sitemap
scripts/checa_layout.py    # smoke test: overflow horizontal + screenshots
scripts/ativa_dominio.ps1  # ativa baixa.pennertech.com.br depois do CNAME no RegistroBr
css/estilo.css             # todo o estilo (tema claro padrão + escuro opcional)
js/site.js                 # busca e filtro do catálogo
js/tema.js                 # alternância de tema (cookie pt_tema)
```

Saída do gerador: `index.html`, `categoria/<slug>.html`, `a/<slug>.html`, `top100.html`,
`sobre.html`, `como-verificamos.html`, `contato.html`, `404.html`, `sitemap.xml`, `robots.txt`.

## Rotina para adicionar ou atualizar um app

```powershell
# 1. editar a pesquisa (pesquisa/links-*.json), ou dados/apps.json direto
python scripts/consolida.py          # valida e monta dados/apps.json
python scripts/verifica_links.py     # testa os links e atualiza status/versão/tamanho
python scripts/icones.py             # baixa ícones de marca que faltarem
python scripts/gerar.py              # regenera as páginas
python scripts/checa_site.py         # QA antes de publicar
git add -A; git commit -m "Atualiza catálogo"; git push
```

O GitHub Pages republica sozinho em ~1 minuto.

### Campos obrigatórios por app

`slug`, `nome`, `fabricante`, `categoria`, `site_oficial`, `url_download`, `tipo_download`
(`direto` ou `pagina`), `resumo` (60–210 caracteres), `descricao` (180+), `destaques` (2–4),
`licenca`, `requisitos`, `so` e — para app grátis — `gratis`.

`so` aceita `windows`, `mac`, `linux`, `android`, `ios`, `web`. App da categoria `celular` precisa
ter `android`. App da categoria `pagos` precisa de `pago: true` e `preco` (texto do plano de entrada,
conferido na página oficial, com a data em `preco_obs`).

Opcionais: `versao`, `tamanho_arquivo`, `arquitetura`, `observacoes`, `pago`, `preco`, `preco_obs`,
`icone` (slug do [Simple Icons](https://simpleicons.org)), `destaque` (aparece na home).

## Regras editoriais

1. Só link do domínio do fabricante. Agregador, blog, espelho e repack estão fora.
2. Instalador direto quando existe URL estável; senão, página oficial de download
   (`tipo_download: "pagina"`).
3. Celular: APK oficial (site do desenvolvedor, GitHub ou F-Droid) tem prioridade; quando só existe
   na loja, o botão leva à página do app na Google Play. Nunca APKPure/APKMirror/Uptodown.
4. Grátis de verdade: open source, freeware sem prazo ou versão gratuita com a condição escrita
   na ficha. Trial não entra — **exceção registrada: WinRAR**, que é avaliação sem prazo e continua
   funcionando com aviso (a ficha explica).
5. Pago entra na categoria **Pagos**, com preço oficial conferido e data. Nunca revendedor de
   licença OEM/"vitalícia", marketplace ou crack.
6. Instalador com ofertas/telemetria tem aviso na página do app (`observacoes`).
7. Nunca excluir app sem antes checar: se o projeto morreu, sai do catálogo; se só mudou de
   versão, atualiza.

## Deploy

Repositório `renatopenner/baixa-certa`, branch `main`, GitHub Pages na raiz.
Enquanto o DNS não é criado, o site responde em `https://pennertech.com.br/baixa-certa/`
(o domínio raiz é do repo `renatopenner.github.io`, então o Pages de projeto herda o domínio).
Domínio final: ver `DOMINIO.md`.

## Decisões editoriais registradas

- **Drift Hunters ficou de fora**: não existe página oficial do desenvolvedor, só portais e
  espelhos — o que fere a regra de link oficial. No lugar entraram jogos livres com site próprio:
  0 A.D., SuperTuxKart e OpenTTD (`pesquisa/links-c.json`).
- **WinRAR entrou a pedido**: é trial sem prazo — depois dos 40 dias continua funcionando com a
  janela de compra. A ficha diz isso com todas as letras e não chama de open source.
- **DaVinci Resolve, Paint.NET, Tor, Telegram, WhatsApp, LM Studio, Proton VPN, FileZilla,
  CrystalDiskInfo, MusicBee, GPU-Z, CrystalDiskMark e GOG Galaxy** usam a página oficial de
  download (`tipo_download: "pagina"`), porque o fabricante não publica URL direta estável.
- **FileZilla** tem aviso de ofertas no instalador; **CrystalDiskMark** e **CrystalDiskInfo** usam
  redirecionador com ads; **Inkscape** e **WhatsApp** bloqueiam verificação automática (403/400) e
  isso está escrito na ficha do app.
- **Affinity Photo e Affinity Designer saíram da categoria Pagos**: a Canva tornou o Affinity
  gratuito em outubro de 2025. Agora entram como gratuitos, com aviso na ficha.
- **Pagos**: preço conferido na página oficial do fabricante em 11/11/2026 (Adobe, Autodesk,
  Microsoft, Corel, SketchUp, IDM, Filmora, Camtasia, NordVPN, Malwarebytes, Revo). Adobe e Autodesk
  bloqueiam `curl`, então o status é 403 de propósito e o preço veio da página renderizada.
- **PowerShell 7** entra pelo `.zip` oficial (a versão 7.7.0 não publicou MSI).

## Atualização 12/11/2026 — 229 apps

- **+100 apps mais usados do mercado** (grupos `links-g` a `links-j`): Chrome, Edge, Opera,
  Vivaldi, Zoom, Teams, Slack, Spotify, Deezer, Notion, Trello, Canva, Figma, CapCut, Plex,
  PotPlayer, MPC-HC, IrfanView, Illustrator, InDesign, After Effects, Audition, Animate, Revit,
  SOLIDWORKS, WPS, Roblox, Minecraft, Valorant, LoL, Docker, Visual Studio, IntelliJ, PyCharm,
  Android Studio, Node, JDK, Postman, XAMPP, MySQL Workbench, SSMS, pgAdmin, Sourcetree, WinSCP,
  Wireshark, 1Password, ExpressVPN, Avast, Kaspersky, Bitdefender, CCleaner, Driver Booster,
  AnyDesk, MSI Afterburner, HWMonitor, Instagram, Facebook, TikTok, YouTube, Gmail, Maps, Netflix,
  Battle.net, EA app, Ubisoft Connect, Rockstar, Xbox, ChatGPT, Claude, Cursor, Unity Hub,
  Unreal Engine, Windows Terminal, WinDirStat, AOMEI Backupper, MiniTool.
- **Página `top100.html`**: ranking dos 100 mais usados (gratuitos e pagos), com ícone, categoria,
  preço/licença e link para a ficha. Gerado por `scripts/monta_top100.py` a partir de ranking curado.
- **Top 5 de cada categoria** (`dados/melhores.json`): o melhor para cada função, com uma frase
  explicando o porquê. Aparece no topo da página da categoria e no bloco “O melhor de cada
  categoria” da home.
- **Ícones oficiais**: `scripts/icones.py` agora tenta override manual → Simple Icons → imagem da
  Wikipédia (logo do produto) → favicon oficial. Resultado: 228 de 229 apps com logo real (só o
  Ditto ficou com monograma).
- **Loja Penner Tech** no cabeçalho (botão com o monograma R) e no rodapé, apontando para
  `https://loja.pennertech.com.br/`.
- **Categoria Pagos virou virtual**: todo app com `pago: true` aparece nela, venha da categoria que
  vier; a categoria funcional (imagem, multimídia, dev…) continua sendo a do app.
- Pipeline de checagem de links migrou de `curl` para `urllib` (timeouts confiáveis no Windows);
  `scripts/verifica_links.py` segue atualizando status, redirect e tamanho.
