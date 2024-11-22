from t1_extract import MercadoLibreScraper
from t2_transform import MercadoLibreTransform
from t3_load import MercadoLibreLoad

#Extract
Scraper = MercadoLibreScraper('MLB', 'Alexa, Google Assistente', 500)
dfItems = Scraper._Get_Items()
# dfItemsDetail = Scraper._Get_Items_Detail(dfItems)

# #Transform
# transform = MercadoLibreTransform(dfItems,dfItemsDetail)
# df = transform.executor()

# #Load
# load = MercadoLibreLoad(df)
# load._data_load()