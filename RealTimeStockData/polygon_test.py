import os 
import requests 
import pandas as pd 
import matplotlib 
import math 
from requests.adapters import HTTPAdapter 
from urllib3.util.retry import Retry
from dotenv import load_dotenv 
from polygon import RESTCLIENT 


load_dotenv() 
api_key = os.getenv("POLYGON_API_KEY") 
client = RESTClient(api_key) 

url = "/v3/reference/tickers/{ticker}" 


ticker = str(input("Enter the Stock Ticker: ")) 
