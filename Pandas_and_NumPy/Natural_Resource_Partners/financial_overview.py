import pandas as pd  
import numpy as np 

import income_statement 
import balance_sheet 
import cash_flow  

nrp_income_df = pd.read_csv('/Users/connorlaber/Desktop/project-portfolio/python-practice/Pandas_and_NumPy/data/income_statements/NRP_income_statement.csv') 
nrp_cf_df = pd.read_csv('/Users/connorlaber/Desktop/project-portfolio/python-practice/Pandas_and_NumPy/data/cash_flow_statements/NRP_annual_cash-flow.csv') 
nrp_bs_df = pd.read_csv('/Users/connorlaber/Desktop/project-portfolio/python-practice/Pandas_and_NumPy/data/balance_sheets/NRP_annual_balance-sheet.csv') 

print(nrp_income_df) 
print(nrp_cf_df) 
print(nrp_bs_df) 



