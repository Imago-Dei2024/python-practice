import os 
from dotenv import load_dotenv 
from polygon import RESTCLIENT 


load_dotenv() 
api_key = os.getenv("POLYGON_API_KEY") 
client = RESTClient(api_key) 

stock_symbol = str(input("Enter the Stock Ticker: ")) 
