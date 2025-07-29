import yfinance as yf 

# Download financial Statements for Specific Companies 
ticker = str(input("Enter a Company Ticker Symbol: ")) 
company = yf.Ticker(ticker) 

#Get the Financial Statements 
income_statement = company.financials 
balance_sheet = company.balance_sheet 
cash_flow = company.cashflow 

income_statement.to_csv(f'/Users/connorlaber/Desktop/python-practice/Pandas_and_NumPy/data/income_statements/{ticker}_income_statement.csv') 
balance_sheet.to_csv(f'/Users/connorlaber/Desktop/python-practice/Pandas_and_NumPy/data/balance_sheets/{ticker}_balance_sheet.csv') 
cash_flow.to_csv(f'/Users/connorlaber/Desktop/python-practice/Pandas_and_NumPy/data/cash_flow_statements/{ticker}_cash_flow_statement.csv')
