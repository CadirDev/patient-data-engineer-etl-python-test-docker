# Projeto ETL com PostgreSQL e Docker

Este projeto realiza um processo **ETL (Extract, Transform, Load)** para ingestão, transformação e carregamento de dados em um banco de dados **PostgreSQL** utilizando containers **Docker**. O objetivo é criar uma aplicação que seja capaz de ingerir dados a partir de um arquivo CSV, transformá-los no formato **FHIR** e armazená-los em um banco de dados PostgreSQL.

## Visão Geral

O processo de ETL do projeto é dividido em três etapas principais:

1. **Extração (Extract)**: Leitura dos dados a partir de um arquivo CSV.
2. **Transformação (Transform)**: Manipulação dos dados e transformação no formato **FHIR**.
3. **Carregamento (Load)**: Armazenamento dos dados transformados no banco de dados **PostgreSQL**.

### Estrutura do Projeto

- **Ingestão de Dados (ETL)**: A aplicação lê dados de um arquivo CSV e os armazena em uma tabela `raw_patient`.
- **Transformação de Dados**: Os dados são transformados para o formato **FHIR** antes de serem carregados na tabela `fhir_patient`.
- **Banco de Dados**: O PostgreSQL é usado para armazenar os dados.
- **Docker**: Docker Compose é utilizado para orquestrar os containers do PostgreSQL e da aplicação Python.
- **Testes Automatizados**: Utiliza **pytest** para garantir o funcionamento correto do processo ETL.

## Tecnologias Utilizadas

- **Python 3.10**: Linguagem de programação utilizada no projeto.
- **Pandas**: Para manipulação e transformação dos dados.
- **SQLAlchemy**: ORM para interação com o banco de dados PostgreSQL.
- **PostgreSQL**: Banco de dados relacional utilizado para armazenar os dados.
- **Docker**: Containerização da aplicação, incluindo o banco de dados e a aplicação Python.
- **pytest**: Framework de testes automatizados para garantir o funcionamento correto do projeto.
- **psycopg2-binary**: Conector do PostgreSQL para Python.

## Pré-requisitos

Antes de iniciar, certifique-se de ter as seguintes ferramentas instaladas:

- **Docker**: [Instruções para instalação](https://www.docker.com/get-started)
- **Docker Compose**: [Instruções para instalação](https://docs.docker.com/compose/install/)
- **Arquivo `patient.csv`**: Um arquivo CSV contendo os dados dos pacientes.

## Configuração do Ambiente

1. **Crie um arquivo `.env`** na raiz do projeto com as variáveis de ambiente necessárias para o banco de dados. Exemplo:

   ```env
   DB_NAME=DB_NAME
   DB_USER=DB _USER
   DB_PASSWORD=DB_PASSWORD
   DB_HOST=DB_HOST
   DB_PORT=DB_PORT

   # Banco de dados de testes
   DB_NAME_TEST=DB_NAME_TEST
   ```
