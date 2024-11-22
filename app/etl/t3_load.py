import pandas as pd
import logging
import sys

# Configuração do logger
logging.basicConfig(filename='log/mercado_libre_load.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class MercadoLibreLoad:
    """
    Classe para carregar os dados processados.
    """
    def __init__(self, df) -> None:
        self.df = df

    def _data_load(self):
        """
        Salva o DataFrame em um arquivo CSV.
        """
        try:
            self.df.to_csv('data/data.csv', index=False)
            print('Arquivo criado em: data/data.csv')
        except Exception as e:
            logging.error(f"Erro ao salvar o arquivo CSV: {e}")
            sys.exit()
