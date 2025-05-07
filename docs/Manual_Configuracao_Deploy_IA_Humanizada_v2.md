# Manual de Configuração e Deploy - Plataforma IA Humanizada

Este manual detalha os passos para configurar as variáveis de ambiente necessárias e realizar o deploy da aplicação IA Humanizada (backend Flask e frontend Next.js) em diferentes ambientes: localmente (localhost), em sua própria VPS (Ubuntu 20.04 ou 22.04) utilizando o domínio `www.iahumanizada.com.br`, e em uma VPS da Hostinger.

## 0. Visão Geral da Arquitetura

A plataforma consiste em dois componentes principais:

*   **Backend:** Uma API RESTful construída com Flask (Python), responsável pela lógica de negócios, gerenciamento de usuários, agentes, bases de conhecimento e interação com LLMs.
*   **Frontend:** Uma aplicação single-page (SPA) construída com Next.js (React/TypeScript), fornecendo a interface do usuário para interagir com a plataforma.

Eles se comunicam via requisições HTTP, com o frontend consumindo os endpoints da API do backend.

## 1. Configuração das Variáveis de Ambiente (`.env` no Backend)

A aplicação utiliza um arquivo `.env` na raiz do diretório do backend (`ia_humanizada_platform/backend/backend_app/`) para gerenciar configurações sensíveis e específicas do ambiente. Isso evita que credenciais sejam expostas diretamente no código.

**Passos para criar e configurar o `.env`:**

1.  **Navegue até o diretório do backend:** `cd /caminho/para/seu/projeto/ia_humanizada_platform/backend/backend_app/`
2.  **Copie o arquivo de exemplo:** `cp .env.example .env` (o arquivo `.env.example` já está no projeto).
3.  **Edite o arquivo `.env`:** Abra o arquivo `.env` recém-criado em um editor de texto e preencha os valores conforme abaixo.

**Variáveis no `.env`:**

```dotenv
# Backend Configuration for IA Humanizada Platform

# --- Flask App Settings --- #
# Chave secreta para segurança das sessões Flask. Gere uma chave segura e aleatória.
# Exemplo (Python): python -c 'import secrets; print(secrets.token_hex(16))'
SECRET_KEY=SUA_CHAVE_SECRETA_AQUI

# Define se o Flask roda em modo debug. Use 'False' em produção, 'True' em desenvolvimento.
FLASK_DEBUG=True

# --- Database (PostgreSQL) --- #
# Usuário do banco de dados PostgreSQL
DB_USERNAME=postgres

# Senha do usuário do banco de dados PostgreSQL (definida durante a configuração do DB)
DB_PASSWORD=SUA_SENHA_DO_BANCO_AQUI

# Host/IP onde o servidor PostgreSQL está rodando (geralmente 'localhost' se na mesma máquina)
DB_HOST=localhost

# Porta do servidor PostgreSQL (padrão é 5432)
DB_PORT=5432

# Nome do banco de dados criado para a aplicação
DB_NAME=ia_humanizada_db

# --- LLM API Keys --- #
# Sua chave de API da OpenAI (obrigatória para a funcionalidade de chat)
OPENAI_API_KEY=SUA_CHAVE_OPENAI_AQUI

# Sua chave de API do Google Gemini (para futura integração)
GEMINI_API_KEY=SUA_CHAVE_GEMINI_AQUI

# --- Frontend URL (para CORS) --- #
# A URL base do seu frontend. Para desenvolvimento local, geralmente http://localhost:3000
# Para produção, será https://www.iahumanizada.com.br
FRONTEND_URL=http://localhost:3000
```

**Importante:** Nunca adicione o arquivo `.env` ao controle de versão (Git). O arquivo `.gitignore` na raiz do projeto já está configurado para ignorá-lo.

## 2. Configuração do Frontend (`.env.local`)

O frontend Next.js também utiliza um arquivo para variáveis de ambiente, localizado em `ia_humanizada_platform/frontend/frontend_app/.env.local`.

**Passos:**

