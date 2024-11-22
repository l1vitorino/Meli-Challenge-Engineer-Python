import requests
import pandas as pd
import json
import logging
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuração do logger
logging.basicConfig(filename='MercadoLibreScraper.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class MercadoLibreScraper:
    """
    Classe para extrair e processar dados da API do Mercado Livre.
    """
    def __init__(self, site, query, sample):
        self.url = 'https://api.mercadolibre.com'
        self.site = site
        self.query = query.split(',')
        self.sample = int(round(sample / len(query.split(',')),0))   # Quantidade de linhas que devem retornar, 0 retorna todas as linhas

    def _Get_Items(self):
        """
        Extrai itens da API do Mercado Livre.
        """
        result = []

        for i in self.query:
            print(f'Extraindo item {i} 🚀 com {self.sample} exemplos')
            offset = 0
            api_limit = 50
            resultado_intermediario = []
            results_rows = api_limit
            while results_rows >= 1 and offset < self.sample :
                try:
                    response = requests.get(
                        f'{self.url}/sites/{self.site}/search?q={i}&offset={offset}&limit={api_limit}'
                    )
                    
                    # Verifica o código de status HTTP
                    if response.status_code == 200:
                        data = response.json().get("results", [])  # Carrega o JSON e garante que results existe
                        resultado_intermediario.extend(data)

                        results_rows = len(data)
                        offset += results_rows  # Incrementa o offset com base no número de resultados retornados
                    else:
                        logging.error(f"Erro na requisição: {response.status_code} - {response.reason}")
                        print(f"Erro na requisição: {response.status_code} - {response.reason}")
                        sys.exit()
                except requests.RequestException as e:
                    logging.error(f"Erro ao realizar a requisição: {e}")
                    print(f"Erro ao realizar a requisição: {e}")
                    sys.exit()  # Em caso de erro, interrompe o loop
                except Exception as e:
                    logging.error(f"Erro inesperado: {e}")
                    print(f"Erro inesperado: {e}")
                    sys.exit()
            result.extend(resultado_intermediario[:self.sample])

        dfItems = pd.DataFrame(result)
        return dfItems

    def _Get_Items_Detail_Inter(self, item_id):
        """
        Método auxiliar para buscar detalhes de um item.
        """
        try:
            response = requests.get(f'{self.url}/items/{item_id}')
            response.raise_for_status()  # Lança exceção para status HTTP >= 400
            data = response.json()
            print(f'Item {item_id} extraído')
            return data
        except requests.RequestException as e:
            logging.error(f"Erro ao buscar detalhes do item {item_id}: {e}")
            print(f"Erro ao buscar detalhes do item {item_id}: {e}")
            return None
        except Exception as e:
            logging.error(f"Erro inesperado ao buscar detalhes do item {item_id}: {e}")
            print(f"Erro inesperado ao buscar detalhes do item {item_id}: {e}")
            return None

    def _Get_Items_Detail(self, dfItems):
        """
        Extrai detalhes dos itens usando paralelismo.
        Mais performático seria utilizar a API em batch, entretanto não temos acesso: /items?ids=:ids
        """
        resultItems = []
        try:
            with ThreadPoolExecutor(max_workers=10) as executor:
                futures = {
                    executor.submit(self._Get_Items_Detail_Inter, row['id']): row['id']
                    for _, row in dfItems.iterrows()
                }

                for future in as_completed(futures):
                    item_id = futures[future]
                    try:
                        result = future.result()
                        if result:
                            resultItems.append(result)
                    except Exception as e:
                        logging.error(f"Erro ao processar item {item_id}: {e}")
                        print(f"Erro ao processar item {item_id}: {e}")

            dfDetails = pd.json_normalize(resultItems)
            return dfDetails
        except Exception as e:
            logging.error(f"Erro no processamento paralelo dos itens: {e}")
            print(f"Erro no processamento paralelo dos itens: {e}")
            return pd.DataFrame()  # Retorna um DataFrame vazio em caso de erro
