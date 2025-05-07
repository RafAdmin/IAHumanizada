# Manual Completo de Instalação e Deploy da Plataforma IA Humanizada

## 1. Introdução

Este manual fornece instruções detalhadas para configurar, instalar e implantar a plataforma IA Humanizada em diferentes ambientes: local (para desenvolvimento), em um Servidor Privado Virtual (VPS) com Ubuntu 20.04 (para produção) e em um VPS da Hostinger.

A plataforma é composta por um backend desenvolvido em Flask (Python) e um frontend desenvolvido em Next.js (Node.js), utilizando PostgreSQL como banco de dados.

**Importante:** Para deploy na Hostinger, é crucial entender que os planos de hospedagem compartilhada **não suportam** aplicações Flask ou Next.js de forma nativa devido à necessidade de acesso root e gerenciamento de processos específicos. Portanto, este guia para Hostinger foca exclusivamente na utilização de seus **planos VPS**.

## 2. Pré-requisitos Gerais

Antes de iniciar, garanta que você tenha as seguintes ferramentas e conhecimentos básicos:

*   **Git:** Para controle de versão e clonagem do repositório.
*   **Linha de Comando (Terminal/Shell):** Familiaridade com operações básicas.
*   **Node.js e npm/pnpm:** Para o frontend Next.js (recomendamos pnpm).
*   **Python e pip:** Para o backend Flask.
*   **virtualenv (ou venv):** Para isolamento de ambientes Python.
*   **PostgreSQL:** Conhecimento básico de instalação e gerenciamento (para VPS).
*   **Acesso SSH:** Para conectar e gerenciar servidores VPS.
*   **Editor de Texto/IDE:** Para visualizar e editar arquivos de configuração.

## 3. Configuração do Arquivo `.env`

A plataforma utiliza arquivos `.env` para gerenciar variáveis de ambiente sensíveis e de configuração, tanto para o backend quanto para o frontend. Nunca adicione os arquivos `.env` diretamente ao controle de versão (eles já estão no `.gitignore`).

Crie os arquivos `.env` a partir dos exemplos (`.env.example`) fornecidos nos respectivos diretórios (`ia_humanizada_platform/backend/backend_app/.env` e `ia_humanizada_platform/frontend/frontend_app/.env.local`).

### 3.1. Backend (`ia_humanizada_platform/backend/backend_app/.env`)

```env
# Configurações da Aplicação Flask
FLASK_APP=main.py
FLASK_ENV=development # Mude para 'production' em ambiente de produção
SECRET_KEY='SUA_CHAVE_SECRETA_FORTE_AQUI' # Gere uma chave segura (ex: openssl rand -hex 32)

# Configurações do Banco de Dados PostgreSQL
DATABASE_URL='postgresql://usuario:senha@host:porta/nome_do_banco'
# Exemplo Local: postgresql://iahumanizada_user:iahumanizada_password@localhost:5432/iahumanizada_db
# Exemplo VPS: postgresql://seu_usuario_pg:sua_senha_pg@localhost:5432/seu_banco_pg

# Configurações de API (Exemplos)
OPENAI_API_KEY='SUA_CHAVE_API_OPENAI_AQUI'
# GEMINI_API_KEY='SUA_CHAVE_API_GEMINI_AQUI' # Adicione conforme necessário

# Outras configurações
# CORS_ORIGINS='http://localhost:3000,https://www.iahumanizada.com.br' # Para produção, adicione seu domínio frontend
```

### 3.2. Frontend (`ia_humanizada_platform/frontend/frontend_app/.env.local`)

```env
# URL da API Backend
NEXT_PUBLIC_API_URL='http://localhost:5000/api' # Para desenvolvimento local
# Em produção, substitua pela URL da sua API backend (ex: https://api.iahumanizada.com.br/api)

# Outras variáveis de ambiente específicas do frontend (se houver)
```

**Geração de `SECRET_KEY`:**
Use o comando abaixo no terminal para gerar uma chave secreta forte para o Flask:
```bash
openssl rand -hex 32
```
Copie o resultado e cole no valor de `SECRET_KEY`.

## 4. Deploy em Ambiente Local (Desenvolvimento)

Ideal para desenvolvimento e testes.

