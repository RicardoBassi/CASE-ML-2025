FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Setar o diretório de trabalho no contêiner
WORKDIR /app

# Copiar os arquivos de requisitos para o contêiner
COPY requirements-api.txt /app/

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements-api.txt

# Copiar o restante dos arquivos do projeto
COPY . /app/

# Expor a porta do Django
EXPOSE 8000

# Comando para rodar o servidor Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]