1.  **Navegue até o diretório do frontend:** `cd /caminho/para/seu/projeto/ia_humanizada_platform/frontend/frontend_app/`
2.  **Crie o arquivo `.env.local`** (se não existir).
3.  **Adicione a URL da API do backend:**

    ```dotenv
    NEXT_PUBLIC_API_URL=http://localhost:5000/api
    ```
    *   **Para desenvolvimento local:** Use `http://localhost:5000/api` (ou a porta que o backend estiver usando).
    *   **Para produção (VPS/Hostinger):** Use `https://www.iahumanizada.com.br/api` (ou o subdomínio da API, se configurado).

## 3. Instalação e Execução em Ambiente Local (localhost)

Ideal para desenvolvimento e testes.

**Pré-requisitos:**

*   **Git:** Instalado.
*   **Python & Pip:** Instalados (versão 3.10 ou superior).
*   **Node.js & pnpm:** Instalados (Node.js versão 18 ou superior, pnpm é usado no projeto).
*   **PostgreSQL Server:** Instalado, rodando e acessível. Crie o banco de dados `ia_humanizada_db` e um usuário/senha (ex: usuário `postgres` com a senha que você definir).

**Passos para o Backend (Flask):**

1.  **Clone o Repositório (se ainda não o fez):**
    ```bash
    git clone <URL_DO_SEU_REPOSITORIO_OU_EXTRAIA_O_ZIP> ia_humanizada_platform
    cd ia_humanizada_platform/backend/backend_app
    ```
2.  **Crie e Ative o Ambiente Virtual:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    ```
3.  **Instale as Dependências:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure o `.env`:** Siga a Seção 1, preenchendo `DB_PASSWORD` com a senha do seu PostgreSQL local e `FLASK_DEBUG=True`, `FRONTEND_URL=http://localhost:3000`.
5.  **Crie as Tabelas no Banco de Dados:**
    ```bash
    flask db init  # Se for a primeira vez e a pasta migrations não existir
    flask db migrate -m "Initial migration" # Se for a primeira vez
    flask db upgrade
    ```
    (Nota: O projeto atual pode não ter Flask-Migrate configurado. Se for o caso, as tabelas são criadas quando o app inicia e `db.create_all()` é chamado, ou você pode precisar de um script para isso.)
    No projeto atual, as tabelas são criadas via `db.create_all()` no `create_app`.
6.  **Execute o Servidor de Desenvolvimento Flask:**
    ```bash
    export FLASK_APP=main.py # Ou set FLASK_APP=main.py no Windows
    flask run --host=0.0.0.0 --port=5000
    ```
    O backend estará rodando em `http://localhost:5000`.

**Passos para o Frontend (Next.js):**

1.  **Navegue até o Diretório do Frontend:**
    ```bash
    cd ../../frontend/frontend_app  # A partir da raiz do projeto
    ```
2.  **Instale as Dependências:**
    ```bash
    pnpm install
    ```
3.  **Configure o `.env.local`:** Siga a Seção 2, usando `NEXT_PUBLIC_API_URL=http://localhost:5000/api`.
4.  **Execute o Servidor de Desenvolvimento Next.js:**
    ```bash
    pnpm dev
    ```
    O frontend estará rodando em `http://localhost:3000`.

Agora você pode acessar `http://localhost:3000` no seu navegador para usar a plataforma.

## 4. Deploy em VPS Própria (Ubuntu 20.04 / 22.04)

**Pré-requisitos na VPS:**

*   **Acesso SSH:** Com um usuário com privilégios `sudo`.
*   **Firewall Configurado:** (e.g., UFW) Permitindo tráfego nas portas 80 (HTTP), 443 (HTTPS) e 22 (SSH).
*   **Git, Python3, Pip, Venv, Node.js, pnpm:** Instalados (veja seções anteriores para comandos de instalação).
*   **PostgreSQL Server:** Instalado e configurado (crie o banco `ia_humanizada_db` e um usuário/senha).
*   **Nginx:** Instalado (`sudo apt install nginx -y`).
*   **Certbot:** Para SSL (`sudo apt install certbot python3-certbot-nginx -y`).
*   **Domínio Configurado:** `www.iahumanizada.com.br` (e `iahumanizada.com.br`) apontando para o IP público da sua VPS.

**Passos para o Backend (Flask com Gunicorn):**

1.  **Clone o Repositório e Navegue:**
    ```bash
    git clone <URL_DO_SEU_REPOSITORIO_OU_EXTRAIA_O_ZIP> ia_humanizada_platform
    cd ia_humanizada_platform/backend/backend_app
    ```