### 4.1. Clonar o Repositório (se ainda não o fez)
```bash
git clone <URL_DO_SEU_REPOSITORIO_GIT_IAHUMANIZADA>
cd iahumanizada_platform
```

### 4.2. Configurar e Rodar o Backend (Flask)

1.  **Navegue até o diretório do backend:**
    ```bash
    cd backend/backend_app
    ```
2.  **Crie e ative um ambiente virtual Python:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure o banco de dados PostgreSQL localmente:**
    *   Instale o PostgreSQL se ainda não o tiver.
    *   Crie um usuário e um banco de dados para a aplicação.
        Exemplo de comandos no psql (substitua com seus valores):
        ```sql
        CREATE USER iahumanizada_user WITH PASSWORD 'iahumanizada_password';
        CREATE DATABASE iahumanizada_db OWNER iahumanizada_user;
        ```
5.  **Crie e configure o arquivo `.env`:**
    Copie `.env.example` para `.env` e preencha com suas credenciais do banco de dados local e `SECRET_KEY`.
    Exemplo para `DATABASE_URL` local:
    `DATABASE_URL='postgresql://iahumanizada_user:iahumanizada_password@localhost:5432/iahumanizada_db'`
6.  **Execute as migrações do banco de dados (Flask-Migrate):**
    ```bash
    flask db init  # Apenas na primeira vez, se a pasta migrations não existir
    flask db migrate -m "Initial migration" # Apenas na primeira vez
    flask db upgrade
    ```
7.  **Inicie o servidor Flask:**
    ```bash
    flask run
    ```
    O backend estará rodando, por padrão, em `http://127.0.0.1:5000`.

### 4.3. Configurar e Rodar o Frontend (Next.js)

1.  **Abra um novo terminal.**
2.  **Navegue até o diretório do frontend:**
    ```bash
    cd frontend/frontend_app # A partir da raiz do projeto iahumanizada_platform
    ```
3.  **Instale as dependências (usando pnpm, recomendado):**
    ```bash
    pnpm install
    ```
4.  **Crie e configure o arquivo `.env.local`:**
    Copie `.env.example` (se existir) ou crie `.env.local` e defina `NEXT_PUBLIC_API_URL` para apontar para o seu backend local:
    `NEXT_PUBLIC_API_URL='http://localhost:5000/api'`
5.  **Inicie o servidor de desenvolvimento Next.js:**
    ```bash
    pnpm dev
    ```
    O frontend estará rodando, por padrão, em `http://localhost:3000`.

### 4.4. Acessar a Aplicação

Abra `http://localhost:3000` no seu navegador para acessar a plataforma IA Humanizada.

## 5. Deploy em VPS Ubuntu 20.04 (Produção)

Este guia assume que você tem um VPS com Ubuntu 20.04 e acesso root/sudo.

### 5.1. Conectar ao VPS via SSH
```bash
ssh seu_usuario@IP_DO_SEU_VPS
```

