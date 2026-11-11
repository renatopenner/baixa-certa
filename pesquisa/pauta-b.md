# Pauta B — pesquisa de links oficiais (36 apps)

Você está pesquisando dados para o site **Baixa Certa** (portal de apps gratuitos com download
direto do fabricante). O site é estático e cada app virará um card + uma página própria.

## Regras

1. **Fonte oficial somente.** Nada de Baixaki, Softonic, Superdownloads, APKPure, blogs, repacks,
   torrents ou espelhos de terceiros. O link deve sair do site do próprio fabricante/projeto.
2. **Prioridade do link de download:**
   - a) URL direta do instalador no servidor do fabricante (`.exe`, `.msi`, `.dmg`, `.AppImage`),
     de preferência apontando para a **última versão estável**;
   - b) se não existir URL direta estável (exige formulário/JS/token/loja), use a **página oficial
     de download** do fabricante e marque `tipo_download: "pagina"`.
3. **Verifique todo link** com `curl.exe` (no Windows):
   ```
   curl.exe -sSIL --max-time 25 -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "URL"
   curl.exe -sSL --max-time 40 -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" -r 0-0 -o NUL -w "%{http_code}|%{content_type}|%{url_effective}|%{size_download}" "URL"
   ```
   Anote o **último** código HTTP e a URL final. Se der 403 de bot/Cloudflare, tente `--compressed`
   e UA de navegador; se persistir, registre o status obtido e explique em `observacoes`.
4. **Nunca invente URL, versão ou tamanho.** Sem confirmação, deixe `null` e explique.
5. Texto em **português do Brasil**, natural, sem exagero de marketing.

## Saída

Escreva **somente** o arquivo `C:\Users\renat\SitesGithub\baixa-certa\pesquisa\links-b.json`
(UTF-8, JSON válido — valide com `python -m json.tool`). Não mexa em nenhum outro arquivo.

Formato (mesmo contrato da pauta A):

```json
{
  "apps": [
    {
      "slug": "7zip",
      "nome": "7-Zip",
      "fabricante": "Igor Pavlov",
      "categoria": "utilidades",
      "site_oficial": "https://www.7-zip.org/",
      "url_download": "https://www.7-zip.org/a/7z2409-x64.exe",
      "tipo_download": "direto",
      "url_download_final": "https://www.7-zip.org/a/7z2409-x64.exe",
      "status_http": 200,
      "content_type": "application/x-msdownload",
      "tamanho_arquivo": "1,6 MB",
      "versao": "24.09",
      "so": ["windows"],
      "arquitetura": "x86-64",
      "licenca": "LGPL-2.1",
      "gratis": "100% grátis e open source",
      "resumo": "Compactador que abre praticamente qualquer formato, incluindo RAR, e cria arquivos .7z.",
      "descricao": "2 a 3 frases explicando o que é, para quem serve e por que vale a pena.",
      "destaques": ["Abre RAR, ZIP, ISO e mais", "Compressão alta em .7z", "Sem anúncios"],
      "requisitos": "Windows 7 ou mais recente",
      "observacoes": "o instalador oficial não tem ofertas."
    }
  ]
}
```

Campos obrigatórios: `slug`, `nome`, `fabricante`, `categoria`, `site_oficial`, `url_download`,
`tipo_download`, `status_http`, `url_download_final`, `so`, `licenca`, `gratis`, `resumo`,
`descricao`, `destaques`, `requisitos`.

- `categoria` deve ser exatamente uma destas: `utilidades`, `seguranca`, `internet`, `backup`,
  `ia`, `jogos`.
- `so`: subconjunto de `["windows","mac","linux","web"]`; todos têm Windows.
- `gratis`: condição real — "100% grátis e open source", "grátis para uso pessoal",
  "grátis com recursos limitados", "versão gratuita" etc.
- `resumo`: 100–160 caracteres. `descricao`: 250–500 caracteres, sem HTML.
- `destaques`: 3 a 4 itens curtos (até 60 caracteres cada).
- Registre em `observacoes` instaladores com ofertas/ads, telemetria, ou exigência de conta/loja.

## Lista de apps (36)

| slug | nome | categoria | dica |
|---|---|---|---|
| 7zip | 7-Zip | utilidades | download direto em 7-zip.org/a/ |
| everything | Everything | utilidades | busca instantânea de arquivos; voidtools |
| powertoys | Microsoft PowerToys | utilidades | página de releases no GitHub oficial |
| sharex | ShareX | utilidades | captura de tela; instalador no GitHub oficial |
| rufus | Rufus | utilidades | cria pendrive bootável; rufus.ie |
| ventoy | Ventoy | utilidades | multiboot USB; releases no GitHub oficial |
| cpuz | CPU-Z | utilidades | CPUID, download direto .exe |
| hwinfo | HWiNFO | utilidades | diagnóstico de hardware; site oficial |
| crystaldiskinfo | CrystalDiskInfo | utilidades | saúde de disco; site oficial |
| wiztree | WizTree | utilidades | uso de disco; site oficial (grátis para uso pessoal) |
| autohotkey | AutoHotkey | utilidades | automação; autohotkey.com |
| bitwarden | Bitwarden | seguranca | gerenciador de senhas; dowload no GitHub oficial |
| keepassxc | KeePassXC | seguranca | senhas local; keepassxc.org |
| veracrypt | VeraCrypt | seguranca | criptografia de disco; veracrypt.fr |
| protonvpn | Proton VPN | seguranca | VPN com plano grátis; página oficial |
| bleachbit | BleachBit | seguranca | limpeza/privacidade; bleachbit.com |
| tor-browser | Tor Browser | seguranca | navegador anônimo; torproject.org |
| brave | Brave | internet | navegador com bloqueio de anúncios |
| firefox | Mozilla Firefox | internet | instalador direto no site da Mozilla |
| telegram | Telegram Desktop | internet | telegram.org/dl/desktop |
| discord | Discord | internet | página oficial de download |
| whatsapp | WhatsApp para Windows | internet | whatsapp.com/download (instalador .exe) |
| signal | Signal Desktop | internet | signal.org/download |
| thunderbird | Mozilla Thunderbird | internet | e-mail; thunderbird.net |
| qbittorrent | qBittorrent | internet | cliente torrent; foss; site oficial |
| filezilla | FileZilla Client | internet | FTP/SFTP; avise em observacoes sobre ofertas no instalador |
| putty | PuTTY | internet | SSH/telnet; site oficial |
| freefilesync | FreeFileSync | backup | sincronização de pastas; site oficial |
| syncthing | Syncthing | backup | sincronização P2P; syncthing.net |
| duplicati | Duplicati | backup | backup criptografado; duplicati.com |
| ollama | Ollama | ia | LLMs locais; ollama.com/download |
| lmstudio | LM Studio | ia | LLMs locais com interface; página oficial (grátis para uso pessoal) |
| jan | Jan | ia | chat com IA local; jan.ai |
| epic-games | Epic Games Store | jogos | launcher grátis; página oficial |
| steam | Steam | jogos | launcher grátis; store.steampowered.com/about |
| drift-hunters | Drift Hunters | jogos | jogo de drift no navegador, grátis; link oficial do jogo |

## Entrega

Ao terminar, responda com: quantos apps foram preenchidos, quantos links `direto` vs `pagina`,
quais apps ficaram com dados incompletos e o caminho do arquivo escrito.
