import requests
import pandas as pd
import json
import logging
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuração do logger
logging.basicConfig(filename='log/mercado_libre_scraper.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class MercadoLibreScraper:
    """
    Classe para extrair e processar dados da API do Mercado Livre.
    """
    def __init__(self, site: str, query: str, sample: int):
        self.url = 'https://api.mercadolibre.com'
        self.site = site
        self.query = query.split(',')
        self.sample = int(round(sample / len(query.split(',')), 0))  # Quantidade de linhas que devem retornar, 0 retorna todas as linhas

    def _get_items(self) -> pd.DataFrame:
        """
        Extrai itens da API do Mercado Livre.
        """
        result = []

        for query_item in self.query:
            print(f'Extraindo item {query_item} 🚀 com {self.sample} exemplos')
            offset = 0
            api_limit = 50
            intermediate_results = []
            results_rows = api_limit
            while results_rows >= 1 and offset < self.sample:
                try:
                    response = requests.get(f'{self.url}/sites/{self.site}/search?q={query_item}&offset={offset}&limit={api_limit}')
                    response.raise_for_status()  # Lança exceção para status HTTP >= 400                    
                    data = response.json().get("results", [])  # Carrega o JSON e garante que results existe
                    intermediate_results.extend(data)
                    offset += len(data)  # Incrementa o offset com base no número de resultados retornados

                except Exception as e:
                    logging.error(f"{"Erro na requisição" if isinstance(e, requests.RequestException) else "Erro inesperado"}: {e}")
                    sys.exit()

            result.extend(intermediate_results[:self.sample])

        df_items = pd.DataFrame(result)
        return df_items

    def _get_item_details_internal(self, item_id):
        """
        Método auxiliar para buscar detalhes de um item.
        """
        response = requests.get(f'{self.url}/items/{item_id}')
        response.raise_for_status()  # Lança exceção para status HTTP >= 400
        data = response.json()
        print(f'Item {item_id} extraído')
        return data

    def _get_item_details(self, df_items) -> pd.DataFrame:
        """
        Extrai detalhes dos itens usando paralelismo.
        Mais performático seria utilizar a API em batch, entretanto não temos acesso: /items?ids=:ids
        """
        result_items = []
        try:
            with ThreadPoolExecutor(max_workers=10) as executor:
                futures = {
                    executor.submit(self._get_item_details_internal, row['id']): row['id']
                    for _, row in df_items.iterrows()
                }

                for future in as_completed(futures):
                    item_id = futures[future]
                    try:
                        result = future.result()
                        if result:
                            result_items.append(result)
                    except Exception as e:
                        logging.error(f"Erro ao processar item {item_id}: {e}")
                        print(f"Erro ao processar item {item_id}: {e}")
                        sys.exit()

            df_details = pd.json_normalize(result_items)
            return df_details
        except Exception as e:
            logging.error(f"{"Erro na requisição" if isinstance(e, requests.RequestException) else "Erro no processamento paralelo dos itens"}: {e}")
            sys.exit()
