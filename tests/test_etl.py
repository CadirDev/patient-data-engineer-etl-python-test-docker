import pytest
from sqlalchemy import text
from src.utils import TEST_ENGINE
from src.utils import createTables

@pytest.fixture(scope="module")
def setup_database():
    """Fixture para configurar o banco de dados antes dos testes e limpar após."""
    # Limpar tabelas existentes antes de criar novas
    with TEST_ENGINE.connect() as connection:
        # Tentar remover tabelas se elas existirem
        connection.execute(text("DROP TABLE IF EXISTS raw_patient"))
        connection.execute(text("DROP TABLE IF EXISTS fhir_patient"))
    
    # Criar as tabelas
    createTables()

    # Yield para garantir que os testes sejam executados após a criação
    yield

    # Limpar as tabelas após os testes
    with TEST_ENGINE.connect() as connection:
        connection.execute(text("DROP TABLE IF EXISTS raw_patient"))
        connection.execute(text("DROP TABLE IF EXISTS fhir_patient"))

def test_create_tables(setup_database):
    """Testar se as tabelas raw_patient e fhir_patient foram criadas com sucesso."""
    with TEST_ENGINE.connect() as connection:
        # Verificar se a tabela 'raw_patient' existe no banco de dados, incluindo o esquema 'public'
        result = connection.execute(text("""
            SELECT 1
            FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_name = 'raw_patient'
        """))
        assert result.fetchone() is not None, "Tabela 'raw_patient' não foi criada"

        # Verificar se a tabela 'fhir_patient' existe no banco de dados, incluindo o esquema 'public'
        result = connection.execute(text("""
            SELECT 1
            FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_name = 'fhir_patient'
        """))
        assert result.fetchone() is not None, "Tabela 'fhir_patient' não foi criada"