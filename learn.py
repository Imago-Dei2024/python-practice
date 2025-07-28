
import yfinance as yf  
import pandas as pd 
import sqlite3 

def fetch_financial_data(ticker): 
    stock = yf.Ticker(ticker) 
    financials = stock.financials 
    return financials 

Ticker = str(input("Please Enter TICKER Symbol: "))
stock = yf.Ticker(Ticker)  

info = stock.info 
print(f"Company: {info['longName']}") 
print(f"Sector: {info['sector']}") 
print(f"Market Cap: {info['marketCap']:,}") 

income_statement = stock.income_stmt
quarterly_income = stock.quarterly_income_stmt 
balance_sheet = stock.balance_sheet 
quarterly_balance = stock.quarterly_balance_sheet
cash_flow = stock.cash_flow 





current_data = stock.history(period="1d") 
current_price = current_data['Close'].iloc[-1] 
print(f"Current Price: ${current_price:,.2f}") 
