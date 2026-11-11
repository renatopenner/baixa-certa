# Baixa Certa

Portal de aplicativos gratuitos com **download direto no site oficial do fabricante**.
Projeto da [Penner Tech](https://loja.pennertech.com.br/) — função: `baixa.pennertech.com.br`.

Sem anúncio, sem instalador empacotado, sem cadastro. O site não hospeda arquivo: cada botão leva
ao servidor do próprio desenvolvedor.

## Como o site é feito

Site **estático** (HTML/CSS/JS puro), hospedado no GitHub Pages. Nada de banco de dados ou servidor:
as páginas são geradas a partir de dois arquivos de dados.

```
dados/categorias.json      # as 10 categorias (nome, descrição, ícone)
dados/apps.json            # o catálogo (versão, links, licença, textos)
pesquisa/links-a.json      # fonte da pesquisa (grupo A)
pesquisa/links-b.json      # fonte da pesquisa (grupo B)
scripts/consolida.py       # pesquisa -> dados/apps.json (valida e completa)
scripts/verifica_links.py  # checa cada link com curl e atualiza apps.json
scripts/icones.py          # baixa os ícones de marca (Simple Icons) para img/apps/
scripts/arte.py            # favicons + og-image
scripts/gerar.py           # gera index, categorias, páginas de app, sitemap
scripts/checa_layout.py    # smoke test: overflow horizontal + screenshots
css/estilo.css             # todo o estilo (fundo branco)
js/site.js                 # busca e filtro do catálogo
```

Saída do gerador: `index.html`, `categoria/<slug>.html`, `a/<slug>.html`, `sobre.html`,
`como-verificamos.html`, `contato.html`, `404.html`, `sitemap.xml`, `robots.txt`.

## Rotina para adicionar ou atualizar um app

```powershell
# 1. editar a pesquisa (pesquisa/links-a.json ou links-b.json), ou dados/apps.json direto
python scripts/consolida.py          # valida e monta dados/apps.json
python scripts/verifica_links.py     # testa os links e atualiza status/versão/tamanho
python scripts/icones.py             # baixa ícones de marca que faltarem
python scripts/gerar.py              # regenera as páginas
git add -A; git commit -m "Atualiza catálogo"; git push
```

O GitHub Pages republica sozinho em ~1 minuto.

### Campos obrigatórios por app

`slug`, `nome`, `fabricante`, `categoria`, `site_oficial`, `url_download`, `tipo_download`
(`direto` ou `pagina`), `resumo` (60–210 caracteres), `descricao` (180+), `destaques` (2–4),
`licenca`, `gratis`, `requisitos`, `so`.

Opcionais: `versao`, `tamanho_arquivo`, `arquitetura`, `observacoes`, `icone` (slug do
[Simple Icons](https://simpleicons.org)), `destaque` (aparece na home).

## Regras editoriais

1. Só link do domínio do fabricante. Agregador, blog, espelho e repack estão fora.
2. O botão aponta para o instalador direto quando existe URL estável; senão, para a página
   oficial de download (marcada como `tipo_download: "pagina"`).
3. Grátis de verdade: open source ou freeware sem prazo. Trial não entra.
4. Instalador com ofertas/telemetria tem aviso na página do app (`observacoes`).
5. Nunca excluir app sem antes checar: se o projeto morreu, sai do catálogo; se só mudou de
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
- **DaVinci Resolve, Paint.NET, Tor, Telegram, WhatsApp, LM Studio, Proton VPN, FileZilla e
  CrystalDiskInfo** usam a página oficial de download (`tipo_download: "pagina"`), porque o
  fabricante não publica instalador por URL direta estável.
- **FileZilla** tem aviso de ofertas no instalador; **CrystalDiskInfo** usa redirecionador com ads;
  **Inkscape** e **WhatsApp** bloqueiam verificação automática (403/400) e isso está escrito na
  ficha do app.
