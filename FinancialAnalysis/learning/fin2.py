import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns 

tsla_df = pd.read_csv('TSLA.csv')
spy_df = pd.read_csv('SPY.csv') 

tsla_df['Date'] = pd.to_datetime(tsla_df['Date'])
spy_df['Date'] = pd.to_datetime(spy_df['Date']) 

tsla_df = tsla_df.sort_values('Date') 
spy_df = spy_df.sort_values('Date')  

tsla_df['Return'] = tsla_df['Close'].pct_change() 
spy_df['Return'] = spy_df['Close'].pct_change()  

tsla_returns = tsla_df['Return'].dropna() 
spy_returns = spy_df['Return'].dropna()  

tsla_average_return = np.mean(tsla_returns) 
spy_average_return = np.mean(spy_returns)  

print("Tesla Average 10y Return: ", tsla_average_return)
print("S&P 500 Average 10y Return: ", spy_average_return) 

tsla_geo_mean_return = np.exp(np.mean(np.log(1 + tsla_returns))) - 1
spy_geo_mean_return = np.exp(np.mean(np.log(1 + spy_returns))) - 1 

print("Geometric Mean of Average Return - Tesla: ", tsla_geo_mean_return) 
print("Geometric Mean of Average Return - SPY: ", spy_geo_mean_return)  

tsla_std_deviation = np.std(tsla_returns) 
spy_std_deviation = np.std(spy_returns) 

print("Standard Deviation - Tesla: ", tsla_std_deviation) 
print("Standard Deviation - SPY: ", spy_std_deviation)  

tsla_variance = np.var(tsla_returns) 
spy_variance = np.var(spy_returns) 

print("Variance from Average Return - Tesla: ", tsla_variance) 
print("Variance from Average Return - SPY: ", spy_variance)  

covariance_matrix = np.cov(tsla_returns, spy_returns) 
covariance = covariance_matrix[0, 1] 
print("Covariance with SPY Index - Tesla: ", covariance)  

correlation_matrix = np.corrcoef(tsla_returns, spy_returns) 
correlation = correlation_matrix[0, 1] 
print("Correlation with SPY Index - Tesla: ", correlation)  

print(tsla_df)