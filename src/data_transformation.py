import pandas as pd  # Biblioteca para manipulação de dados em formato de tabela
import json  # Biblioteca para manipulação de dados em formato JSON

def transformToFhir(df):
    """
    Função responsável por transformar os dados do DataFrame para o formato FHIR.
    O formato FHIR é um padrão para dados de saúde.
    """
    # Função interna que transforma uma linha do DataFrame para o formato FHIR
    def transformRow(row):
        return {
            "id": f"{row['first_name']}{row['last_name']}{row['birth_date']}",  # Geração de ID único baseado em nome e data de nascimento
            "full_name": f"{row['first_name']} {row['last_name']}",  # Criação do nome completo
            "birth_date": row['birth_date'],  # Mantém a data de nascimento
            "gender": row['gender'],  # Mantém o gênero
            "address": row['address'],  # Mantém o endereço
            "telecom": json.dumps({"phone": row['phone_number'], "email": row['email']}),  # Dados de contato em formato JSON
            "marital_status": row['marital_status'],  # Estado civil
            "insurance_number": row['insurance_number'],  # Número do seguro de saúde
            "nationality": row['nationality']  # Nacionalidade
        }

    # Aplica a transformação em todas as linhas do DataFrame
    dfFhir = df.apply(transformRow, axis=1)

    # Converte a lista de dicionários para um DataFrame novamente
    dfFhir = pd.DataFrame(dfFhir.tolist()) 

    return dfFhir  # Retorna o DataFrame transformado