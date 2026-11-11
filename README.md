# Baixa Certa

Portal de aplicativos gratuitos com **download direto no site oficial do fabricante**.
Projeto da [Penner Tech](https://loja.pennertech.com.br/) — função: `baixa.pennertech.com.br`.

Sem anúncio, sem instalador empacotado, sem cadastro. O site não hospeda arquivo: cada botão leva
ao servidor do próprio desenvolvedor. **113 apps em 11 categorias**, incluindo a aba **Celular**
(Android), com APK oficial ou página na Google Play.

## Como o site é feito

Site **estático** (HTML/CSS/JS puro), hospedado no GitHub Pages. Nada de banco de dados ou servidor:
as páginas são geradas a partir de dois arquivos de dados.

```
dados/categorias.json      # as 11 categorias (nome, descrição, ícone)
dados/apps.json            # o catálogo (versão, links, licença, textos)
pesquisa/links-a.json      # fonte da pesquisa (grupo A — escritório/mídia/imagem/dev)
pesquisa/links-b.json      # fonte da pesquisa (grupo B — utilidades/segurança/internet)
pesquisa/links-c.json      # jogos verificados manualmente (substituem o Drift Hunters)
pesquisa/links-d.json      # desktop do dia a dia (WinRAR, LocalSend, VirtualBox, Calibre…)
pesquisa/links-e.json      # aba Celular (Android — APK oficial ou Google Play)
scripts/consolida.py       # pesquisa -> dados/apps.json (valida e completa)
scripts/verifica_links.py  # checa cada link com curl e atualiza apps.json
scripts/icones.py          # baixa os ícones de marca (Simple Icons) para img/apps/
scripts/arte.py            # favicons + og-image
scripts/gerar.py           # gera index, categorias, páginas de app, sitemap
scripts/checa_site.py      # QA: links internos, H1, JSON-LD, metas, IDs, sitemap
scripts/checa_layout.py    # smoke test: overflow horizontal + screenshots
scripts/ativa_dominio.ps1  # ativa baixa.pennertech.com.br depois do CNAME no Registro.br
css/estilo.css             # todo o estilo (fundo branco)
js/site.js                 # busca e filtro do catálogo
```

Saída do gerador: `index.html`, `categoria/<slug>.html`, `a/<slug>.html`, `sobre.html`,
`como-verificamos.html`, `contato.html`, `404.html`, `sitemap.xml`, `robots.txt`.

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
`licenca`, `gratis`, `requisitos`, `so`.

`so` aceita `windows`, `mac`, `linux`, `android`, `ios`, `web`. App da categoria `celular` precisa
ter `android`.

Opcionais: `versao`, `tamanho_arquivo`, `arquitetura`, `observacoes`, `icone` (slug do
[Simple Icons](https://simpleicons.org)), `destaque` (aparece na home).

## Regras editoriais

1. Só link do domínio do fabricante. Agregador, blog, espelho e repack estão fora.
2. Instalador direto quando existe URL estável; senão, página oficial de download
   (`tipo_download: "pagina"`).
3. Celular: APK oficial (site do desenvolvedor, GitHub ou F-Droid) tem prioridade; quando só existe
   na loja, o botão leva à página do app na Google Play. Nunca APKPure/APKMirror/Uptodown.
4. Grátis de verdade: open source, freeware sem prazo ou versão gratuita com a condição escrita
   na ficha. Trial não entra — **exceção registrada: WinRAR**, que é avaliação sem prazo e continua
   funcionando com aviso (a ficha explica).
5. Instalador com ofertas/telemetria tem aviso na página do app (`observacoes`).
6. Nunca excluir app sem antes checar: se o projeto morreu, sai do catálogo; se só mudou de
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
- **PowerShell 7** entra pelo `.zip` oficial (a versão 7.7.0 não publicou MSI).
