# Pauta F — apps PAGOS que dominam o mercado (16 apps)

Você está montando a nova categoria **Pagos** do site **Baixa Certa** (portal da Penner Tech).
Aqui o público quer saber **quanto custa, como é cobrado e onde comprar sem cair em licença
pirata/OEM irregular**. O site não vende nada: o botão leva ao site oficial do fabricante.

## Regras

1. **Só site oficial do fabricante** (página de produto e/ou de preços). Nada de revendedor
   aleatório, marketplace, "licença vitalícia" de terceiro, crack, keygen, conta compartilhada.
2. **Preço**: confira no site oficial brasileiro (ou global com nota). Registre o texto como aparece
   ("R$ 39,90/mês", "R$ 1.299,00/ano", "US$ 19,99/mês") e **a data da conferência**. Se o preço não
   for visível (exige login/região), use `null` e explique em `observacoes`.
3. **Verifique a URL** com `curl.exe` (status final; a maioria será página HTML):
   ```
   curl.exe -sSIL --max-time 30 -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36" "URL"
   ```
4. Nunca inventar preço, versão, requisito ou licença.
5. Texto em português do Brasil, tom direto e honesto: para quem serve, o que o plano inclui, o que
   o plano gratuito (se existir) não cobre.

## Saída

Escreva **somente** `C:\Users\renat\SitesGithub\baixa-certa\pesquisa\links-f.json` (UTF-8, JSON
válido, valide com `python -m json.tool`). Não altere nenhum outro arquivo.

Formato:

```json
{
  "verificado_em": "2026-11-11",
  "apps": [
    {
      "slug": "microsoft-365",
      "nome": "Microsoft 365",
      "fabricante": "Microsoft",
      "categoria": "pagos",
      "pago": true,
      "preco": "R$ 359,00/ano (Pessoal)",
      "site_oficial": "https://www.microsoft.com/pt-br/microsoft-365/",
      "url_download": "https://www.microsoft.com/pt-br/microsoft-365/buy/compare-all-microsoft-365-products",
      "tipo_download": "pagina",
      "url_download_final": "https://...",
      "status_http": 200,
      "content_type": "text/html",
      "tamanho_arquivo": null,
      "versao": null,
      "so": ["windows", "mac", "ios", "android"],
      "arquitetura": null,
      "licenca": "Assinatura (Microsoft 365)",
      "gratis": null,
      "preco_obs": "Preço conferido em 11/11/2026 na página de planos; muda com promoções.",
      "resumo": "Office completo (Word, Excel, PowerPoint, Outlook) + 1 TB de OneDrive, em assinatura.",
      "descricao": "2 a 3 frases: o que é, para quem serve, por que pagar em vez da alternativa grátis.",
      "destaques": ["Word, Excel, PowerPoint atualizados", "1 TB de OneDrive", "Instala em PC e celular"],
      "requisitos": "Windows 10/11, macOS; apps móveis para Android/iOS",
      "observacoes": "Existe versão gratuita na web com recursos limitados; a assinatura libera o app de desktop."
    }
  ]
}
```

Campos obrigatórios: `slug, nome, fabricante, categoria, site_oficial, url_download, tipo_download,
status_http, so, licenca, resumo, descricao, destaques, requisitos, pago, preco`. Aqui `gratis` fica
`null` (é pago) e `preco` é obrigatório (ou `null` com explicação).

- `categoria` sempre `pagos`; `pago` sempre `true`.
- `so`: subconjunto de windows/mac/linux/android/ios/web.
- `resumo` 100–160 caracteres; `descricao` 250–500; `destaques` 3–4 itens até 60 caracteres.
- `preco`: o texto comercial do plano de entrada (o mais barato pago). Explicite se é mensal/anual/
  licença única. Se houver plano gratuito, diga em `observacoes`.

## Lista (16)

| slug | nome | fabricante | o que destacar |
|---|---|---|---|
| microsoft-365 | Microsoft 365 | Microsoft | planos Pessoal/Família, apps desktop + 1 TB OneDrive |
| adobe-photoshop | Adobe Photoshop | Adobe | plano Fotografia (Photoshop + Lightroom) ou avulso |
| adobe-lightroom | Adobe Lightroom | Adobe | assinatura, edição RAW + nuvem |
| adobe-acrobat-pro | Adobe Acrobat Pro | Adobe | PDF: editar, assinar, OCR |
| adobe-premiere-pro | Adobe Premiere Pro | Adobe | edição de vídeo profissional |
| affinity-photo | Affinity Photo | Canva/Affinity | licença única (sem assinatura) |
| affinity-designer | Affinity Designer | Canva/Affinity | vetorial, licença única |
| coreldraw | CorelDRAW Graphics Suite | Corel | assinatura ou licença única, mercado gráfico BR |
| autocad | AutoCAD | Autodesk | assinatura, CAD 2D/3D |
| sketchup-pro | SketchUp Pro | Trimble | modelagem 3D, assinatura |
| idm | Internet Download Manager | Tonec | licença única, gerenciador de downloads |
| filmora | Wondershare Filmora | Wondershare | editor de vídeo com assinatura |
| camtasia | TechSmith Camtasia | TechSmith | gravação e edição de tela |
| nordvpn | NordVPN | Nord Security | VPN paga, planos mensal/anual |
| malwarebytes-premium | Malwarebytes Premium | Malwarebytes | antivírus/anti-malware pago |
| revo-uninstaller-pro | Revo Uninstaller Pro | VS Revo Group | desinstalador/licença única |

## Entrega

Responda curto: quantos apps, quais preços conseguiu confirmar na fonte oficial, quais ficaram sem
preço (e por quê) e o caminho do arquivo.
