import requests 
import sqlite3 
import os 
from dotenv import load_dotenv 
from polygon import RESTClient

load_dotenv() 
api_key = os.getenv("POLYGON_API_KEY") 
tickers_url = os.getenv("TICKERS_URL") 
ticker_overview_url = os.getenv("TICKER_OVERVIEW_URL") 
related_tickers_url = os.getenv("RELATED_TICKERS") 
financials_url = os.getenv("FINANCIALS_URL") 
short_interest_url = os.getenv("SHORT_INTEREST_URL") 
short_volume_url = os.getenv("SHORT_VOLUME_URL") 
market_movers_url = os.getenv("TOP_MOVERS_URL")
market_snapshot_url = os.getenv("FULL_MARKET_SNAPSHOT_URL")
client = RESTClient(api_key) 

url = 'https://api.polygon.io/v3/reference/tickers/AAPL?apiKey=tADjUt359vPx3_KmsmYEgB9V5OmWxTXe'   

ticker = str(input("Enter a Ticker Symbol: "))

overview = client.get_ticker_details(
    (ticker)
) 

relatedTickers = client.get_related_companies( 
    (ticker) 
) 

def get_all_financial_statements(ticker):
    """Pull all financial statement data and return as Python dictionaries"""
    
    # Make API call
    response = client.get(financials_url + f"?ticker={ticker}")
    data = response.json()
    
    all_periods = []
    
    if data.get('status') == 'OK' and 'results' in data:
        for financial_record in data['results']:
            
            # Basic company/period info
            period_data = {
                'company_name': financial_record.get('company_name'),
                'cik': financial_record.get('cik'), 
                'ticker': ticker,
                'fiscal_period': financial_record.get('fiscal_period'),
                'fiscal_year': financial_record.get('fiscal_year'),
                'timeframe': financial_record.get('timeframe'),
                'filing_date': financial_record.get('filing_date'),
                'end_date': financial_record.get('end_date'),
            }
            
            # Get the financials object
            financials = financial_record.get('financials', {})
            
            # Extract all four financial statements as-is
            period_data['balance_sheet'] = financials.get('balance_sheet', {})
            period_data['income_statement'] = financials.get('income_statement', {})
            period_data['cash_flow_statement'] = financials.get('cash_flow_statement', {})
            period_data['comprehensive_income'] = financials.get('comprehensive_income', {})
            
            all_periods.append(period_data)
    
    return all_periods

# Usage
financial_data = get_all_financial_statements(ticker)


print(ticker) 
print(overview)  
print(relatedTickers)
