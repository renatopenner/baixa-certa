# Pauta G — apps mais usados: navegadores, comunicação, produtividade e nuvem (26)

Você está completando o catálogo do **Baixa Certa** (portal da Penner Tech). O site agora tem apps
gratuitos, de celular e **pagos** — e está ganhando os programas mais usados do mercado.

## Regras (valem para todos)

1. **Fonte oficial somente**: site do fabricante ou página oficial de download/preços. Nada de
   Baixaki, Softonic, Superdownloads, blogs, repacks, torrents, espelhos ou marketplaces.
2. Link preferencial: instalador direto quando o fabricante publica URL estável; senão, página
   oficial de download → `tipo_download: "pagina"`.
3. **Verifique com `curl.exe`** (Windows):
   ```
   curl.exe -sSIL --max-time 30 -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36" "URL"
   curl.exe -sSL --max-time 45 -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36" -r 0-0 -o NUL -w "%{http_code}|%{content_type}|%{url_effective}" "URL"
   ```
   Se o site bloquear robô (403/429), registre o status real e explique em `observacoes`.
4. **Nunca invente** URL, versão, tamanho, preço ou licença.
5. Texto em **português do Brasil**, direto.

## Saída

Escreva **somente** `C:\Users\renat\SitesGithub\baixa-certa\pesquisa\links-g.json`
(UTF-8, JSON válido — valide com `python -m json.tool`).

```json
{
  "verificado_em": "2026-11-12",
  "apps": [
    {
      "slug": "chrome",
      "nome": "Google Chrome",
      "fabricante": "Google",
      "categoria": "internet",
      "pago": false,
      "preco": null,
      "preco_obs": null,
      "site_oficial": "https://www.google.com/chrome/",
      "url_download": "https://www.google.com/chrome/",
      "tipo_download": "pagina",
      "url_download_final": "https://www.google.com/chrome/",
      "status_http": 200,
      "content_type": "text/html",
      "tamanho_arquivo": null,
      "versao": null,
      "so": ["windows", "mac", "linux", "android", "ios"],
      "arquitetura": null,
      "licenca": "Proprietário · gratuito",
      "gratis": "100% grátis; o Chrome é fechado e coleta dados de uso",
      "resumo": "Navegador mais usado do mundo, rápido e integrado à conta Google.",
      "descricao": "2 a 3 frases: o que é, para quem serve, por que é o mais usado.",
      "destaques": ["Sincroniza com a conta Google", "Catálogo enorme de extensões", "Atualiza sozinho"],
      "requisitos": "Windows 10/11, macOS 11+ ou Linux",
      "observacoes": null
    }
  ]
}
```

Obrigatórios: `slug, nome, fabricante, categoria, site_oficial, url_download, tipo_download,
status_http, so, licenca, resumo, descricao, destaques, requisitos`.
Grátis → `pago: false`, `gratis` preenchido, `preco: null`. Pago/freemium → `pago: true` (se cobra)
com `preco` (plano de entrada, conferido na página oficial) e `preco_obs` com a data; freemium com
plano grátis real pode ser `pago: false` e explicar o limite em `gratis`/`observacoes`.

- `categoria` exatamente uma de: escritorio, multimidia, imagem, dev, utilidades, seguranca,
  internet, backup, ia, jogos (a categoria `pagos` é virtual — não usar).
- `resumo` 100–160 caracteres; `descricao` 250–500; `destaques` 3–4 itens de até 60 caracteres.
- `observacoes`: anúncios, telemetria, conta obrigatória, limite do plano grátis.

## Lista (26)

| slug | nome | categoria | obs. |
|---|---|---|---|
| chrome | Google Chrome | internet | navegador mais usado; página oficial de download |
| microsoft-edge | Microsoft Edge | internet | navegador padrão do Windows |
| opera | Opera | internet | navegador com VPN grátis embutida |
| vivaldi | Vivaldi | internet | navegador altamente configurável |
| zoom | Zoom Workplace | internet | reuniões; plano grátis com limite de 40 min |
| microsoft-teams | Microsoft Teams | internet | reuniões/trabalho; versão gratuita e planos |
| slack | Slack | internet | comunicação de equipes; free com histórico limitado |
| messenger | Messenger | internet | mensageiro do Facebook; app Windows e celular |
| viber | Viber | internet | mensageiro; chamadas grátis |
| line | LINE | internet | mensageiro muito usado na Ásia |
| webex | Cisco Webex | internet | reuniões corporativas |
| teamviewer | TeamViewer | internet | acesso remoto; grátis para uso pessoal |
| spotify | Spotify | multimidia | streaming de música; free com anúncios |
| deezer | Deezer | multimidia | streaming de música; free com anúncios |
| kmplayer | KMPlayer | multimidia | player de vídeo; versão gratuita |
| nextcloud-desktop | Nextcloud Desktop | backup | sincroniza arquivos com seu servidor Nextcloud |
| google-drive | Google Drive | backup | 15 GB grátis; planos pagos |
| onedrive | Microsoft OneDrive | backup | 5 GB grátis; integrado ao Windows/Office |
| dropbox | Dropbox | backup | 2 GB grátis; planos pagos |
| mega | MEGA | backup | 20 GB grátis com criptografia |
| notion | Notion | escritorio | notas e projetos; grátis para uso pessoal |
| trello | Trello | escritorio | quadros kanban; plano grátis |
| evernote | Evernote | escritorio | notas; plano grátis limitado |
| todoist | Todoist | escritorio | tarefas; plano grátis |
| canva | Canva | imagem | design fácil; grátis com recursos Pro pagos |
| figma | Figma | imagem | design de interface; grátis para uso pessoal |

## Entrega

Responda curto: quantos apps, quantos `direto` x `pagina`, quantos pagos com preço confirmado e o
caminho do arquivo.
