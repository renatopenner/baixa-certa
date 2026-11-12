# Pauta H — apps mais usados: mídia, design, PDF e jogos (27)

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
   Se bloquear robô (403/429), registre o status real e explique em `observacoes`.
4. **Nunca invente** URL, versão, tamanho, preço ou licença.
5. Texto em **português do Brasil**, direto.

## Saída

Escreva **somente** `C:\Users\renat\SitesGithub\baixa-certa\pesquisa\links-h.json`
(UTF-8, JSON válido — valide com `python -m json.tool`).

Contrato igual à pauta G (mesmos campos). Exemplo de pago:

```json
{
  "slug": "illustrator",
  "nome": "Adobe Illustrator",
  "fabricante": "Adobe",
  "categoria": "imagem",
  "pago": true,
  "preco": "R$ 72,09/mês (anual, cobranças mensais)",
  "preco_obs": "Preço conferido em 12/11/2026 na página oficial de planos da Adobe.",
  "site_oficial": "https://www.adobe.com/br/products/illustrator.html",
  "url_download": "https://www.adobe.com/br/products/illustrator/plans.html",
  "tipo_download": "pagina",
  "url_download_final": "https://www.adobe.com/br/products/illustrator/plans.html",
  "status_http": 200,
  "content_type": "text/html",
  "tamanho_arquivo": null,
  "versao": null,
  "so": ["windows", "mac", "ios"],
  "arquitetura": null,
  "licenca": "Assinatura",
  "gratis": null,
  "resumo": "Ilustração vetorial padrão do mercado, com integração ao restante do Creative Cloud.",
  "descricao": "2 a 3 frases: o que é, para quem serve, por que pagar em vez da alternativa grátis.",
  "destaques": ["Vetores precisos para impressão", "Integração com Photoshop/Figma", "Fontes e efeitos"],
  "requisitos": "Windows 10/11 64-bit ou macOS, 8 GB de RAM recomendados",
  "observacoes": "Só assinatura, sem licença vitalícia. Existe teste grátis de 7 dias."
}
```

- `categoria` exatamente uma de: escritorio, multimidia, imagem, dev, utilidades, seguranca,
  internet, backup, ia, jogos.
- `resumo` 100–160 caracteres; `descricao` 250–500; `destaques` 3–4 itens até 60 caracteres.
- Freemium com plano grátis real → `pago: false` e explique em `gratis`/`observacoes`.
- Jogos gratuitos (Roblox, Valorant, LoL) → `pago: false`, link do launcher oficial do jogo.

## Lista (27)

| slug | nome | categoria | obs. |
|---|---|---|---|
| capcut | CapCut | multimidia | editor de vídeo; plano grátis com marca d'água/limites |
| streamlabs | Streamlabs Desktop | multimidia | gravação/streaming; gratuito |
| potplayer | PotPlayer | multimidia | player de vídeo gratuito (desenvolvedor Daum/Kakao) |
| mpc-hc | MPC-HC | multimidia | player leve open source; releases no GitHub oficial |
| plex | Plex Media Server | multimidia | servidor de mídia; free e planos |
| aimp | AIMP | multimidia | player de áudio gratuito |
| irfanview | IrfanView | imagem | visualizador; grátis para uso pessoal |
| xnview-mp | XnView MP | imagem | visualizador/conversor; grátis para uso pessoal |
| faststone | FastStone Image Viewer | imagem | visualizador; grátis para uso pessoal |
| rawtherapee | RawTherapee | imagem | revelação RAW open source |
| digikam | digiKam | imagem | gerenciador de fotos open source |
| capture-one | Capture One | imagem | revelação RAW profissional; PAGO |
| acrobat-reader | Adobe Acrobat Reader | escritorio | leitor de PDF gratuito |
| foxit-reader | Foxit Reader | escritorio | leitor de PDF; tem versão paga |
| illustrator | Adobe Illustrator | imagem | PAGO, assinatura |
| indesign | Adobe InDesign | imagem | PAGO, assinatura |
| after-effects | Adobe After Effects | multimidia | PAGO, assinatura |
| audition | Adobe Audition | multimidia | PAGO, assinatura |
| animate | Adobe Animate | multimidia | PAGO, assinatura |
| bandicam | Bandicam | multimidia | gravação de tela; grátis com marca d'água / PAGO |
| revit | Autodesk Revit | imagem | PAGO, assinatura (BIM) |
| solidworks | SOLIDWORKS | imagem | PAGO (CAD 3D) — página oficial do fabricante (Dassault) |
| wps-office | WPS Office | escritorio | suíte com plano grátis e Premium |
| roblox | Roblox | jogos | jogo/plataforma gratuito com itens pagos |
| minecraft | Minecraft Launcher | jogos | launcher oficial; jogo pago, launcher grátis |
| valorant | VALORANT | jogos | jogo gratuito (Riot); launcher oficial |
| league-of-legends | League of Legends | jogos | jogo gratuito (Riot); launcher oficial |

## Entrega

Responda curto: quantos apps, quantos `direto` x `pagina`, quantos pagos com preço confirmado e o
caminho do arquivo.
