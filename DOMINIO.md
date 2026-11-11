# Domínio — baixa.pennertech.com.br (ATIVO)

**Status 11/11/2026 17:20:** domínio **ativo e com HTTPS forçado**. O site responde em
<https://baixa.pennertech.com.br/> — GitHub Pages (repo `renatopenner/baixa-certa`, branch `main`,
raiz) com custom domain e `Enforce HTTPS` ligados.

O endereço antigo `https://pennertech.com.br/baixa-certa/` faz **301** para o domínio próprio.

## Como ficou

| Peça | Onde | Config |
|---|---|---|
| Site | repo `baixa-certa` | custom domain `baixa.pennertech.com.br`, `Enforce HTTPS` ligado, arquivo `CNAME` no repo |
| DNS | Registro.br (`d.sec.dns.br` / `e.sec.dns.br`) | CNAME `baixa` → `renatopenner.github.io` |
| Certificado | GitHub (Let's Encrypt) | emitido e aprovado automaticamente |

## Verificação (11/11/2026)

```
200  https://baixa.pennertech.com.br/
200  https://baixa.pennertech.com.br/a/vlc.html
200  https://baixa.pennertech.com.br/categoria/celular.html
200  https://baixa.pennertech.com.br/sitemap.xml
301  https://pennertech.com.br/baixa-certa/  -> https://baixa.pennertech.com.br/
```

## Regras para não quebrar

- **Nunca remover o `CNAME`** do repo: é ele que mantém o subdomínio.
- Não mexer nos 4 A do apex nem no CNAME da `loja`.
- Se a zona migrar para Cloudflare no futuro, recriar o mesmo CNAME `baixa` →
  `renatopenner.github.io`.
- O script `scripts/ativa_dominio.ps1` documenta o processo (DNS → custom domain → HTTPS); já foi
  executado e não precisa rodar de novo.
- Ao mover o site para outro host, trocar primeiro o DNS e só depois remover o custom domain do
  GitHub.

## Pendências

1. **Google Search Console**: criar propriedade `baixa.pennertech.com.br`, verificar (arquivo HTML no
   repo ou TXT no DNS) e enviar `https://baixa.pennertech.com.br/sitemap.xml`.
2. Ligar o portal à loja: já feito (menu, rodapé e banner em `loja.pennertech.com.br` apontando para
   o domínio próprio).
