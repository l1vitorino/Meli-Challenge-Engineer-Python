import pandas as pd
import logging

#TODO Inserir try & except para todas as funções

class MercadoLibreLoad:
    def __init__(self, df) -> None:
        self.df = df
    def _data_load(self):
        self.df.to_csv('data/data.csv', index= False)
        print('Arquivo criado em: data/data.csv')