### 5.2. Atualizar o Sistema e Instalar Dependências Essenciais
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-dev python3-venv nginx curl git postgresql postgresql-contrib libpq-dev
```

### 5.3. Configurar Banco de Dados PostgreSQL no VPS
1.  **Inicie e habilite o serviço PostgreSQL:**
    ```bash
    sudo systemctl start postgresql
    sudo systemctl enable postgresql
    ```
2.  **Acesse o psql como usuário postgres:**
    ```bash
    sudo -u postgres psql
    ```
3.  **Crie um usuário e um banco de dados para a aplicação (substitua com seus valores):**
    ```sql
    CREATE USER seu_usuario_db WITH PASSWORD 'sua_senha_db_forte';
    CREATE DATABASE seu_banco_db OWNER seu_usuario_db;
    
    -- Opcional: Se o usuário do sistema que rodará o Flask for diferente do seu_usuario_db
    -- GRANT ALL PRIVILEGES ON DATABASE seu_banco_db TO seu_usuario_db;
    ```
4.  **Saia do psql:** `\q`

### 5.4. Clonar o Repositório no VPS
```bash
cd /var/www # Ou outro diretório de sua preferência para projetos web
sudo git clone <URL_DO_SEU_REPOSITORIO_GIT_IAHUMANIZADA> iahumanizada.com.br
cd iahumanizada.com.br
sudo chown -R $USER:$USER . # Dê permissão ao seu usuário atual (ou crie um usuário dedicado)
```

### 5.5. Configurar o Backend (Flask) no VPS

1.  **Navegue até o diretório do backend:**
    ```bash
    cd backend/backend_app
    ```
2.  **Crie e ative um ambiente virtual:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  **Instale as dependências Python, incluindo Gunicorn:**
    ```bash
    pip install -r requirements.txt
    pip install gunicorn # Servidor de aplicação WSGI para produção
    ```
4.  **Crie e configure o arquivo `.env`:**
    Copie `.env.example` para `.env`. Preencha `SECRET_KEY`, `OPENAI_API_KEY`, e a `DATABASE_URL` apontando para o PostgreSQL no VPS.
    Exemplo `DATABASE_URL`:
    `DATABASE_URL='postgresql://seu_usuario_db:sua_senha_db_forte@localhost:5432/seu_banco_db'`
    Mude `FLASK_ENV` para `production`.
5.  **Execute as migrações do banco de dados:**
    ```bash
    flask db upgrade
    ```
6.  **Teste o Gunicorn (opcional, mas recomendado):**
    ```bash
    gunicorn --workers 3 --bind unix:/tmp/iahumanizada_backend.sock -m 007 main:app
    ```
    (Use `Ctrl+C` para parar após o teste. O socket será criado em `/tmp/` ou no diretório do projeto se preferir)
    Se preferir testar via porta TCP (ex: 8000) antes de configurar o socket:
    `gunicorn --workers 3 --bind 0.0.0.0:8000 main:app`
    Lembre-se de liberar a porta no firewall (`sudo ufw allow 8000`) para teste externo.

7.  **Configurar Supervisor para Gerenciar o Gunicorn:**
    Supervisor garante que sua aplicação Flask reinicie se falhar e inicie com o boot do sistema.
    ```bash
    sudo apt install -y supervisor
    ```
    Crie um arquivo de configuração para sua aplicação no Supervisor:
    ```bash
    sudo nano /etc/supervisor/conf.d/iahumanizada_backend.conf
    ```
    Cole o seguinte conteúdo (ajuste os caminhos e usuário se necessário):
    ```ini
    [program:iahumanizada_backend]
    command=/var/www/iahumanizada.com.br/backend/backend_app/venv/bin/gunicorn --workers 3 --bind unix:/var/www/iahumanizada.com.br/backend/backend_app/iahumanizada_backend.sock -m 007 main:app
    directory=/var/www/iahumanizada.com.br/backend/backend_app
    user=seu_usuario_do_sistema # O usuário que tem permissão na pasta do projeto
    autostart=true
    autorestart=true
    stderr_logfile=/var/log/supervisor/iahumanizada_backend_err.log
    stdout_logfile=/var/log/supervisor/iahumanizada_backend_out.log
    ```
    **Nota sobre o socket:** O caminho `unix:/var/www/iahumanizada.com.br/backend/backend_app/iahumanizada_backend.sock` é uma sugestão. Garanta que o Nginx (próximo passo) tenha permissão para acessá-lo.

    Recarregue e inicie o serviço do Supervisor:
    ```bash
    sudo supervisorctl reread
    sudo supervisorctl update
    sudo supervisorctl start iahumanizada_backend
    sudo supervisorctl status iahumanizada_backend
    ```

### 5.6. Configurar o Frontend (Next.js) no VPS

1.  **Instale Node.js e pnpm (ou npm):**
    ```bash
    curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
    sudo apt install -y nodejs
    sudo npm install -g pnpm # Recomendado
    ```
2.  **Navegue até o diretório do frontend:**
    ```bash
    cd /var/www/iahumanizada.com.br/frontend/frontend_app
    ```
3.  **Instale as dependências:**
    ```bash
    pnpm install
    ```
4.  **Crie e configure o arquivo `.env.local`:**
    Defina `NEXT_PUBLIC_API_URL` para a URL pública do seu backend (que será configurada no Nginx, ex: `https://api.iahumanizada.com.br/api`).
5.  **Faça o build da aplicação Next.js para produção:**
    ```bash
    pnpm build
    ```