2.  **Ambiente Virtual e Dependências:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    pip install gunicorn # Para produção
    ```
3.  **Configure o `.env`:** Siga a Seção 1. Use `FLASK_DEBUG=False`, `FRONTEND_URL=https://www.iahumanizada.com.br`, e as credenciais corretas do seu PostgreSQL na VPS.
4.  **Crie as Tabelas no Banco (se necessário):** Como na configuração local.
5.  **Configure o Gunicorn como Serviço (systemd):**
    *   Crie `sudo nano /etc/systemd/system/iahumanizada-backend.service`:
        ```ini
        [Unit]
        Description=Gunicorn instance for IA Humanizada Backend
        After=network.target

        [Service]
        User=seu_usuario_na_vps # Usuário não-root que rodará o processo
        Group=www-data
        WorkingDirectory=/home/seu_usuario_na_vps/ia_humanizada_platform/backend/backend_app
        Environment="PATH=/home/seu_usuario_na_vps/ia_humanizada_platform/backend/backend_app/venv/bin"
        # EnvironmentFile=/home/seu_usuario_na_vps/ia_humanizada_platform/backend/backend_app/.env # Carrega variáveis do .env
        ExecStart=/home/seu_usuario_na_vps/ia_humanizada_platform/backend/backend_app/venv/bin/gunicorn --workers 3 --bind unix:/tmp/iahumanizada-backend.sock main:app
        # Para carregar .env, descomente EnvironmentFile ou passe variáveis aqui:
        # ExecStart=/bin/sh -c 'source /home/seu_usuario_na_vps/ia_humanizada_platform/backend/backend_app/.env && /home/seu_usuario_na_vps/ia_humanizada_platform/backend/backend_app/venv/bin/gunicorn --workers 3 --bind unix:/tmp/iahumanizada-backend.sock main:app'

        [Install]
        WantedBy=multi-user.target
        ```
        *Ajuste `seu_usuario_na_vps` e os caminhos.*
    *   Inicie e habilite:
        ```bash
        sudo systemctl daemon-reload
        sudo systemctl start iahumanizada-backend
        sudo systemctl enable iahumanizada-backend
        sudo systemctl status iahumanizada-backend
        ```

**Passos para o Frontend (Next.js com PM2):**

1.  **Navegue até o Diretório do Frontend:**
    ```bash
    cd /home/seu_usuario_na_vps/ia_humanizada_platform/frontend/frontend_app
    ```
2.  **Instale Dependências:** `pnpm install`
3.  **Configure o `.env.local`:** Siga a Seção 2, usando `NEXT_PUBLIC_API_URL=https://www.iahumanizada.com.br/api`.
4.  **Build da Aplicação:** `pnpm build`
5.  **Instale PM2 (Gerenciador de Processos):**
    ```bash
    sudo pnpm install -g pm2 # Ou npm install -g pm2
    ```
6.  **Inicie o Frontend com PM2:**
    ```bash
    pm2 start pnpm --name "iahumanizada-frontend" -- run start # O comando 'start' do package.json (next start)
    pm2 startup # Para iniciar com o sistema
    pm2 save # Salva a configuração atual do PM2
    ```
    O frontend Next.js geralmente roda na porta 3000 por padrão.

**Configuração do Nginx como Reverse Proxy (para Backend e Frontend):**

1.  Crie `sudo nano /etc/nginx/sites-available/iahumanizada`:
    ```nginx
    server {
        listen 80;
        server_name www.iahumanizada.com.br iahumanizada.com.br;

        # Redirecionamento para HTTPS (será adicionado pelo Certbot ou pode ser manual)
        # location / {
        #    return 301 https://$host$request_uri;
        # }

        # Para verificações do Certbot
        location ~ /.well-known/acme-challenge/ {
            allow all;
            root /var/www/html; # Ou outro diretório acessível
        }
    }

    server {
        listen 443 ssl http2;
        server_name www.iahumanizada.com.br iahumanizada.com.br;

        ssl_certificate /etc/letsencrypt/live/www.iahumanizada.com.br/fullchain.pem; # Caminho do Certbot
        ssl_certificate_key /etc/letsencrypt/live/www.iahumanizada.com.br/privkey.pem; # Caminho do Certbot
        include /etc/letsencrypt/options-ssl-nginx.conf; # Configurações SSL recomendadas
        ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # Configurações SSL recomendadas

        location /api/ {
            proxy_pass http://unix:/tmp/iahumanizada-backend.sock; # Comunica com Gunicorn
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_read_timeout 600s; # Aumentar timeout se necessário
            proxy_send_timeout 600s;
        }

        location / {
            proxy_pass http://localhost:3000; # Comunica com o servidor Next.js (PM2)
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_cache_bypass $http_upgrade;
        }

        # Configurações adicionais de segurança e otimização podem ser adicionadas aqui
        client_max_body_size 100M; # Exemplo para permitir uploads maiores
    }
    ```
