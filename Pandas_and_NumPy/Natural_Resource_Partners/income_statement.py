
import pandas as pd

df = pd.read_csv('/Users/connorlaber/Desktop/python-practice/Pandas_and_NumPy/data/income_statements/NRP_income_statement.csv')

revenue_data = df[df.iloc[:, 0] == 'TotalRevenue'] 
 

cost_of_revenue_data = df[df.iloc[:, 0] == 'CostOfRevenue'] 


gross_profit_data = df[df.iloc[:, 0] == 'GrossProfit'] 


operating_expense_data = df[df.iloc[:, 0] == 'OperatingExpense'] 


net_income_data = df[df.iloc[:, 0] == 'NetIncome'] 


basic_eps_data = df[df.iloc[:, 0] == 'BasicEPS'] 