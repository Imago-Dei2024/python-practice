import yfinance as yf 

# Download financial Statements for Specific Companies 
ticker = str(input("Enter a Company Ticker Symbol: ")) 
company = yf.Ticker(ticker) 

#Get the Financial Statements 
income_statement = company.financials 
balance_sheet = company.balance_sheet 
cashflow = company.cashflow 

income_statement.to_csv('/Users/connorlaber/Desktop/python-practice/Pandas_and_NumPy/data/income_statements') 