6.  **Configurar PM2 para Gerenciar a Aplicação Next.js:**
    PM2 é um gerenciador de processos para Node.js que ajuda a manter sua aplicação viva.
    ```bash
    sudo pnpm add -g pm2 # Instala PM2 globalmente usando pnpm
    # ou sudo npm install pm2 -g
    ```
    Inicie a aplicação Next.js com PM2 (a partir do diretório `frontend/frontend_app`):
    ```bash
    pm2 start pnpm --name "iahumanizada_frontend" -- start -p 3000 # O -p 3000 é a porta que o Next.js escutará localmente
    ```
    Configure PM2 para iniciar no boot:
    ```bash
    pm2 startup systemd
    # Siga as instruções que o comando acima fornecer (geralmente copiar e colar um comando com sudo)
    pm2 save
    ```
    Verifique o status:
    ```bash
    pm2 list
    ```

### 5.7. Configurar Nginx como Proxy Reverso

Nginx servirá seus arquivos estáticos, atuará como proxy reverso para Gunicorn (backend) e PM2/Next.js (frontend), e lidará com SSL.

1.  **Crie um arquivo de configuração do Nginx para sua aplicação:**
    ```bash
    sudo nano /etc/nginx/sites-available/iahumanizada.com.br
    ```
    Cole a seguinte configuração (ajuste `server_name`, caminhos do socket/logs e portas conforme necessário):

    ```nginx
    # Backend API em api.iahumanizada.com.br
    server {
        listen 80;
        server_name api.iahumanizada.com.br;

        location / {
            include proxy_params;
            proxy_pass http://unix:/var/www/iahumanizada.com.br/backend/backend_app/iahumanizada_backend.sock;
        }

        # Logs (opcional, mas recomendado)
        access_log /var/log/nginx/api.iahumanizada.com.br.access.log;
        error_log /var/log/nginx/api.iahumanizada.com.br.error.log;
    }

    # Frontend em www.iahumanizada.com.br
    server {
        listen 80;
        server_name www.iahumanizada.com.br iahumanizada.com.br;

        location / {
            proxy_pass http://localhost:3000; # Porta que o Next.js (PM2) está escutando
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_cache_bypass $http_upgrade;
        }

        # Logs (opcional, mas recomendado)
        access_log /var/log/nginx/www.iahumanizada.com.br.access.log;
        error_log /var/log/nginx/www.iahumanizada.com.br.error.log;
    }
    ```

2.  **Crie um link simbólico para habilitar o site:**
    ```bash
    sudo ln -s /etc/nginx/sites-available/iahumanizada.com.br /etc/nginx/sites-enabled/
    ```
3.  **Teste a configuração do Nginx:**
    ```bash
    sudo nginx -t
    ```
4.  **Reinicie o Nginx:**
    ```bash
    sudo systemctl restart nginx
    ```

### 5.8. Configurar Domínio e SSL com Let's Encrypt

1.  **Configure os registros DNS:**
    No seu provedor de domínio (onde você comprou `iahumanizada.com.br`), crie/atualize os seguintes registros A:
    *   `iahumanizada.com.br` -> `IP_DO_SEU_VPS`
    *   `www.iahumanizada.com.br` -> `IP_DO_SEU_VPS`
    *   `api.iahumanizada.com.br` -> `IP_DO_SEU_VPS`
    Aguarde a propagação do DNS.

