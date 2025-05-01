# API Django para Predição de Carga de Aquecimento e Resfriamento

Este repositório contém uma API Django para realizar predições de carga de aquecimento e resfriamento com base em um modelo de regressão previamente treinado.

## Índice

1. [Configuração do Ambiente](#configuração-do-ambiente)
   - [Opção 1: Usando Conda](#opção-1-usando-conda)
   - [Opção 2: Usando Virtualenv](#opção-2-usando-virtualenv)
2. [Configuração do Banco de Dados PostgreSQL](#configuração-do-banco-de-dados-postgresql)
3. [Executando a API Localmente](#executando-a-api-localmente)
4. [Rodando a API com Docker Compose](#rodando-a-api-com-docker-compose)
5. [Comandos Úteis](#comandos-úteis)
6. [Considerações Finais](#considerações-finais)

---

## 1. Configuração do Ambiente

### Opção 1: Usando Conda

1. **Instale o Miniconda ou Anaconda**:
   - Baixe e instale o Miniconda ou Anaconda.

2. **Crie um Ambiente Conda**:
   conda create --name api-env python=3.10

3. **Ative o Ambiente**:
   conda activate api-env

4. **Instale as Dependências**:
   - Navegue para o diretório raiz do projeto (CASE-ML-2025).
   - Execute o comando:
     pip install -r requirements.txt

5. **Verifique a Instalação**:
   - Verifique se o Django foi instalado corretamente:
     python -m django --version

### Opção 2: Usando Virtualenv

1. **Instale o Virtualenv**:
   - Se ainda não tiver o `virtualenv` instalado, execute:
     pip install virtualenv

2. **Crie um Ambiente Virtual**:
   virtualenv venv

3. **Ative o Ambiente**:
   - **No Linux/MacOS**:
     source venv/bin/activate
   - **No Windows**:
     venv\Scripts\activate

4. **Instale as Dependências**:
   - Navegue para o diretório raiz do projeto (CASE-ML-2025).
   - Execute o comando:
     pip install -r requirements.txt

5. **Verifique a Instalação**:
   - Verifique se o Django foi instalado corretamente:
     python -m django --version

---

## 2. Configuração do Banco de Dados PostgreSQL

1. **Instale o PostgreSQL**:
   - **No Linux**:
     sudo apt update
     sudo apt install postgresql postgresql-contrib
   - **No MacOS (via Homebrew)**:
     brew install postgresql
   - **No Windows**: Faça o download e instale o PostgreSQL a partir do site oficial.

2. **Crie um Banco de Dados**:
   - Acesse o PostgreSQL:
     sudo -u postgres psql
   - Execute os seguintes comandos para criar o banco de dados:
     CREATE DATABASE nome_do_banco;
     CREATE USER usuario WITH PASSWORD 'senha';
     GRANT ALL PRIVILEGES ON DATABASE nome_do_banco TO usuario;
     \q

3. **Configure o Arquivo `settings.py`**:
   - Atualize as configurações do banco de dados no arquivo `settings.py`:
     ```python
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.postgresql',
             'NAME': 'nome_do_banco',
             'USER': 'usuario',
             'PASSWORD': 'senha',
             'HOST': 'localhost',
             'PORT': '5432',
         }
     }
     ```

---

## 3. Executando a API Localmente

1. **Aplique as Migrações**:
   python manage.py makemigrations
   python manage.py migrate

2. **Crie um Superusuário**:
   python manage.py createsuperuser

3. **Execute o Servidor de Desenvolvimento**:
   python manage.py runserver

4. **Acesse a API**:
   - Acesse a documentação Swagger em:
     http://localhost:8000/swagger/

5. **Acesse a API pelo frontend**:
     http://localhost:8000/

---

## 4. Rodando a API com Docker Compose

### Pré-requisitos
Instale o Docker e o Docker Compose.

### Passo a Passo

1. **Construa e Inicie os Containers**:
   - Navegue para o diretório que contém a API (DjangoAPI). Esse diretório contém os arquivos necessários para a execução do container.
     docker-compose --build
   - Aguarde o download e instalação do container. Após finalizar execute:
     docker-compose up

2. **Aplique as Migrações no Container**:
   - Em um novo terminal, execute:
     docker-compose exec web python manage.py makemigrations
     docker-compose exec web python manage.py migrate

3. **Crie um Superusuário**:
   docker-compose exec web python manage.py createsuperuser

4. **Acesse a API**:
   - Acesse a documentação Swagger em:
     http://localhost:8000/swagger/

---

## 5. Comandos Úteis

1. **Parar os Containers**:
   docker-compose down

2. **Reconstruir os Containers**:
   docker-compose up --build

3. **Acessar o Shell do Django**:
   docker-compose exec web python manage.py shell

4. **Limpar Dados do PostgreSQL**:
   docker-compose down -v

---

## 6. Considerações Finais

Este guia fornece instruções completas para configurar e executar a API localmente ou em um ambiente Docker. Certifique-se de ajustar as configurações do banco de dados (settings.py) conforme necessário. 