2.  Habilite o site: `sudo ln -s /etc/nginx/sites-available/iahumanizada /etc/nginx/sites-enabled/`
3.  Teste e reinicie Nginx: `sudo nginx -t && sudo systemctl restart nginx`

**Configuração do SSL com Certbot:**

1.  Execute o Certbot:
    ```bash
    sudo certbot --nginx -d www.iahumanizada.com.br -d iahumanizada.com.br
    ```
    Siga as instruções, escolha redirecionar HTTP para HTTPS.
2.  Verifique a renovação: `sudo certbot renew --dry-run`.

## 5. Deploy em VPS da Hostinger

A Hostinger oferece planos VPS onde você terá acesso root, similar a uma VPS própria. Portanto, **os passos para deploy em uma VPS da Hostinger são essencialmente os mesmos descritos na Seção 4 (Deploy em VPS Própria Ubuntu).**

**Considerações Específicas da Hostinger:**

*   **Escolha do Plano VPS:** Certifique-se de que o plano VPS escolhido tem recursos suficientes (CPU, RAM, Disco) para rodar PostgreSQL, Node.js (para Next.js), Python (para Flask/Gunicorn) e Nginx simultaneamente.
*   **Sistema Operacional:** Ao configurar sua VPS na Hostinger, escolha uma distribuição Linux como Ubuntu 20.04 ou 22.04.
*   **Painel da Hostinger:** Utilize o painel da Hostinger para gerenciar sua VPS, configurar DNS para seu domínio `www.iahumanizada.com.br` apontar para o IP da VPS, e gerenciar o firewall (se houver um firewall de nível de provedor além do UFW na VPS).
*   **Suporte Hostinger:** Consulte a documentação da Hostinger ou o suporte deles para quaisquer particularidades sobre a configuração de firewalls, redes ou instalação de pacotes em suas VPSs.
*   **Importante:** Conforme pesquisa, planos de hospedagem compartilhada da Hostinger **não suportam** deploy direto de aplicações Next.js (que precisam de Node.js no servidor) ou Flask (que precisa de Python e controle sobre o ambiente). Você **precisará de um plano VPS**.

Siga todos os passos da Seção 4, adaptando os caminhos de diretório e nomes de usuário conforme sua configuração na VPS da Hostinger.

## 6. Dicas e Solução de Problemas

*   **Logs:** Verifique os logs do Nginx (`/var/log/nginx/error.log`, `/var/log/nginx/access.log`), Gunicorn (via `sudo journalctl -u iahumanizada-backend`), PM2 (`pm2 logs iahumanizada-frontend`) e do próprio PostgreSQL para diagnosticar problemas.
*   **Permissões:** Certifique-se de que os usuários que rodam Gunicorn e PM2 têm as permissões corretas para acessar os arquivos do projeto e o socket (no caso do Gunicorn).
*   **Firewall:** Verifique se o firewall (UFW na VPS, firewall da Hostinger) não está bloqueando as portas 80, 443 ou a comunicação entre os serviços.
*   **Variáveis de Ambiente:** Confirme que todas as variáveis nos arquivos `.env` e `.env.local` estão corretas para o ambiente de produção.
*   **CORS:** O backend Flask já está configurado com Flask-CORS para permitir requisições do `FRONTEND_URL` definido no `.env`. Certifique-se que esta URL está correta em produção.

Este manual deve fornecer uma base sólida para o deploy da sua plataforma. Boa sorte!

