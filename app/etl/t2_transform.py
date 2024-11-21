import pandas as pd
import logging

#TODO Inserir try & except para todas as funções
#TODO Trazer Marca

class MercadoLibreTransform:
    """
    Classe para extrair e processar dados da API do Mercado Livre.
    """
    def __init__(self,dfItems, dfItemsDetail):
        self.dfItems = dfItems
        self.dfItemsDetail = dfItemsDetail

    def _transform_items(self):
        #Items
        SalesNormalize = pd.json_normalize(self.dfItems["sale_price"])
        self.dfItems['sale_amount'] =  SalesNormalize['amount']
        self.dfItems['sale_type'] =  SalesNormalize['type']
        self.dfItems = self.dfItems[['id','condition', 'title', 'buying_mode','price','original_price', 'sale_amount', 'sale_type', 'available_quantity', 'accepts_mercadopago', 'use_thumbnail_id']]
        return self.dfItems
    
    def _transform_detail_items(self): 
         self.dfItemsDetail = self.dfItemsDetail[['id', 'health', 'seller_address.search_location.city.name','seller_address.search_location.state.name']]
         return self.dfItemsDetail
    
    def executor(self,): 
        df1 = self._transform_items()
        df2 = self._transform_detail_items()
        result = pd.merge(df1, df2, on= 'id', how='left' )
        return result
