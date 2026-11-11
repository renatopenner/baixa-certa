# Pauta D â€” apps de desktop para o dia a dia (24 apps)

VocÃª estÃ¡ completando o catÃ¡logo do site **Baixa Certa** (portal da Penner Tech de apps gratuitos
com download oficial). O site Ã© gerado a partir de JSON; cada app vira card + pÃ¡gina prÃ³pria.

## Regras (valem para todos)

1. **Fonte oficial somente.** Nada de Baixaki, Softonic, Superdownloads, blogs, repacks, torrents ou
   espelhos de terceiros. O link sai do site do fabricante/projeto ou, quando o fabricante distribui
   pelo GitHub, do release oficial do prÃ³prio projeto.
2. **Prioridade do link:**
   - a) URL direta do instalador (`.exe`, `.msi`) na Ãºltima versÃ£o estÃ¡vel;
   - b) se nÃ£o houver URL direta estÃ¡vel (formulÃ¡rio/JS/token/loja), use a **pÃ¡gina oficial de
     download** e marque `tipo_download: "pagina"`.
3. **Verifique todo link com `curl.exe`** (Windows):
   ```
   curl.exe -sSIL --max-time 30 -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36" "URL"
   curl.exe -sSL --max-time 45 -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36" -r 0-0 -o NUL -w "%{http_code}|%{content_type}|%{url_effective}" "URL"
   ```
   Anote o Ãºltimo status HTTP, o content-type e a URL final. GitHub entrega asset por URL assinada
   temporÃ¡ria: grave em `url_download_final` a URL versionada estÃ¡vel (nÃ£o a assinada).
4. **Nunca invente** URL, versÃ£o, tamanho ou licenÃ§a. Sem confirmaÃ§Ã£o â†’ `null` + explicaÃ§Ã£o em
   `observacoes`.
5. Texto em **portuguÃªs do Brasil**, natural e direto.

## SaÃ­da

Escreva **somente** `C:\Users\renat\SitesGithub\baixa-certa\pesquisa\links-d.json` (UTF-8, JSON
vÃ¡lido, valide com `python -m json.tool`). NÃ£o altere nenhum outro arquivo.

Formato:

```json
{
  "verificado_em": "2026-11-11",
  "apps": [
    {
      "slug": "winrar",
      "nome": "WinRAR",
      "fabricante": "RARLAB",
      "categoria": "utilidades",
      "site_oficial": "https://www.win-rar.com/",
      "url_download": "https://...",
      "tipo_download": "direto",
      "url_download_final": "https://...",
      "status_http": 200,
      "content_type": "application/x-msdownload",
      "tamanho_arquivo": "3,9 MB",
      "versao": "7.20",
      "so": ["windows"],
      "arquitetura": "x86-64",
      "licenca": "ProprietÃ¡rio (avaliaÃ§Ã£o)",
      "gratis": "GrÃ¡tis na prÃ¡tica: avaliaÃ§Ã£o sem prazo, com aviso ao abrir",
      "resumo": "Compacta e descompacta RAR, ZIP e vÃ¡rios formatos, com recuperaÃ§Ã£o de arquivo corrompido.",
      "descricao": "2 a 3 frases: o que Ã©, para quem serve, por que vale a pena.",
      "destaques": ["...", "...", "..."],
      "requisitos": "Windows 7 ou mais recente",
      "observacoes": "ExplicaÃ§Ã£o de licenÃ§a/instalador/ofertas quando houver."
    }
  ]
}
```

Campos obrigatÃ³rios: `slug, nome, fabricante, categoria, site_oficial, url_download, tipo_download,
status_http, url_download_final, so, licenca, gratis, resumo, descricao, destaques, requisitos`.

- `categoria` Ã© exatamente uma de: `escritorio`, `multimidia`, `imagem`, `dev`, `utilidades`,
  `seguranca`, `internet`, `jogos`.
- `resumo` 100â€“160 caracteres; `descricao` 250â€“500; `destaques` 3â€“4 itens de atÃ© 60 caracteres.
- Registrar em `observacoes` instalador com ofertas/telemetria, exigÃªncia de conta, licenÃ§a
  restrita a uso pessoal, dependÃªncia de runtime etc.

## Lista (23)

| slug | nome | categoria | observaÃ§Ã£o para a pesquisa |
|---|---|---|---|
| winrar | WinRAR | utilidades | rarlab.com/win-rar.com. Ã‰ **trial sem prazo** que continua funcionando com aviso ("comprar licenÃ§a") â€” registre isso com honestidade em `gratis` e `observacoes`; NÃƒO chamar de open source |
| localsend | LocalSend | utilidades | localsend.org / GitHub localsend/localsend; envia arquivo PCâ†”celular na mesma rede |
| rustdesk | RustDesk | internet | rustdesk.com; acesso remoto open source, cliente Windows |
| balenaetcher | balenaEtcher | utilidades | etcher.balena.io; grava ISO em pendrive/SD |
| virtualbox | Oracle VirtualBox | utilidades | virtualbox.org; mÃ¡quina virtual gratuita (Extension Pack Ã© separado) |
| calibre | Calibre | escritorio | calibre-ebook.com; gerenciador/conversor de ebooks |
| anki | Anki | escritorio | apps.ankiweb.net; flashcards com repetiÃ§Ã£o espaÃ§ada |
| winmerge | WinMerge | dev | winmerge.org; compara arquivos e pastas |
| bruno | Bruno | dev | usebruno.com / GitHub; cliente de API open source (alternativa ao Postman) |
| powershell | PowerShell 7 | dev | GitHub PowerShell/PowerShell releases (MSI oficial da Microsoft) |
| ditto | Ditto | utilidades | ditto-cp.sourceforge.io; histÃ³rico de Ã¡rea de transferÃªncia open source |
| quicklook | QuickLook | utilidades | GitHub inulute/QuickLook ou projeto oficial; prÃ©-visualizaÃ§Ã£o estilo macOS |
| imageglass | ImageGlass | imagem | imageglass.org; visualizador de imagens leve |
| musicbee | MusicBee | multimidia | getmusicbee.com; player de mÃºsica para Windows |
| kodi | Kodi | multimidia | kodi.tv; central de mÃ­dia |
| jellyfin-media-player | Jellyfin Media Player | multimidia | GitHub jellyfin/jellyfin-media-player; cliente desktop do Jellyfin |
| gpuz | GPU-Z | utilidades | techpowerup.com/gpuz; informaÃ§Ãµes da placa de vÃ­deo |
| crystaldiskmark | CrystalDiskMark | utilidades | crystalmark.info; mede velocidade de disco (pÃ¡gina oficial, tem ads na pÃ¡gina) |
| treesize | TreeSize Free | utilidades | jam-software.com/treesize_free; mostra o que ocupa espaÃ§o (grÃ¡tis para uso pessoal) |
| cryptomator | Cryptomator | seguranca | cryptomator.org; criptografa arquivos na nuvem |
| angryip | Angry IP Scanner | internet | angryip.org; varredura de rede local open source |
| gog-galaxy | GOG Galaxy | jogos | gog.com/galaxy; launcher gratuito da GOG |
| memtest86 | MemTest86 | utilidades | memtest86.com; teste de memÃ³ria RAM (ediÃ§Ã£o gratuita), imagem para pendrive |

## Entrega

Responda curto: quantos apps, quantos `direto` vs `pagina`, quais ficaram com dado incompleto e o
caminho do arquivo.

