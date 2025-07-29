import pandas as pd 

df = pd.read_csv('/Users/connorlaber/Desktop/python-practice/Pandas_and_NumPy/data/balance_sheets/NRP_annual_balance-sheet.csv')

# Printing Specific Rows based on the Text Value in the first column - Balance Sheet 
total_assets_data = df[df.iloc[:, 0] == 'TotalAssets'] 


current_assets_data = df[df.iloc[:, 0] == 'CurrentAssets'] 
 

total_liabilities_data = df[df.iloc[:, 0] == 'TotalLiabilities'] 
 

current_liabilities_data = df[df.iloc[:, 0] == 'CurrentLiabilities']


total_debt_data = df[df.iloc[:, 0] == 'TotalDebt'] 


current_debt_data = df[df.iloc[:, 0] == 'CurrentDebt'] 


long_term_debt_data = df[df.iloc[:, 0] == 'LongTermDebt'] 
 

stockholder_equity_data = df[df.iloc[:, 0] == 'StockholdersEquity'] 
  

working_capital_data = df[df.iloc[:, 0] == 'WorkingCapital'] 


invested_capital_data = df[df.iloc[:, 0] == 'InvestedCapital'] 


shares_issued_data = df[df.iloc[:, 0] == 'SharesIssued'] 


ordinary_shares_data = df[df.iloc[:, 0] == 'OrdinarySharesNumber'] 

