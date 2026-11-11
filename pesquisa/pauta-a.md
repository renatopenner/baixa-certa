# Pauta A — pesquisa de links oficiais (28 apps)

Você está pesquisando dados para o site **Baixa Certa** (portal de apps gratuitos com download
direto do fabricante). O site é estático e cada app virará um card + uma página própria.

## Regras

1. **Fonte oficial somente.** Nada de Baixaki, Softonic, Superdownloads, APKPure, blogs, repacks,
   torrents ou espelhos de terceiros. O link deve sair do site do próprio fabricante/projeto.
2. **Prioridade do link de download:**
   - a) URL direta do instalador no servidor do fabricante (`.exe`, `.msi`, `.dmg`, `.AppImage`),
     de preferência apontando para a **última versão estável**;
   - b) se não existir URL direta estável (exige formulário/JS/token), use a **página oficial de
     download** do fabricante e marque `tipo_download: "pagina"`.
3. **Verifique todo link** com `curl.exe` (no Windows). Exemplo:
   ```
   curl.exe -sSIL --max-time 25 -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "URL"
   ```
   Anote o **último** código HTTP e a URL final (`url_effective`). Para confirmar que é arquivo:
   ```
   curl.exe -sSL --max-time 40 -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" -r 0-0 -o NUL -w "%{http_code}|%{content_type}|%{url_effective}|%{size_download}" "URL"
   ```
   Use `-r 0-0` (primeiro byte) para não baixar o instalador inteiro.
   Se receber 403 para bot (Cloudflare), tente com `--compressed` e UA de navegador; se continuar,
   marque `status_http` com o valor obtido e explique em `observacoes`.
4. **Nunca invente URL, versão ou tamanho.** Se não conseguir confirmar, deixe `null` e explique.
5. Texto em **português do Brasil**, natural, sem exagero de marketing.

## Saída

Escreva **somente** o arquivo `C:\Users\renat\SitesGithub\baixa-certa\pesquisa\links-a.json`
(UTF-8, JSON válido — valide com `python -m json.tool`). Não mexa em nenhum outro arquivo.

Formato:

```json
{
  "apps": [
    {
      "slug": "libreoffice",
      "nome": "LibreOffice",
      "fabricante": "The Document Foundation",
      "categoria": "escritorio",
      "site_oficial": "https://pt-br.libreoffice.org/",
      "url_download": "https://...",
      "tipo_download": "direto",
      "url_download_final": "https://...",
      "status_http": 200,
      "content_type": "application/x-msdownload",
      "tamanho_arquivo": "359 MB",
      "versao": "25.8.2",
      "so": ["windows", "mac", "linux"],
      "arquitetura": "x86-64",
      "licenca": "MPL-2.0",
      "gratis": "100% grátis e open source",
      "resumo": "Suíte de escritório completa e gratuita, compatível com Word, Excel e PowerPoint.",
      "descricao": "2 a 3 frases explicando o que é, para quem serve e por que vale a pena.",
      "destaques": ["Compatible com .docx/.xlsx/.pptx", "Writer, Calc, Impress, Draw", "Sem limite de uso ou assinatura"],
      "requisitos": "Windows 10/11 64-bit, 4 GB de RAM, ~1,5 GB de disco",
      "observacoes": "Instalador MSI disponível; a página pt-BR redireciona para a versão mais recente."
    }
  ]
}
```

Campos obrigatórios: `slug`, `nome`, `fabricante`, `categoria`, `site_oficial`, `url_download`,
`tipo_download`, `status_http`, `url_download_final`, `so`, `licenca`, `gratis`, `resumo`,
`descricao`, `destaques`, `requisitos`. Os demais podem ser `null`.

- `categoria` deve ser exatamente uma destas: `escritorio`, `multimidia`, `imagem`, `dev`.
- `so`: subconjunto de `["windows","mac","linux","web"]`; aqui todos têm Windows.
- `gratis`: diga a condição real, ex.: "100% grátis e open source", "grátis para uso pessoal",
  "grátis com recursos limitados", "grátis para sempre (versão gratuita)".
- `resumo`: 100–160 caracteres, sem ponto final duplicado.
- `descricao`: 250–500 caracteres, sem HTML.
- `destaques`: 3 a 4 itens curtos (até 60 caracteres cada).
- Se o app tiver instalador com ofertas/ads (ex.: FileZilla) ou telemetria, registre em `observacoes`.

## Lista de apps (28)

| slug | nome | categoria | dica |
|---|---|---|---|
| libreoffice | LibreOffice | escritorio | URL direta por versão em download.documentfoundation.org; prefira a página pt-BR se a direta for instável |
| onlyoffice | ONLYOFFICE Desktop Editors | escritorio | desktop editors, instalador .exe/.msi oficial |
| sumatrapdf | SumatraPDF | escritorio | leitor de PDF leve; releases no GitHub oficial |
| pdf24 | PDF24 Creator | escritorio | criador/editor de PDF; download direto no site oficial |
| joplin | Joplin | escritorio | notas markdown; instalador no GitHub oficial |
| obsidian | Obsidian | escritorio | notes; versão gratuita para uso pessoal |
| zotero | Zotero | escritorio | gerenciador de referências acadêmicas |
| vlc | VLC media player | multimidia | get.videolan.org tem pasta `last/win64` |
| davinci-resolve | DaVinci Resolve | multimidia | Blackmagic exige formulário — provavelmente `tipo_download: "pagina"` |
| shotcut | Shotcut | multimidia | editor de vídeo; instalador no site oficial/GitHub |
| kdenlive | Kdenlive | multimidia | editor de vídeo do KDE; binário Windows no site oficial |
| handbrake | HandBrake | multimidia | conversor de vídeo; download direto no site oficial |
| obs-studio | OBS Studio | multimidia | gravação/streaming; release no GitHub |
| audacity | Audacity | multimidia | editor de áudio; instalador no site oficial |
| foobar2000 | foobar2000 | multimidia | player de áudio; download no site oficial |
| gimp | GIMP | imagem | download.gimp.org tem pastas por versão |
| krita | Krita | imagem | pintura digital; instalador no site oficial |
| inkscape | Inkscape | imagem | vetorial; instalador no site oficial |
| paintnet | Paint.NET | imagem | editor de imagem para Windows; download oficial é página com mirrors |
| darktable | darktable | imagem | revelação RAW; instalador no site oficial |
| blender | Blender | imagem | 3D; download.blender.org/release com versão |
| freecad | FreeCAD | imagem | CAD 3D; releases no GitHub oficial |
| vscode | Visual Studio Code | dev | code.visualstudio.com, link direto `stable/win32-x64` |
| git | Git for Windows | dev | git-scm.com, instalador direto no GitHub oficial |
| notepadpp | Notepad++ | dev | editor de texto; download no site oficial |
| python | Python | dev | python.org, instalador `python-3.x.y-amd64.exe` |
| dbeaver | DBeaver Community | dev | cliente SQL; instalador no GitHub oficial |
| github-desktop | GitHub Desktop | dev | cliente git; download no site oficial |

## Entrega

Ao terminar, responda com: quantos apps foram preenchidos, quantos links `direto` vs `pagina`,
quais apps ficaram com dados incompletos e o caminho do arquivo escrito.
