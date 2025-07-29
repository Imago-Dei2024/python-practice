import os 
from dotenv import load_dotenv 
import requests 
from polygon import RESTClient 
import time 

time.sleep(1) 

load_dotenv() 
api_key = os.getenv('POLYGON_API_KEY') 
base_url = 'https://api.polygon.io/vX/reference/financials' 
client = RESTClient(api_key) 

ticker = str(input("Enter a Ticker Symbol: "))

financials = [] 
for f in client.vx.list_stock_financials( 
    timeframe = "annual", 
    order = "asc", 
    limit = "1", 
    sort = "filing_date",
    ):
    financials.append(f) 

print(financials)  
    