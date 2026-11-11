# Ativa o domínio baixa.pennertech.com.br no GitHub Pages depois que o CNAME
# existir no Registro.br. Roda a verificação e, se o DNS já responder, configura
# o custom domain, o HTTPS e testa as URLs.
#
# Uso: pwsh scripts/ativa_dominio.ps1
$ErrorActionPreference = "Stop"
$repo = "renatopenner/baixa-certa"
$dominio = "baixa.pennertech.com.br"
$alvo = "renatopenner.github.io"

Write-Host "1/4 Conferindo DNS de $dominio ..."
$cname = $null
try { $cname = (Resolve-DnsName $dominio -Type CNAME -ErrorAction Stop).NameHost } catch { }
if (-not $cname) {
  Write-Host "  DNS ainda não respondeu. Crie no Registro.br: CNAME  baixa  ->  $alvo" -ForegroundColor Yellow
  exit 1
}
Write-Host "  CNAME: $cname"
if ($cname -notlike "*$alvo*") {
  Write-Host "  CNAME aponta para $cname (esperado $alvo). Confira antes de continuar." -ForegroundColor Yellow
  exit 1
}

Write-Host "2/4 Configurando custom domain no GitHub Pages ..."
gh api "repos/$repo/pages" -X PUT -f "cname=$dominio" | Out-Null
Write-Host "  ok"

Write-Host "3/4 Aguardando certificado/HTTPS (pode levar alguns minutos) ..."
$ok = $false
for ($i = 1; $i -le 20; $i++) {
  $r = curl.exe -sS -o NUL -w "%{http_code}" "https://$dominio/" 2>$null
  if ($r -eq "200") { $ok = $true; break }
  Start-Sleep -Seconds 20
}
if ($ok) {
  gh api "repos/$repo/pages" -X PUT -f "https_enforced=true" | Out-Null
  Write-Host "  HTTPS ativo"
} else {
  Write-Host "  HTTPS ainda não respondeu. Veja Settings > Pages do repo; o certificado costuma sair em até 1 hora." -ForegroundColor Yellow
}

Write-Host "4/4 Teste final:"
foreach ($caminho in @("/", "/a/vlc.html", "/categoria/jogos.html", "/sitemap.xml", "/robots.txt")) {
  $codigo = curl.exe -sS -o NUL -w "%{http_code}" "https://$dominio$caminho" 2>$null
  Write-Host ("  {0,-28} {1}" -f $caminho, $codigo)
}
Write-Host "`nPronto. Falta trocar o link da loja (https://pennertech.com.br/baixa-certa/) por https://$dominio/"
Write-Host "nos arquivos HTML de C:\Users\renat\SitesGithub\site-renato-penner e dar push."
