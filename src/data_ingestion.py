import pandas as pd  # Biblioteca para manipulação de dados em formato de tabela
from sqlalchemy import create_engine  # Biblioteca para criar conexão com banco de dados SQL
import os  # Biblioteca para manipulação de variáveis de ambiente
import re  # Expressões regulares para validação de email
from dotenv import load_dotenv  # Carregar variáveis de ambiente do arquivo .env

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração do banco de dados, extraída das variáveis de ambiente
dbName = os.getenv("DB_NAME")
dbUser = os.getenv("DB_USER")
dbPassword = os.getenv("DB_PASSWORD")
dbHost = os.getenv("DB_HOST")
dbPort = os.getenv("DB_PORT")

# Criando a conexão com o banco de dados PostgreSQL utilizando SQLAlchemy
engine = create_engine(f'postgresql://{dbUser}:{dbPassword}@{dbHost}:{dbPort}/{dbName}')

def ingestData(csvFile):
    """
    Função responsável por ler dados de um arquivo CSV e carregá-los na tabela raw_patient no banco de dados.
    Também realiza o pré-processamento de dados antes da ingestão.
    """
    # Carregando os dados do arquivo CSV para um DataFrame pandas
    df = pd.read_csv(csvFile)

    # Tratando valores ausentes (substituindo valores ausentes por valores padrão)
    df['birth_date'].fillna('1900-01-01', inplace=True)  # Substitui valores ausentes em 'birth_date'
    df['address'].fillna('Unknown', inplace=True)  # Substitui valores ausentes em 'address'

    # Função para validar o formato de email utilizando expressões regulares
    def isValidEmail(email):
        return bool(re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA0-9-]+\.[a-zA-Z0-9-.]+$", str(email)))

    # Remover registros com e-mails inválidos
    df = df[df['email'].apply(isValidEmail)]

    # Carregar os dados limpos na tabela raw_patient no banco de dados
    df.to_sql("raw_patient", engine, if_exists="replace", index=False)
    
    return df  # Retorna o DataFrame limpo