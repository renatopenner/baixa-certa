# Pauta J — apps mais usados: celular, jogos, IA, dev e utilidades (21)

Você está completando o catálogo do **Baixa Certa** (portal da Penner Tech). O site tem apps
gratuitos, de celular e pagos — e está ganhando os **100 aplicativos mais usados do mercado**.
Esta é a última leva (21 apps para fechar os 100).

## Regras (valem para todos)

1. **Fonte oficial somente**: site do fabricante, loja oficial (Google Play do próprio app) ou
   launcher oficial. Nada de Baixaki, Softonic, APKmirror, APKPure, Uptodown, blogs, repacks,
   torrents, espelhos ou marketplaces.
2. Celular → link da **Google Play** (`tipo_download: "pagina"`) ou APK oficial do desenvolvedor
   (`"direto"`). Desktop → instalador oficial quando houver URL estável, senão página oficial.
3. **Verifique com `curl.exe`**:
   ```
   curl.exe -sSIL --max-time 30 -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36" "URL"
   curl.exe -sSL --max-time 45 -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36" -r 0-0 -o NUL -w "%{http_code}|%{content_type}|%{url_effective}" "URL"
   ```
   Play Store pode dar 403/consentimento; registre o status real e explique em `observacoes`.
4. **Nunca invente** URL, versão, tamanho, preço ou licença.
5. Texto em **português do Brasil**, direto.

## Saída

Escreva **somente** `C:\Users\renat\SitesGithub\baixa-certa\pesquisa\links-j.json`
(UTF-8, JSON válido — valide com `python -m json.tool`). Contrato igual à pauta G (campos
`pago`/`preco`/`preco_obs` inclusos).

- `categoria` exatamente uma de: escritorio, multimidia, imagem, dev, utilidades, seguranca,
  internet, backup, ia, jogos, **celular**.
- App de celular: `so: ["android"]` e categoria `celular`.
- `resumo` 100–160 caracteres; `descricao` 250–500; `destaques` 3–4 itens até 60 caracteres.
- Pago → `pago: true` + `preco` + `preco_obs` com data; grátis → `pago: false` e `gratis`.
- `observacoes`: anúncios, compras no app, conta obrigatória, limite de uso.

## Lista (21)

| slug | nome | categoria | obs. |
|---|---|---|---|
| instagram | Instagram | celular | Android/Play Store; grátis com anúncios |
| facebook | Facebook | celular | Android/Play Store; grátis |
| tiktok | TikTok | celular | Android/Play Store; grátis com compras |
| youtube | YouTube | celular | Android/Play Store; grátis com anúncios, Premium pago |
| gmail | Gmail | celular | Android/Play Store; gratuito |
| google-maps | Google Maps | celular | Android/Play Store; gratuito |
| netflix | Netflix | celular | Android/Play Store; assinatura paga (pago=true, preco do plano) |
| battle-net | Battle.net | jogos | launcher oficial Blizzard; gratuito |
| ea-app | EA app | jogos | launcher oficial EA; gratuito |
| ubisoft-connect | Ubisoft Connect | jogos | launcher oficial Ubisoft; gratuito |
| rockstar-launcher | Rockstar Games Launcher | jogos | launcher oficial; gratuito |
| xbox-app | Xbox | jogos | app oficial Xbox para PC; gratuito |
| chatgpt | ChatGPT | ia | app desktop oficial OpenAI; grátis com Plus pago |
| claude | Claude | ia | app desktop oficial Anthropic; grátis com Pro pago |
| cursor | Cursor | dev | editor com IA; plano grátis e Pro pago |
| unity-hub | Unity Hub | dev | Hub oficial gratuito (editor Unity tem planos) |
| unreal-engine | Unreal Engine | dev | Epic Games; gratuito com royalties |
| windows-terminal | Windows Terminal | dev | terminal oficial da Microsoft, gratuito |
| windirstat | WinDirStat | utilidades | analisador de disco open source |
| aomei-backupper | AOMEI Backupper | backup | backup; versão grátis e Pro pago |
| minitool-partition-wizard | MiniTool Partition Wizard | utilidades | partições; grátis e Pro pago |

## Entrega

Responda curto: quantos apps, quantos `direto` x `pagina`, quantos pagos com preço confirmado e o
caminho do arquivo.
