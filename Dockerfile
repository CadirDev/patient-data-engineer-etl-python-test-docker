FROM python:3.10-slim

# Instalar dependências
RUN pip install --no-cache-dir \
    sqlalchemy \
    psycopg2-binary \
    python-dotenv

# Configurar diretório de trabalho
WORKDIR /app

# Copiar o código da aplicação
COPY . .

# Instalar dependências do projeto
RUN pip install -r requirements.txt

# Executar a aplicação
CMD ["python", "main.py"]
