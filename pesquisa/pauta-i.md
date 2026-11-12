# Pauta I — apps mais usados: desenvolvimento, segurança e utilidades (26)

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
4. **Nunca invente** URL, versão, tamanho, preço ou licença.
5. Texto em **português do Brasil**, direto.

## Saída

Escreva **somente** `C:\Users\renat\SitesGithub\baixa-certa\pesquisa\links-i.json`
(UTF-8, JSON válido — valide com `python -m json.tool`). Contrato igual à pauta G/H (mesmos campos,
`pago`/`preco`/`preco_obs` inclusos).

- `categoria` exatamente uma de: escritorio, multimidia, imagem, dev, utilidades, seguranca,
  internet, backup, ia, jogos.
- `resumo` 100–160 caracteres; `descricao` 250–500; `destaques` 3–4 itens até 60 caracteres.
- Freemium com plano grátis real → `pago: false` e explique em `gratis`/`observacoes`.
- Pago → `pago: true` + `preco` (plano de entrada) + `preco_obs` com a data da conferência.

## Lista (26)

| slug | nome | categoria | obs. |
|---|---|---|---|
| docker-desktop | Docker Desktop | dev | grátis para uso pessoal/pequenas empresas; planos pagos |
| visual-studio | Visual Studio Community | dev | edição gratuita da IDE da Microsoft |
| intellij-idea | IntelliJ IDEA | dev | Community grátis; Ultimate pago |
| pycharm | PyCharm | dev | Community grátis; Professional pago |
| android-studio | Android Studio | dev | IDE oficial Android, gratuita |
| nodejs | Node.js | dev | runtime JavaScript gratuito (LTS no site oficial) |
| java-jdk | Java (JDK) | dev | Oracle JDK / OpenJDK; use a página oficial da Oracle ou Eclipse Temurin |
| postman | Postman | dev | cliente de API; plano grátis |
| xampp | XAMPP | dev | Apache+PHP+MySQL para testes locais |
| mysql-workbench | MySQL Workbench | dev | modelagem/administração MySQL, gratuito |
| ssms | SQL Server Management Studio | dev | ferramenta gratuita da Microsoft |
| pgadmin | pgAdmin | dev | administração PostgreSQL, open source |
| sourcetree | Sourcetree | dev | cliente Git gratuito (Atlassian) |
| winscp | WinSCP | internet | transferência SFTP/FTP gratuita |
| wireshark | Wireshark | seguranca | analisador de rede open source |
| glasswire | GlassWire | seguranca | monitor de rede; grátis e Elite |
| 1password | 1Password | seguranca | PAGO, gerenciador de senhas por assinatura |
| expressvpn | ExpressVPN | seguranca | PAGO, VPN por assinatura |
| avast | Avast Free Antivirus | seguranca | gratuito com upsell para o Premium |
| kaspersky | Kaspersky Standard | seguranca | PAGO (assinatura) |
| bitdefender | Bitdefender | seguranca | PAGO (assinatura); existe versão free limitada |
| ccleaner | CCleaner | utilidades | limpeza; versão grátis e Professional |
| driver-booster | Driver Booster | utilidades | atualização de drivers; grátis com limites, Pro pago |
| anydesk | AnyDesk | internet | acesso remoto; grátis para uso pessoal |
| msi-afterburner | MSI Afterburner | utilidades | overclock/monitoramento, gratuito |
| hwmonitor | HWMonitor | utilidades | monitoramento de hardware; versão grátis |

## Entrega

Responda curto: quantos apps, quantos `direto` x `pagina`, quantos pagos com preço confirmado e o
caminho do arquivo.
