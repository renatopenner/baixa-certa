# Domínio — baixa.pennertech.com.br

**Status 11/11/2026:** site publicado e no ar em `https://pennertech.com.br/baixa-certa/`
(GitHub Pages do repo `renatopenner/baixa-certa`). Falta apenas o registro DNS do subdomínio,
que é um passo manual no Registro.br — depois disso o endereço final `https://baixa.pennertech.com.br/`
passa a valer com HTTPS.

## Situação

O site é servido pelo GitHub Pages (repo `renatopenner/baixa-certa`, branch `main`, raiz).
O GitHub Pages exige um registro DNS para reconhecer o subdomínio:

| Tipo | Nome | Valor | Onde |
|---|---|---|---|
| CNAME | `baixa` | `renatopenner.github.io` | Registro.br (zona `pennertech.com.br`) |

Não criar outro registro para `baixa` e **não** mexer nos 4 A do apex nem no CNAME da `loja`.

## Passo a passo (Registro.br)

1. Entrar em <https://registro.br> → **Painel** → `pennertech.com.br` → **DNS** → **Editar zona**.
2. Adicionar: tipo **CNAME**, nome **baixa**, valor **renatopenner.github.io** (sem ponto final,
   sem `https://`). Salvar.
3. Aguardar a publicação da zona (normalmente 10–30 min; o Registro.br mostra o status).
4. No GitHub: `gh api repos/renatopenner/baixa-certa/pages -X PUT -f cname=baixa.pennertech.com.br`
   (ou Settings → Pages → Custom domain). Marcar **Enforce HTTPS** quando o certificado sair
   (automático, costuma levar de minutos a 1 hora).

## Enquanto o DNS não propaga

O site já funciona em <https://renatopenner.github.io/baixa-certa/>.

## Verificação depois de publicar

```powershell
nslookup baixa.pennertech.com.br
curl -sI https://baixa.pennertech.com.br/           # 200
curl -sI https://baixa.pennertech.com.br/a/vlc.html # 200
curl -s  https://baixa.pennertech.com.br/sitemap.xml | Select-Object -First 3
```

Canonical, OG e sitemap já apontam para `https://baixa.pennertech.com.br` — eles passam a valer
assim que o domínio ativar.

## Regras para não quebrar

- **Não remover** o arquivo `CNAME` do repo depois que o domínio estiver ativo.
- A raiz `pennertech.com.br` continua redirecionando para a loja; o portal é subdomínio, não
  substitui a loja.
- Se um dia migrar para Cloudflare Tunnel (plano em `_tmp/plano-pennertech.md`), o CNAME do
  GitHub Pages passa a ser criado na Cloudflare — manter o mesmo nome `baixa`.
