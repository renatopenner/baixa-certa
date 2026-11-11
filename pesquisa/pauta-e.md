# Pauta E — aba Celular: apps gratuitos para Android (24 apps)

Você está criando a nova categoria **Celular** do site **Baixa Certa** (portal da Penner Tech de
apps gratuitos com download oficial). O público é Android (o dono do site usa Galaxy S23 Ultra).

## Regras (valem para todos)

1. **Fonte oficial somente.** Use, por ordem de preferência:
   - a) **URL direta do APK** publicada pelo próprio desenvolvedor (site oficial, GitHub releases,
     F-Droid, releases de projeto) → `tipo_download: "direto"`;
   - b) **página oficial do app na Google Play** (`https://play.google.com/store/apps/details?id=...`)
     → `tipo_download: "pagina"`;
   - c) se o desenvolvedor indica outro caminho oficial (ex.: página própria com APK), use esse.
   **Nunca** use APKPure, APKMirror, Uptodown, Baixaki, Softonic, blogs ou espelhos.
2. **Verifique com `curl.exe`** (Windows):
   ```
   curl.exe -sSIL --max-time 30 -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36" "URL"
   curl.exe -sSL --max-time 45 -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36" -r 0-0 -o NUL -w "%{http_code}|%{content_type}|%{url_effective}" "URL"
   ```
   A Play Store costuma bloquear `curl` com 403 ou devolver HTML de consentimento — registre o status
   obtido e explique em `observacoes`. Para APK, confirme content-type de pacote/octet-stream.
3. **Nunca invente** URL, versão, tamanho de APK, licença ou nota. Sem confirmação → `null`.
4. Texto em **português do Brasil**, natural e direto, sem marketing exagerado.

## Saída

Escreva **somente** `C:\Users\renat\SitesGithub\baixa-certa\pesquisa\links-e.json` (UTF-8, JSON
válido, valide com `python -m json.tool`). Não altere nenhum outro arquivo.

Formato:

```json
{
  "verificado_em": "2026-11-11",
  "apps": [
    {
      "slug": "whatsapp-messenger",
      "nome": "WhatsApp Messenger",
      "fabricante": "Meta",
      "categoria": "celular",
      "site_oficial": "https://www.whatsapp.com/android/",
      "url_download": "https://play.google.com/store/apps/details?id=com.whatsapp",
      "tipo_download": "pagina",
      "url_download_final": "https://play.google.com/store/apps/details?id=com.whatsapp",
      "status_http": 200,
      "content_type": "text/html",
      "tamanho_arquivo": null,
      "versao": null,
      "so": ["android"],
      "arquitetura": null,
      "licenca": "Proprietário · gratuito",
      "gratis": "100% grátis, sem anúncio no app",
      "resumo": "Mensageiro mais usado do mundo, com chamadas, grupos e backup na nuvem.",
      "descricao": "2 a 3 frases: o que é, para que serve no celular e o que exige (conta, espaço).",
      "destaques": ["...", "...", "..."],
      "requisitos": "Android 8.0 ou superior (confira na loja)",
      "observacoes": null
    }
  ]
}
```

Campos obrigatórios: `slug, nome, fabricante, categoria, site_oficial, url_download, tipo_download,
status_http, url_download_final, so, licenca, gratis, resumo, descricao, destaques, requisitos`.

- `categoria` sempre `celular`; `so` sempre `["android"]`.
- `resumo` 100–160 caracteres; `descricao` 250–500; `destaques` 3–4 itens de até 60 caracteres.
- `gratis`: diga a condição real — "100% grátis e open source", "grátis com anúncios",
  "grátis com compras dentro do app", "grátis para uso pessoal".
- `observacoes`: anúncios, compras no app, conta obrigatória, permissões sensíveis, APK fora da loja,
  exigência de Android mínimo. Isso é importante para o leitor decidir.

## Lista (24)

| slug | nome | onde baixar (preferência) |
|---|---|---|
| whatsapp-messenger | WhatsApp Messenger | Play Store; página oficial whatsapp.com/android |
| telegram-messenger | Telegram Messenger | Play Store ou APK oficial em telegram.org/android |
| signal-messenger | Signal | Play Store; APK oficial em signal.org/android/apk |
| firefox-android | Firefox para Android | Play Store ou APK oficial da Mozilla (ftp.mozilla.org / download.mozilla.org) |
| vlc-android | VLC for Android | Play Store; APK em get.videolan.org/vlc-android/ |
| fdroid | F-Droid | APK oficial https://f-droid.org/F-Droid.apk (direto) |
| bitwarden-android | Bitwarden | Play Store; releases APK no GitHub oficial |
| keepassdx | KeePassDX | Play Store / F-Droid / GitHub oficial |
| aegis-authenticator | Aegis Authenticator | Play Store / F-Droid / APK no GitHub oficial |
| protonvpn-android | Proton VPN | Play Store |
| tor-browser-android | Tor Browser | APK oficial do Tor Project (dist.torproject.org/.../android) |
| localsend-android | LocalSend | Play Store / APK no GitHub oficial |
| syncthing-android | Syncthing-Fork | F-Droid / APK no GitHub oficial (projeto Syncthing-Fork) |
| tailscale-android | Tailscale | Play Store |
| jellyfin-android | Jellyfin | Play Store / APK no GitHub oficial |
| kodi-android | Kodi | Play Store / APK oficial em kodi.tv/download |
| ankidroid | AnkiDroid | Play Store / F-Droid / GitHub oficial |
| open-camera | Open Camera | Play Store / F-Droid |
| material-files | Material Files | Play Store / F-Droid |
| waze | Waze | Play Store |
| joplin-android | Joplin | Play Store / APK no GitHub oficial |
| nextcloud-android | Nextcloud | Play Store / F-Droid |
| obsidian-android | Obsidian | Play Store (app gratuito para uso pessoal) |
| termux | Termux | F-Droid / APK no GitHub oficial (não use a versão antiga da Play Store) |

## Entrega

Responda curto: quantos apps, quantos `direto` (APK) vs `pagina` (loja), quais ficaram com dado
incompleto e o caminho do arquivo.
