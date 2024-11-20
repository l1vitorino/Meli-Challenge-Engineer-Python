import requests
import pandas as pd
import json
import logging

# Configuração do logger
logging.basicConfig(filename='MercadoLibreScraper.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class MercadoLibreScraper:
    """
    Classe para extrair e processar dados da API do Mercado Livre.
    """
    def __init__(self,site, query):
        self.url = 'https://api.mercadolibre.com'
        self.site = site
        self.query = query

    def GetItems(self):

        api_limit = 50
        offset = 0
        results_rows = api_limit
        result = []    

        while results_rows >= 50:
            response = requests.get(f'{self.url}/sites/{self.site}/search?q={self.query}&offset={offset}&limit={api_limit}#json').content
            data = json.loads(response)["results"]
            result.extend(data)

            results_rows = len(data)
            offset = offset + results_rows
            print(f'Página extraida de {offset - results_rows} até {offset}')
            
        dfItems = pd.DataFrame(result)
        return dfItems
    
    def GetItemnsDetail(self,dfItems):
        
        resultItems = []

        for index, row in dfItems.iterrows():
            response = json.loads(
                requests.get(f'{self.url}/items/{row['id']}#json').content
            )
            resultItems.append(response)
            print(f'Item {row['id']} extraido')
        dfItems = pd.json_normalize(resultItems)
        return dfItems