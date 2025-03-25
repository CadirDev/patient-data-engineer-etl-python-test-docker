from src.data_ingestion import ingestData  # Importa a função de ingestão de dados
from src.data_transformation import transformToFhir  # Importa a função de transformação de dados
from src.utils import createTables, generateYaml, engine  # Importa as funções auxiliares e o engine

def main():
    """
    Função principal do processo. Executa o processo de criação de tabelas, ingestão e transformação de dados.
    """
    # Criar tabelas no banco de dados (se não existirem)
    createTables()

    # Gerar a documentação em formato YAML
    generateYaml()

    # Ingerir os dados do CSV e carregá-los na tabela 'raw_patient'
    df = ingestData("patient.csv")

    # Transformar os dados para o formato FHIR
    dfFhir = transformToFhir(df)

    # Inserir os dados transformados na tabela 'fhir_patient'
    dfFhir.to_sql("fhir_patient", engine, if_exists="replace", index=False)

    # Mensagem de sucesso
    print("Processo concluído com sucesso.")

# Executar a função main quando o script for chamado diretamente
if __name__ == "__main__":
    main()