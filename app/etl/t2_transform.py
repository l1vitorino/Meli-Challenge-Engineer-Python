import pandas as pd
import sys
import logging

# Configuração do logger
logging.basicConfig(filename='log/mercado_libre_transform.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class MercadoLibreTransform:
    """
    Classe para extrair e processar dados da API do Mercado Livre.
    """
    def __init__(self, df_items, df_items_detail):
        self.df_items = df_items
        self.df_items_detail = df_items_detail

    def _transform_items(self):
        """
        Transforma os dados do dataframe de itens.
        """
        try:
            sales_normalize = pd.json_normalize(self.df_items["sale_price"])
            self.df_items['sale_amount'] = sales_normalize['amount']
            self.df_items['sale_type'] = sales_normalize['type']
            self.df_items = self.df_items[
                ['id','Brand', 'condition', 'title', 'buying_mode', 'price', 
                 'original_price', 'sale_amount', 'sale_type', 
                 'available_quantity', 'accepts_mercadopago', 'use_thumbnail_id']
            ]
            return self.df_items
        except Exception as e:
            logging.error(f"Erro na transformação de itens: {e}")
            sys.exit()

    def _transform_detail_items(self):
        """
        Transforma os dados do dataframe de detalhes dos itens.
        """
        try:
            BRAND_attributes = []
            RAM_attributes = []
            RELEASE_YEAR_attributes = []

            for index, row in self.df_items_detail.iterrows():
                for attributes in row['attributes']:
                    BRAND_attributes.append( { "id": row['id'] ,  attributes['id']: attributes['values'][0]['name']} ) if attributes['id'] == 'BRAND' else '0'
                    RAM_attributes.append( { "id": row['id'] ,  attributes['id']: attributes['values'][0]['name']} ) if attributes['id'] == 'RAM' else '0'
                    RELEASE_YEAR_attributes.append( { "id": row['id'] ,  attributes['id']: attributes['values'][0]['name']} ) if attributes['id'] == 'RELEASE_YEAR' else '0'
           
            self.df_items_detail = pd.merge(self.df_items_detail, pd.DataFrame.from_dict(BRAND_attributes), on='id', how='left')
            self.df_items_detail = pd.merge(self.df_items_detail, pd.DataFrame.from_dict(RAM_attributes), on='id', how='left')
            self.df_items_detail = pd.merge(self.df_items_detail, pd.DataFrame.from_dict(RELEASE_YEAR_attributes), on='id', how='left')

            seller_address_normalize = pd.json_normalize(self.df_items_detail["seller_address"])
            
            self.df_items_detail['Seller_City'] = seller_address_normalize['city.name']
            self.df_items_detail['Seller_State'] = seller_address_normalize['state.name']
            self.df_items_detail['Seller_country'] = seller_address_normalize['country.name']

            self.df_items_detail = self.df_items_detail[
                ['id', 'health', 'Seller_City', 
                 'Seller_State','Seller_country','BRAND', 'RAM', 'RELEASE_YEAR']
            ]
            return self.df_items_detail.drop_duplicates()
        except Exception as e:
            logging.error(f"Erro na transformação de detalhes dos itens: {e}")
            sys.exit()

    def executor(self):
        """
        Executa as transformações e mescla os dataframes.
        """
        try:
            df1 = self._transform_items()
            df2 = self._transform_detail_items()
            result = pd.merge(df1, df2, on='id', how='left')
            return result
        except Exception as e:
            logging.error(f"Erro na execução do transformador: {e}")
            sys.exit()