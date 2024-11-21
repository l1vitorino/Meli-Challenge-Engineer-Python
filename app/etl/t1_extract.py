import requests
import pandas as pd
import json
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

#TODO Inserir try & except para todas as funções
#TODO Ajustar o offset
#TODO Validar dados do paralelismo

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
        self.query = query
        self.sample = sample  # Quantidade de linhas que devem retornar, 0 retorna todas as linhas

    def _Get_Items(self):
        """
        Extrai itens da API do Mercado Livre.
        """
        api_limit = 50
        offset = 0
        results_rows = api_limit
        result = []

        while results_rows >= 50 and (offset <= self.sample or self.sample == 0):
            response = requests.get(f'{self.url}/sites/{self.site}/search?q={self.query}&offset={offset}&limit={api_limit}').content
            data = json.loads(response)["results"]
            result.extend(data)

            results_rows = len(data)
            offset = offset + results_rows + 1
            print(f'Página extraída de {offset - results_rows - 1} até {offset - 1}')

        dfItems = pd.DataFrame(result)
        return dfItems

    def _Get_Items_Detail_Inter(self, item_id):
        """
        Método auxiliar para buscar detalhes de um item.
        """
        try:
            response = json.loads(requests.get(f'{self.url}/items/{item_id}').content)
            #print(f'Item {item_id} extraído')
            return response
        except Exception as e:
            logging.error(f"Erro ao buscar detalhes do item {item_id}: {e}")
            return None

    def _Get_Items_Detail(self, dfItems):
        """
        Extrai detalhes dos itens usando paralelismo.
        Mais performatico seria utilizar a API em batch, entretanto não temos acesso: /items?ids=:ids
        """
        print('Extração dos itens iniciado')
        resultItems = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            # Envia requisições paralelas para buscar detalhes dos itens
            futures = {executor.submit(self._Get_Items_Detail_Inter, row['id']): row['id'] for _, row in dfItems.iterrows()}

            for future in as_completed(futures):
                item_id = futures[future]
                try:
                    result = future.result()
                    if result:
                        resultItems.append(result)
                except Exception as e:
                    logging.error(f"Erro ao processar item {item_id}: {e}")

        dfDetails = pd.json_normalize(resultItems)
        return dfDetails
    