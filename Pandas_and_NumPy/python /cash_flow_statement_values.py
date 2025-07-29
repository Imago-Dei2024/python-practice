import pandas as pd 

df = pd.read_csv('/Users/connorlaber/Desktop/python-practice/Pandas_and_NumPy/data/cash_flow_statements/NRP_annual_cash-flow.csv')


# Printing Specific Rows based on the Text Value in the first column - Balance Sheet 
operating_cash_flow = df[df.iloc[:, 0] == 'OperatingCashFlow'] 


investing_cash_flow = df[df.iloc[:, 0] == 'InvestingCashFlow'] 


financing_cash_flow = df[df.iloc[:, 0] == 'FinancingCashFlow'] 


free_cash_flow = df[df.iloc[:, 0] == 'FreeCashFlow']


beginning_cash_position = df[df.iloc[:, 0] == 'BeginningCashPosition'] 


end_cash_position = df[df.iloc[:, 0] == 'EndCashPosition'] 


changes_in_cash = df[df.iloc[:, 0] == 'ChangesInCash']
 

# --- Other Stats to Note --- # 
changes_in_working_capital = df[df.iloc[:, 0] == 'ChangeInWorkingCapital'] 


cash_flow_from_continuing_financing_activities = df[df.iloc[:, 0] == 'CashFlowFromContinuingFinancingActivities'] 


long_term_debt_issuance = df[df.iloc[:, 0] == 'LongTermDebtIssuance']


issuance_of_debt = df[df.iloc[:, 0] == 'IssuanceOfDebt'] 


repayment_of_debt = df[df.iloc[:, 0] == 'RepaymentOfDebt'] 


long_term_debt_payments = df[df.iloc[:, 0] == 'LongTermDebtPayments'] 


cash_dividends_paid = df[df.iloc[:, 0] == 'CashDividendsPaid'] 
