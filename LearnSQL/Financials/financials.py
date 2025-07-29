import requests 
import sqlite3 
import os 
from dotenv import load_dotenv 
from polygon import RESTClient 

load_dotenv() 
api_key = os.getenv('POLYGON_API_KEY') 

url = os.getenv('FINANCIALS_URL') 
client = RESTClient(api_key) 

# 2. Function definition (defines the function but doesn't run it yet)
def get_all_financial_statements(ticker):
    """Pull all financial statement data and return as Python dictionaries"""
    
    # Make API call
    response = client.get( + f"?ticker={ticker}")
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
            financials = client.vx.list_stock_financials('financials', {})
            
            # Extract all four financial statements as-is
            period_data['balance_sheet'] = financials.get('balance_sheet', {})
            period_data['income_statement'] = financials.get('income_statement', {})
            period_data['cash_flow_statement'] = financials.get('cash_flow_statement', {})
            period_data['comprehensive_income'] = financials.get('comprehensive_income', {})
            
            all_periods.append(period_data)
    
    return all_periods

# 3. This is where execution actually happens (when you run the file)
ticker = str(input("Enter a Ticker Symbol: "))
financial_data = get_all_financial_statements(ticker)  # <- API call happens HERE

print(ticker) 