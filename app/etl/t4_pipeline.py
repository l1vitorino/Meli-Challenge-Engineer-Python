from t1_extract import MercadoLibreScraper
from t2_transform import MercadoLibreTransform
from t3_load import MercadoLibreLoad

#Extract
Scraper = MercadoLibreScraper('MLB','Xiaomi,Iphone,Samsung', 2400) #Maximum allowed is 1000 for public users.
dfItems = Scraper._get_items()
dfItemsDetail = Scraper._get_item_details(dfItems)

#Transform
transform = MercadoLibreTransform(dfItems,dfItemsDetail)
df = transform.executor()

#Load
load = MercadoLibreLoad(df)
load._data_load()