2.  **Instale o Certbot (para Let's Encrypt):**
    ```bash
    sudo apt install -y certbot python3-certbot-nginx
    ```
3.  **Obtenha os certificados SSL:**
    ```bash
    sudo certbot --nginx -d www.iahumanizada.com.br -d iahumanizada.com.br -d api.iahumanizada.com.br
    ```
    Siga as instruções na tela. Certbot modificará automaticamente sua configuração do Nginx para usar HTTPS e configurará a renovação automática.

4.  **Verifique a renovação automática (opcional):**
    ```bash
    sudo certbot renew --dry-run
    ```

### 5.9. Configurar Firewall (UFW)
```bash
sudo ufw allow 'Nginx Full' # Permite tráfego HTTP e HTTPS
sudo ufw allow OpenSSH
sudo ufw enable
sudo ufw status
```

### 5.10. Testar a Aplicação

Abra `https://www.iahumanizada.com.br` no seu navegador. Teste o registro, login e as funcionalidades da API (que agora deve ser acessível via `https://api.iahumanizada.com.br/api`).

## 6. Deploy na Hostinger (VPS)

Como mencionado, a Hostinger **requer um plano VPS** para hospedar aplicações Flask e Next.js. A hospedagem compartilhada não é adequada.

O processo de deploy em um VPS da Hostinger é **muito similar ao deploy em um VPS Ubuntu 20.04 genérico**, pois a Hostinger geralmente fornece acesso root aos seus VPS, permitindo que você instale e configure o ambiente conforme necessário.

### 6.1. Principais Passos e Considerações para Hostinger VPS:

1.  **Escolha um Plano VPS:** Adquira um plano VPS da Hostinger que atenda aos requisitos de recursos da sua aplicação.
2.  **Acesso SSH:** A Hostinger fornecerá credenciais e instruções para acessar seu VPS via SSH. Utilize-as para conectar.
3.  **Sistema Operacional:** Se possível, escolha Ubuntu 20.04 (ou uma versão LTS compatível) ao configurar seu VPS na Hostinger para seguir este guia mais de perto.
4.  **Siga as Seções 5.2 a 5.10 deste Manual:**
    *   Atualização do sistema e instalação de dependências (Nginx, Python, Node.js, PostgreSQL, etc.).
    *   Configuração do PostgreSQL no VPS.
    *   Clonagem do repositório.
    *   Configuração do backend Flask com Gunicorn e Supervisor.
    *   Configuração do frontend Next.js com PM2.
    *   Configuração do Nginx como proxy reverso.
    *   **Gerenciamento de DNS na Hostinger:** Ao chegar na etapa de configurar o domínio (Seção 5.8.1), você usará o painel de gerenciamento de DNS da Hostinger para apontar `iahumanizada.com.br`, `www.iahumanizada.com.br` e `api.iahumanizada.com.br` para o IP do seu VPS Hostinger.
    *   Configuração de SSL com Let's Encrypt (Certbot).
    *   Configuração do Firewall.

### 6.2. Diferenças Potenciais ou Pontos de Atenção na Hostinger:

*   **Painel de Controle da Hostinger (hPanel):** Embora a maior parte da configuração seja via SSH, o hPanel da Hostinger pode ser usado para gerenciamento de VPS (reiniciar, reinstalar SO), gerenciamento de DNS e, possivelmente, algumas configurações de firewall mais básicas (embora UFW via linha de comando seja mais granular).
*   **Firewall:** Verifique se a Hostinger aplica alguma camada de firewall externa ao VPS. Normalmente, você terá controle total sobre o firewall do SO (como UFW), mas é bom estar ciente.
*   **Recursos do VPS:** Monitore o uso de CPU, RAM e disco do seu VPS Hostinger, especialmente após o deploy, para garantir que o plano escolhido é adequado.

Em resumo, trate seu VPS Hostinger como um servidor Ubuntu padrão e siga as instruções detalhadas na Seção 5.

## 7. Considerações Finais e Solução de Problemas Comuns

*   **Logs:** Verifique sempre os logs do Nginx (`/var/log/nginx/`), Supervisor (`/var/log/supervisor/`), PM2 (`pm2 logs nome_da_app`), Gunicorn e da sua aplicação Flask para diagnosticar problemas.
*   **Permissões:** Erros de permissão são comuns. Garanta que o usuário que executa Gunicorn/PM2 e o Nginx tenham as permissões corretas para acessar os arquivos do projeto, sockets e logs.
*   **Variáveis de Ambiente:** Verifique se os arquivos `.env` e `.env.local` estão corretos e se as variáveis estão sendo carregadas adequadamente pelas aplicações.
*   **Conexão com Banco de Dados:** Teste a conexão com o banco de dados separadamente se encontrar problemas.
*   **Firewall:** Certifique-se de que o firewall (UFW ou da Hostinger) não está bloqueando as portas necessárias (80, 443).
*   **Build do Frontend:** Garanta que o build do Next.js (`pnpm build`) foi executado sem erros antes de tentar servir com PM2.

Este manual visa ser um guia completo. Adapte os comandos e configurações conforme a especificidade do seu ambiente e projeto.

