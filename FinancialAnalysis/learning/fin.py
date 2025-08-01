import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Tuple, Dict, Optional
import warnings
from pathlib import Path

class StockAnalyzer:
    """
    A class for analyzing stock returns and comparing performance metrics.
    """
    
    def __init__(self, style: str = 'whitegrid'):
        """Initialize the analyzer with plotting style."""
        sns.set_style(style)
        plt.rcParams['figure.figsize'] = (12, 8)
        warnings.filterwarnings('ignore', category=RuntimeWarning)
    
    def load_and_process_data(self, file_path: str, stock_name: str) -> pd.DataFrame:
        """
        Load and process stock data from CSV file.
        
        Args:
            file_path: Path to the CSV file
            stock_name: Name of the stock for labeling
            
        Returns:
            Processed DataFrame with returns calculated
        """
        try:
            # Load data
            df = pd.read_csv(file_path)
            
            # Validate required columns
            required_cols = ['Date', 'Close']
            if not all(col in df.columns for col in required_cols):
                raise ValueError(f"Missing required columns. Need: {required_cols}")
            
            # Process data
            df['Date'] = pd.to_datetime(df['Date'])
            df = df.sort_values('Date').reset_index(drop=True)
            
            # Calculate returns with error handling
            df['Return'] = df['Close'].pct_change()
            df['Stock'] = stock_name
            
            # Remove extreme outliers (returns > 50% or < -50%)
            df.loc[abs(df['Return']) > 0.5, 'Return'] = np.nan
            
            print(f"✓ Loaded {stock_name} data: {len(df)} records from {df['Date'].min().date()} to {df['Date'].max().date()}")
            return df
            
        except FileNotFoundError:
            print(f"❌ Error: File {file_path} not found")
            return pd.DataFrame()
        except Exception as e:
            print(f"❌ Error processing {stock_name} data: {str(e)}")
            return pd.DataFrame()
    
    def align_data(self, df1: pd.DataFrame, df2: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Align two datasets by date to ensure fair comparison.
        
        Args:
            df1, df2: DataFrames to align
            
        Returns:
            Tuple of aligned DataFrames
        """
        # Find common date range
        start_date = max(df1['Date'].min(), df2['Date'].min())
        end_date = min(df1['Date'].max(), df2['Date'].max())
        
        # Filter to common date range
        df1_aligned = df1[(df1['Date'] >= start_date) & (df1['Date'] <= end_date)].copy()
        df2_aligned = df2[(df2['Date'] >= start_date) & (df2['Date'] <= end_date)].copy()
        
        print(f"✓ Aligned data from {start_date.date()} to {end_date.date()}")
        return df1_aligned, df2_aligned
    
    def calculate_statistics(self, returns: pd.Series, name: str) -> Dict:
        """
        Calculate comprehensive statistics for returns.
        
        Args:
            returns: Series of returns
            name: Name for labeling
            
        Returns:
            Dictionary of calculated statistics
        """
        clean_returns = returns.dropna()
        
        if len(clean_returns) == 0:
            return {}
        
        # Handle negative returns for geometric mean
        positive_returns = clean_returns[clean_returns > -1]  # Avoid log of negative numbers
        
        stats = {
            'name': name,
            'count': len(clean_returns),
            'mean_return': clean_returns.mean(),
            'std_deviation': clean_returns.std(),
            'variance': clean_returns.var(),
            'skewness': clean_returns.skew(),
            'kurtosis': clean_returns.kurtosis(),
            'min_return': clean_returns.min(),
            'max_return': clean_returns.max(),
            'annualized_return': clean_returns.mean() * 252,  # Assuming daily data
            'annualized_volatility': clean_returns.std() * np.sqrt(252),
        }
        
        # Geometric mean (only for valid returns)
        if len(positive_returns) > 0:
            stats['geometric_mean'] = np.exp(np.log(1 + positive_returns).mean()) - 1
        else:
            stats['geometric_mean'] = np.nan
            
        # Sharpe ratio (assuming risk-free rate of 2%)
        risk_free_rate = 0.02 / 252  # Daily risk-free rate
        stats['sharpe_ratio'] = (stats['mean_return'] - risk_free_rate) / stats['std_deviation']
        
        return stats
    
    def calculate_portfolio_metrics(self, returns1: pd.Series, returns2: pd.Series, 
                                  name1: str, name2: str) -> Dict:
        """
        Calculate portfolio metrics between two assets.
        
        Args:
            returns1, returns2: Return series for both assets
            name1, name2: Names for labeling
            
        Returns:
            Dictionary of portfolio metrics
        """
        # Align series and remove NaN values
        aligned_data = pd.DataFrame({
            name1: returns1,
            name2: returns2
        }).dropna()
        
        if len(aligned_data) < 2:
            return {}
        
        r1, r2 = aligned_data[name1], aligned_data[name2]
        
        metrics = {
            'covariance': np.cov(r1, r2)[0, 1],
            'correlation': np.corrcoef(r1, r2)[0, 1],
        }
        
        # Calculate Beta (stock vs market)
        if name2.upper() == 'SPY':  # Assuming SPY is the market
            metrics['beta'] = metrics['covariance'] / r2.var()
        elif name1.upper() == 'SPY':
            metrics['beta'] = r1.var() / metrics['covariance']
        
        return metrics
    
    def print_summary(self, stats_list: list, portfolio_metrics: Dict = None):
        """Print a formatted summary of all statistics."""
        print("\n" + "="*80)
        print("STOCK ANALYSIS SUMMARY")
        print("="*80)
        
        for stats in stats_list:
            if not stats:
                continue
                
            print(f"\n📊 {stats['name'].upper()} STATISTICS:")
            print(f"   Data Points: {stats['count']:,}")
            print(f"   Average Daily Return: {stats['mean_return']:.4f} ({stats['mean_return']*100:.2f}%)")
            print(f"   Geometric Mean Return: {stats['geometric_mean']:.4f} ({stats['geometric_mean']*100:.2f}%)")
            print(f"   Annualized Return: {stats['annualized_return']:.4f} ({stats['annualized_return']*100:.2f}%)")
            print(f"   Daily Volatility: {stats['std_deviation']:.4f} ({stats['std_deviation']*100:.2f}%)")
            print(f"   Annualized Volatility: {stats['annualized_volatility']:.4f} ({stats['annualized_volatility']*100:.2f}%)")
            print(f"   Sharpe Ratio: {stats['sharpe_ratio']:.3f}")
            print(f"   Skewness: {stats['skewness']:.3f}")
            print(f"   Kurtosis: {stats['kurtosis']:.3f}")
            print(f"   Min/Max Return: {stats['min_return']:.4f} / {stats['max_return']:.4f}")
        
        if portfolio_metrics:
            print(f"\n🔗 PORTFOLIO METRICS:")
            print(f"   Correlation: {portfolio_metrics['correlation']:.4f}")
            print(f"   Covariance: {portfolio_metrics['covariance']:.6f}")
            if 'beta' in portfolio_metrics:
                print(f"   Beta: {portfolio_metrics['beta']:.3f}")
    
    def create_visualizations(self, df1: pd.DataFrame, df2: pd.DataFrame):
        """
        Create comprehensive visualizations for the analysis.
        
        Args:
            df1, df2: DataFrames with stock data
        """
        # Set up the plotting style
        plt.style.use('seaborn-v0_8')
        
        # Create subplot layout
        fig = plt.figure(figsize=(20, 15))
        
        # 1. Return distributions
        plt.subplot(3, 3, 1)
        sns.histplot(df1['Return'].dropna(), kde=True, alpha=0.7, label=df1['Stock'].iloc[0])
        sns.histplot(df2['Return'].dropna(), kde=True, alpha=0.7, label=df2['Stock'].iloc[0])
        plt.title('Return Distributions Comparison')
        plt.xlabel('Daily Return')
        plt.ylabel('Frequency')
        plt.legend()
        
        # 2. Box plots
        plt.subplot(3, 3, 2)
        returns_data = pd.concat([
            df1[['Return', 'Stock']].dropna(),
            df2[['Return', 'Stock']].dropna()
        ])
        sns.boxplot(data=returns_data, x='Stock', y='Return')
        plt.title('Return Distribution Box Plots')
        plt.xticks(rotation=45)
        
        # 3. Scatter plot
        plt.subplot(3, 3, 3)
        aligned_data = pd.merge(df1[['Date', 'Return']], df2[['Date', 'Return']], 
                               on='Date', suffixes=('_1', '_2')).dropna()
        sns.scatterplot(data=aligned_data, x='Return_2', y='Return_1', alpha=0.6)
        plt.title(f'{df1["Stock"].iloc[0]} vs {df2["Stock"].iloc[0]} Returns')
        plt.xlabel(f'{df2["Stock"].iloc[0]} Daily Return')
        plt.ylabel(f'{df1["Stock"].iloc[0]} Daily Return')
        
        # Add regression line
        sns.regplot(data=aligned_data, x='Return_2', y='Return_1', scatter=False, color='red')
        
        # 4. Time series of returns
        plt.subplot(3, 3, 4)
        plt.plot(df1['Date'], df1['Return'], alpha=0.7, label=df1['Stock'].iloc[0])
        plt.plot(df2['Date'], df2['Return'], alpha=0.7, label=df2['Stock'].iloc[0])
        plt.title('Daily Returns Over Time')
        plt.xlabel('Date')
        plt.ylabel('Daily Return')
        plt.legend()
        plt.xticks(rotation=45)
        
        # 5. Cumulative returns
        plt.subplot(3, 3, 5)
        df1_clean = df1.dropna(subset=['Return'])
        df2_clean = df2.dropna(subset=['Return'])
        cum_returns_1 = (1 + df1_clean['Return']).cumprod()
        cum_returns_2 = (1 + df2_clean['Return']).cumprod()
        
        plt.plot(df1_clean['Date'], cum_returns_1, label=f'{df1["Stock"].iloc[0]} Cumulative')
        plt.plot(df2_clean['Date'], cum_returns_2, label=f'{df2["Stock"].iloc[0]} Cumulative')
        plt.title('Cumulative Returns')
        plt.xlabel('Date')
        plt.ylabel('Cumulative Return')
        plt.legend()
        plt.xticks(rotation=45)
        
        # 6. Rolling correlation (if enough data)
        plt.subplot(3, 3, 6)
        if len(aligned_data) > 60:  # Need at least 60 days for rolling correlation
            aligned_data['Rolling_Corr'] = aligned_data['Return_1'].rolling(window=60).corr(aligned_data['Return_2'])
            plt.plot(aligned_data.index, aligned_data['Rolling_Corr'])
            plt.title('60-Day Rolling Correlation')
            plt.xlabel('Time')
            plt.ylabel('Correlation')
        else:
            plt.text(0.5, 0.5, 'Insufficient data for\nrolling correlation', 
                    ha='center', va='center', transform=plt.gca().transAxes)
            plt.title('Rolling Correlation (Insufficient Data)')
        
        # 7. Volatility comparison
        plt.subplot(3, 3, 7)
        vol_data = pd.DataFrame({
            'Stock': [df1['Stock'].iloc[0], df2['Stock'].iloc[0]],
            'Volatility': [df1['Return'].std(), df2['Return'].std()]
        })
        sns.barplot(data=vol_data, x='Stock', y='Volatility')
        plt.title('Volatility Comparison')
        plt.ylabel('Daily Volatility')
        
        # 8. Q-Q plots for normality check
        from scipy import stats
        plt.subplot(3, 3, 8)
        stats.probplot(df1['Return'].dropna(), dist="norm", plot=plt)
        plt.title(f'{df1["Stock"].iloc[0]} Q-Q Plot')
        
        plt.subplot(3, 3, 9)
        stats.probplot(df2['Return'].dropna(), dist="norm", plot=plt)
        plt.title(f'{df2["Stock"].iloc[0]} Q-Q Plot')
        
        plt.tight_layout()
        plt.show()

def main():
    """Main function to run the analysis."""
    # Initialize analyzer
    analyzer = StockAnalyzer()
    
    # Configuration
    config = {
        'tsla_file': 'TSLA.csv',
        'spy_file': 'SPY.csv',
        'tsla_name': 'Tesla',
        'spy_name': 'SPY'
    }
    
    print("🚀 Starting Stock Analysis...")
    
    # Load and process data
    tsla_df = analyzer.load_and_process_data(config['tsla_file'], config['tsla_name'])
    spy_df = analyzer.load_and_process_data(config['spy_file'], config['spy_name'])
    
    if tsla_df.empty or spy_df.empty:
        print("❌ Cannot proceed with analysis due to data loading errors.")
        return
    
    # Align data for fair comparison
    tsla_aligned, spy_aligned = analyzer.align_data(tsla_df, spy_df)
    
    # Calculate statistics
    tsla_stats = analyzer.calculate_statistics(tsla_aligned['Return'], config['tsla_name'])
    spy_stats = analyzer.calculate_statistics(spy_aligned['Return'], config['spy_name'])
    
    # Calculate portfolio metrics
    portfolio_metrics = analyzer.calculate_portfolio_metrics(
        tsla_aligned['Return'], spy_aligned['Return'], 
        config['tsla_name'], config['spy_name']
    )
    
    # Print summary
    analyzer.print_summary([tsla_stats, spy_stats], portfolio_metrics)
    
    # Create visualizations
    print("\n📈 Generating visualizations...")
    analyzer.create_visualizations(tsla_aligned, spy_aligned)
    
    print("\n✅ Analysis complete!")

if __name__ == "__main__":
    main()

