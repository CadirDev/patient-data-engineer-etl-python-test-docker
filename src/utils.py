from sqlalchemy import create_engine, text  # Para manipulação do banco de dados e execução de queries SQL
import os  # Para manipulação de variáveis de ambiente
from dotenv import load_dotenv  # Carregar variáveis de ambiente do arquivo .env
import yaml  # Para gerar a documentação no formato YAML

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração do banco de dados, extraída das variáveis de ambiente
dbName = os.getenv("DB_NAME")
dbUser = os.getenv("DB_USER")
dbPassword = os.getenv("DB_PASSWORD")
dbHost = os.getenv("DB_HOST")
dbPort = os.getenv("DB_PORT")

#teste
dbNameTeste = os.getenv("DB_NAME_TEST")

# Criando a conexão com o banco de dados
engine = create_engine(f'postgresql://{dbUser}:{dbPassword}@{dbHost}:{dbPort}/{dbName}')
TEST_ENGINE = create_engine(f'postgresql://{dbUser}:{dbPassword}@{dbHost}:{dbPort}/{dbNameTeste}')

def createTables():
    """
    Função responsável por criar as tabelas no banco de dados caso elas não existam.
    """
    try:
        with engine.connect() as connection:
            print("Criando tabela 'raw_patient'...")
            connection.execute(text('''CREATE TABLE IF NOT EXISTS raw_patient (
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(100),
                last_name VARCHAR(100),
                birth_date DATE,
                gender VARCHAR(20),
                address VARCHAR(255),
                city VARCHAR(100),
                state VARCHAR(2),
                zip_code VARCHAR(10),
                phone_number VARCHAR(20),
                email VARCHAR(100),
                emergency_contact_name VARCHAR(200),
                emergency_contact_phone VARCHAR(20),
                blood_type VARCHAR(5),
                insurance_provider VARCHAR(100),
                insurance_number VARCHAR(50),
                marital_status VARCHAR(20),
                preferred_language VARCHAR(50),
                nationality VARCHAR(100),
                allergies TEXT,
                last_visit_date DATE,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );'''))
            print("Tabela 'raw_patient' criada com sucesso.")

            print("Criando tabela 'fhir_patient'...")
            connection.execute(text('''CREATE TABLE IF NOT EXISTS fhir_patient (
                id VARCHAR(255) PRIMARY KEY,
                full_name VARCHAR(200),
                birth_date DATE,
                gender VARCHAR(20),
                address VARCHAR(255),
                telecom JSONB,  -- Campo JSON contendo telefone e email
                marital_status VARCHAR(20),
                insurance_number VARCHAR(255),
                nationality VARCHAR(20)
            );'''))
            print("Tabela 'fhir_patient' criada com sucesso.")

            # Adicionando verificação de tabelas após criação
            print("Verificando as tabelas no banco de dados...")
            result = connection.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"))
            tables = result.fetchall()
            print("Tabelas no banco de dados:")
            for table in tables:
                print(table[0])

    except Exception as e:
        print(f"Erro ao criar as tabelas: {e}")


def generateYaml():
    """
    Função responsável por gerar a documentação das tabelas em formato YAML.
    """
    data_assets = {
        "raw_patient": {
            "description": """
                Tabela contendo os dados brutos dos pacientes, diretamente importados do CSV fornecido. 
                Esta tabela contém informações pessoais, dados de contato, informações médicas e dados de seguro dos pacientes antes de qualquer transformação.
            """,
            "columns": {
                "id": "Identificador único do paciente (chave primária).",
                "first_name": "Primeiro nome do paciente.",
                "last_name": "Sobrenome do paciente.",
                "birth_date": "Data de nascimento do paciente.",
                "gender": "Gênero do paciente.",
                "address": "Endereço residencial do paciente.",
                "city": "Cidade onde o paciente reside.",
                "state": "Estado onde o paciente reside.",
                "zip_code": "Código postal do paciente.",
                "phone_number": "Número de telefone do paciente.",
                "email": "Endereço de email do paciente.",
                "emergency_contact_name": "Nome da pessoa de contato em caso de emergência.",
                "emergency_contact_phone": "Telefone da pessoa de contato em caso de emergência.",
                "blood_type": "Tipo sanguíneo do paciente.",
                "insurance_provider": "Fornecedor de seguro saúde do paciente.",
                "insurance_number": "Número do seguro de saúde do paciente.",
                "marital_status": "Estado civil do paciente.",
                "preferred_language": "Idioma preferido pelo paciente.",
                "nationality": "Nacionalidade do paciente.",
                "allergies": "Lista de alergias do paciente.",
                "last_visit_date": "Data da última visita do paciente.",
                "created_at": "Data e hora da criação do registro.",
                "updated_at": "Data e hora da última atualização do registro."
            },
            "tests": [
                "Verificar se todas as colunas obrigatórias estão presentes.",
                "Validar se os emails possuem um formato correto.",
                "Garantir que nenhum campo crítico está vazio após a ingestão."
            ]
        },
        "fhir_patient": {
            "description": """
                Tabela transformada para o formato FHIR, contendo os dados essenciais do paciente organizados de maneira padronizada 
                para interoperabilidade no setor de saúde. A tabela inclui um identificador único, nome completo, dados de contato no formato JSON e outras informações essenciais.
            """,
            "columns": {
                "id": "Identificador único gerado a partir dos atributos do paciente.",
                "full_name": "Nome completo do paciente (primeiro nome + sobrenome).",
                "birth_date": "Data de nascimento do paciente.",
                "gender": "Gênero do paciente.",
                "address": "Endereço do paciente.",
                "telecom": "Campo JSON contendo informações de contato, incluindo telefone e email.",
                "marital_status": "Estado civil do paciente.",
                "insurance_number": "Número do seguro de saúde do paciente.",
                "nationality": "Nacionalidade do paciente."
            },
            "tests": [
                "Verificar se o campo telecom contém um JSON válido.",
                "Assegurar que o nome completo foi corretamente concatenado.",
                "Garantir que o identificador único está sendo gerado corretamente."
            ]
        }
    }

    # Salvando documentação YAML em um arquivo com codificação UTF-8
    with open("data_assets.yaml", "w", encoding="utf-8") as file:
        yaml.dump(data_assets, file, default_flow_style=False, allow_unicode=True)