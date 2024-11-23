# **Meli-Challenge-Engineer-Python**

## **Descrição Geral**
O projeto **Meli-Challenge-Engineer-Python** é uma solução de ETL (Extract, Transform, Load) desenvolvida para interagir com a API do Mercado Livre. Ele permite a extração de dados de produtos, transformação e enriquecimento, e armazenamento em um formato apropriado para análises futuras. 

A abordagem modular e escalável visa facilitar o uso e a análise dos dados coletados, otimizando consultas e insights para tomada de decisão.

---

## **Estrutura Geral do Projeto**

![Diagrama de alto nivel](Diagrama_de_alto_nivel.png "Diagrama de alto nivel")

### **Diretórios e Arquivos**
1. **app/**
   - **ETL/**:
     - **t1_extract.py**: Responsável pela extração de dados.
     - **t2_transform.py**: Realiza o processamento e transformação dos dados extraídos.
     - **t3_load.py**: Carrega os dados transformados em um arquivo CSV.
     - **t4_pipeline.py**: Orquestra todas as etapas do pipeline ETL.
   - **exploratory_analysis/**:
     - **analysis.ipynb**: Caderno Jupyter para análise exploratória dos dados gerados pelo pipeline.

2. **Configuração e Dependências**:
   - **pyproject.toml** e **poetry.lock**: Gerenciamento de dependências usando o Poetry.
   - **gitignore.txt**: Arquivos e pastas ignorados pelo Git.
   - **README.md**: Este arquivo com a documentação completa do projeto.

3. **Log**:
   - Diretório com os arquivos de log gerados durante o pipeline:
     - `mercado_libre_scraper.log`
     - `mercado_libre_transform.log`
     - `mercado_libre_load.log`

4. **Data**:
   - **data.csv**: Arquivo resultante do pipeline, com os dados processados e prontos para análise.

---

## **Pipeline ETL**

O pipeline ETL segue três etapas principais: extração, transformação e carregamento.
Devemos apenas passar as informações para a primeira etapa de extração
1. site (str): O site é de qual país estamos extraindo as informações, no scrip está por default MLB (Brasil), mas pode ser inserido MBA (Argentina), CUP (Cuba), entre outros, podemos analisar todos nesse aqui https://api.mercadolibre.com/sites/;
2. query(str): A query são os itens que desejamos iterar e retornar, a separação deve ser feita por virgula ',';
3. sample(int): Por fim temos o tamanho do sample que desejamos retornar por item dentro da query, algumas informações importantes são:
    1. A API publica do mercado livre tem uma limitação de 1000 resultados por pesquisa;
    2. Extrações pesadas pode finalizar em timeout.

### **1. Extração**
A extração utiliza a classe `MercadoLibreScraper` para coletar dados da API do Mercado Livre. Os produtos e seus detalhes são extraídos com base em palavras-chave (ex.: marcas) fornecidas pelo usuário. A classe também suporta paralelismo para otimizar a coleta dos dados.

---

### **2. Transformação**
A transformação é realizada pela classe `MercadoLibreTransform`, responsável por normalizar, processar e enriquecer os dados extraídos. Essa etapa organiza as informações para torná-las adequadas para análises futuras.

#### **Etapas de Transformação**
1. Transformação dos itens básicos (`_transform_items`).
2. Enriquecimento dos itens com atributos detalhados (`_transform_detail_items`).
3. Combinação dos DataFrames resultantes.

---

### **3. Carregamento**

A etapa de carregamento é a fase final do pipeline ETL. Utilizando a classe `MercadoLibreLoad`, os dados processados são salvos em um arquivo `.csv`, permitindo fácil acesso para análises e uso posterior.

#### Detalhes

- O arquivo gerado é salvo no diretório `data/` com o nome `data.csv`.
- O formato CSV foi escolhido por ser amplamente utilizado e facilmente integrável com ferramentas de análise de dados.

---

## Rodando o projeto

### Pré-requisitos

* **VSCode**: Ou outro editor de código. [Instruções de instalação do VSCode aqui](https://code.visualstudio.com/download).

* **Pyenv**: É usado para gerenciar versões do Python. [Instruções de instalação do Pyenv aqui](https://github.com/pyenv/pyenv#installation). Vamos usar nesse projeto o Python 3.12.1.

* **Poetry**: Este projeto utiliza Poetry para gerenciamento de dependências. [Instruções de instalação do Poetry aqui](https://python-poetry.org/docs/#installation).


### Instalação e Configuração

1. Clone o repositório para a sua máquina


2. Configure a versão correta do Python com `pyenv`:

```bash
pyenv install 3.12.1
pyenv local 3.12.1
```

3. Configurar poetry para Python version 3.11.5 e ative o ambiente virtual:

```bash
poetry env use 3.12.1
poetry shell
```

4. Instale as dependencias do projeto:

```bash
poetry install
```

5. Aba o scrip pipeline.py e rode