import pandas as pd
from extract import MercadoLibreScraper

Scraper = MercadoLibreScraper('MLB', 'ultrabook+corei7+16gb')
dfItems = Scraper.GetItems()
dfItemsDetail = Scraper.GetItemnsDetail(dfItems)

#Items
SalesNormalize = pd.json_normalize(dfItems["sale_price"])
dfItems['sale_amount'] =  SalesNormalize['amount']
dfItems['sale_type'] =  SalesNormalize['type']
df = dfItems[['id','condition', 'title', 'buying_mode','price','original_price', 'sale_amount', 'sale_type', 'available_quantity', 'accepts_mercadopago', 'use_thumbnail_id']]

#ItemsDetail
print(   dfItems['attributes'] )
