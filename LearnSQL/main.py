import sqlite3
import os

DATABASE_FILE = "financial_data_1.db"
SCHEMA_FILE = "schema.sql"

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE_FILE)
    # This allows you to access columns by name
    conn.row_factory = sqlite3.Row
    return conn

def create_database():
    """Creates the database and all tables from schema.sql"""
    print("Checking database and tables...")
    
    # Check if database file exists and has the correct tables
    if os.path.exists(DATABASE_FILE):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            conn.close()
            
            table_names = [table[0] for table in tables]
            expected_tables = [
                'companies', 'valuation_metrics', 'ticker_details', 'related_tickers',
                'full_market_snapshot', 'top_movers', 'financial_filings', 
                'income_statements', 'balance_sheets', 'cash_flow_statements'
            ]
            
            missing_tables = [table for table in expected_tables if table not in table_names]
            
            if len(missing_tables) == 0:
                print(f"Database exists with all {len(table_names)} tables. Ready to use!")
                return
            else:
                print(f"Database exists but missing tables: {missing_tables}")
                print("Recreating database with correct schema...")
                os.remove(DATABASE_FILE)
        except sqlite3.Error as e:
            print(f"Error checking existing database: {e}")
            print("Recreating database...")
            os.remove(DATABASE_FILE)

    print("Creating database and tables...")
    try:
        # Check if schema file exists
        if not os.path.exists(SCHEMA_FILE):
            print(f"Error: {SCHEMA_FILE} not found in current directory: {os.getcwd()}")
            print("Please make sure schema.sql exists in the same directory as main.py")
            return
            
        with open(SCHEMA_FILE, 'r') as f:
            schema_sql = f.read()
        
        print(f"Schema file found. Content length: {len(schema_sql)} characters")
        
        with get_db_connection() as conn:
            # Using executescript to run multiple SQL statements
            conn.executescript(schema_sql)
            
        # Verify tables were created
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        conn.close()
        
        table_names = [table[0] for table in tables]
        print(f"Database and tables created successfully!")
        print(f"Created tables: {', '.join(table_names)}")
        
    except FileNotFoundError:
        print(f"Error: {SCHEMA_FILE} not found. Please make sure it's in the same directory.")
        print(f"Current directory: {os.getcwd()}")
        print("Files in current directory:")
        for file in os.listdir('.'):
            print(f"  {file}")
    except sqlite3.Error as e:
        print(f"An error occurred during database creation: {e}")
        print("This might be due to syntax errors in the schema.sql file.")
        print("Please check your schema.sql file for any SQL syntax errors.")

def add_company_data(company_details):
    """
    Adds a new company and its general information to the database.
    `company_details` should be a dictionary.
    Returns the ID of the newly inserted company.
    """
    sql = """
        INSERT INTO companies (
            company_name, ticker_symbol, industry, sector, market_cap, 
            bid, ask, fifty_two_week_high, fifty_two_week_low, volume, 
            average_volume, beta_5y_monthly, pe_ratio_ttm, eps_ttm, 
            earnings_date, forward_dividend_yield, ex_dividend_date,
            shares_outstanding, current_share_price
        ) VALUES (
            :company_name, :ticker_symbol, :industry, :sector, :market_cap, 
            :bid, :ask, :fifty_two_week_high, :fifty_two_week_low, :volume, 
            :average_volume, :beta_5y_monthly, :pe_ratio_ttm, :eps_ttm, 
            :earnings_date, :forward_dividend_yield, :ex_dividend_date,
            :shares_outstanding, :current_share_price
        )
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(sql, company_details)
        conn.commit()
        print(f"Successfully added company: {company_details['company_name']}")
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        print(f"Error: Company with ticker '{company_details['ticker_symbol']}' already exists.")
        # If it exists, let's get its ID
        cursor.execute("SELECT id FROM companies WHERE ticker_symbol = ?", (company_details['ticker_symbol'],))
        result = cursor.fetchone()
        return result['id'] if result else None
    except sqlite3.Error as e:
        print(f"An error occurred while adding company data: {e}")
        return None
    finally:
        conn.close()

def add_related_tickers(base_ticker, related_tickers_list):
    """
    Adds related tickers for a given base ticker.
    `related_tickers_list` should be a list of ticker symbols.
    """
    sql = """
        INSERT OR IGNORE INTO related_tickers (base_ticker, related_ticker)
        VALUES (?, ?)
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        for i, related_ticker in enumerate(related_tickers_list):
            cursor.execute(sql, (base_ticker, related_ticker))
        conn.commit()
        print(f"Successfully added {len(related_tickers_list)} related tickers for {base_ticker}")
    except sqlite3.Error as e:
        print(f"An error occurred while adding related tickers: {e}")
    finally:
        conn.close()

def add_financial_filing(filing_details):
    """
    Adds a financial filing record.
    Returns the filing_id for use in other financial statements.
    """
    sql = """
        INSERT INTO financial_filings (
            ticker, cik, company_name, sic, filing_date, period_of_report_date,
            start_date, end_date, fiscal_period, fiscal_year, timeframe,
            acceptance_datetime, source_filing_url, source_filing_file_url
        ) VALUES (
            :ticker, :cik, :company_name, :sic, :filing_date, :period_of_report_date,
            :start_date, :end_date, :fiscal_period, :fiscal_year, :timeframe,
            :acceptance_datetime, :source_filing_url, :source_filing_file_url
        )
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(sql, filing_details)
        conn.commit()
        filing_id = cursor.lastrowid
        print(f"Successfully added financial filing for {filing_details['company_name']} - {filing_details['fiscal_period']} {filing_details['fiscal_year']}")
        return filing_id
    except sqlite3.IntegrityError:
        print(f"Error: Filing already exists for {filing_details['cik']} - {filing_details['fiscal_period']} {filing_details['fiscal_year']}")
        # Get existing filing ID
        cursor.execute("""
            SELECT id FROM financial_filings 
            WHERE cik = ? AND fiscal_period = ? AND fiscal_year = ? AND timeframe = ?
        """, (filing_details['cik'], filing_details['fiscal_period'], 
              filing_details['fiscal_year'], filing_details['timeframe']))
        result = cursor.fetchone()
        return result['id'] if result else None
    except sqlite3.Error as e:
        print(f"An error occurred while adding financial filing: {e}")
        return None
    finally:
        conn.close()

def add_income_statement(filing_id, income_data):
    """
    Adds income statement data for a specific filing.
    """
    sql = """
        INSERT OR REPLACE INTO income_statements (
            filing_id, revenues, cost_of_revenue, gross_profit,
            research_and_development_expenses, selling_general_and_administrative_expenses,
            operating_expenses, operating_income_loss, interest_expense_operating,
            interest_income_expense_net, income_loss_from_continuing_operations_before_tax,
            income_tax_expense_benefit, net_income_loss, net_income_loss_attributable_to_parent,
            earnings_per_share_basic, earnings_per_share_diluted,
            weighted_average_shares_outstanding_basic, weighted_average_shares_outstanding_diluted
        ) VALUES (
            :filing_id, :revenues, :cost_of_revenue, :gross_profit,
            :research_and_development_expenses, :selling_general_and_administrative_expenses,
            :operating_expenses, :operating_income_loss, :interest_expense_operating,
            :interest_income_expense_net, :income_loss_from_continuing_operations_before_tax,
            :income_tax_expense_benefit, :net_income_loss, :net_income_loss_attributable_to_parent,
            :earnings_per_share_basic, :earnings_per_share_diluted,
            :weighted_average_shares_outstanding_basic, :weighted_average_shares_outstanding_diluted
        )
    """
    income_data['filing_id'] = filing_id
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(sql, income_data)
        conn.commit()
        print(f"Successfully added income statement for filing ID: {filing_id}")
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"An error occurred while adding income statement: {e}")
        return None
    finally:
        conn.close()

def add_top_mover(mover_data):
    """
    Adds top mover data.
    """
    sql = """
        INSERT INTO top_movers (
            ticker_symbol, direction, position_rank, todays_change,
            todays_change_perc, current_price, volume
        ) VALUES (
            :ticker_symbol, :direction, :position_rank, :todays_change,
            :todays_change_perc, :current_price, :volume
        )
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(sql, mover_data)
        conn.commit()
        print(f"Successfully added top mover: {mover_data['ticker_symbol']} ({mover_data['direction']})")
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"An error occurred while adding top mover: {e}")
        return None
    finally:
        conn.close()

def get_company_by_ticker(ticker):
    """Retrieves a company's general information by its ticker symbol."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM companies WHERE ticker_symbol = ?", (ticker,))
    company = cursor.fetchone()
    conn.close()
    
    if company:
        # Convert the sqlite3.Row object to a dictionary for easier use
        return dict(company)
    return None

def get_financial_summary(ticker, timeframe='annual'):
    """
    Gets a financial summary for a company including latest income statement and balance sheet.
    """
    sql = """
        SELECT 
            f.ticker, f.company_name, f.fiscal_year, f.fiscal_period,
            i.revenues, i.net_income_loss, i.earnings_per_share_diluted,
            b.assets, b.stockholders_equity, b.cash_and_cash_equivalents_at_carrying_value
        FROM financial_filings f
        LEFT JOIN income_statements i ON f.id = i.filing_id
        LEFT JOIN balance_sheets b ON f.id = b.filing_id
        WHERE f.ticker = ? AND f.timeframe = ?
        ORDER BY f.fiscal_year DESC, f.fiscal_period DESC
        LIMIT 1
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql, (ticker, timeframe))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return dict(result)
    return None

def get_top_movers(direction='gainers', limit=10):
    """
    Gets top movers (gainers or losers) from the latest query.
    """
    sql = """
        SELECT ticker_symbol, direction, position_rank, todays_change_perc, current_price
        FROM top_movers 
        WHERE direction = ?
        ORDER BY position_rank ASC
        LIMIT ?
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql, (direction, limit))
    results = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in results]

def debug_database():
    """Debug function to check database state"""
    print("\n=== Database Debug Info ===")
    print(f"Current directory: {os.getcwd()}")
    print(f"Database file exists: {os.path.exists(DATABASE_FILE)}")
    print(f"Schema file exists: {os.path.exists(SCHEMA_FILE)}")
    
    if os.path.exists(DATABASE_FILE):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            conn.close()
            
            table_names = [table[0] for table in tables]
            print(f"Tables in database: {table_names}")
            print(f"Number of tables: {len(table_names)}")
        except Exception as e:
            print(f"Error reading database: {e}")
    
    print("Files in current directory:")
    for file in os.listdir('.'):
        print(f"  {file}")
    print("========================\n")

def main():
    """Main function to run the program."""
    # Debug info
    debug_database()
    
    # 1. Create the database if it doesn't exist
    create_database()

    # 2. Example: Add data for Apple Inc.
    apple_data = {
        'company_name': 'Apple Inc.',
        'ticker_symbol': 'AAPL',
        'industry': 'Consumer Electronics',
        'sector': 'Technology',
        'market_cap': 3250000000000,  # 3.25 Trillion
        'bid': 208.50,
        'ask': 209.25,
        'fifty_two_week_high': 237.23,
        'fifty_two_week_low': 164.08,
        'volume': 45000000,
        'average_volume': 52000000,
        'beta_5y_monthly': 1.29,
        'pe_ratio_ttm': 32.75,
        'eps_ttm': 6.43,
        'earnings_date': '2024-02-01',
        'forward_dividend_yield': 0.0047,
        'ex_dividend_date': '2024-02-09',
        'shares_outstanding': 15550000000,  # 15.55 Billion
        'current_share_price': 209.15
    }
    
    company_id = add_company_data(apple_data)

    # 3. Example: Add related tickers for Apple
    if company_id:
        related_tickers = ['MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META']
        add_related_tickers('AAPL', related_tickers)

    # 4. Example: Add a financial filing
    filing_data = {
        'ticker': 'AAPL',
        'cik': '0000320193',
        'company_name': 'Apple Inc.',
        'sic': '3571',
        'filing_date': '2023-11-03',
        'period_of_report_date': '2023-09-30',
        'start_date': '2022-10-01',
        'end_date': '2023-09-30',
        'fiscal_period': 'FY',
        'fiscal_year': '2023',
        'timeframe': 'annual',
        'acceptance_datetime': '20231103162459',
        'source_filing_url': 'https://www.sec.gov/Archives/edgar/data/320193/000032019323000106/0000320193-23-000106-index.htm',
        'source_filing_file_url': None
    }
    
    filing_id = add_financial_filing(filing_data)

    # 5. Example: Add income statement data
    if filing_id:
        income_data = {
            'revenues': 383285000000,  # $383.3B
            'cost_of_revenue': 214137000000,  # $214.1B
            'gross_profit': 169148000000,  # $169.1B
            'research_and_development_expenses': 29915000000,  # $29.9B
            'selling_general_and_administrative_expenses': 24932000000,  # $24.9B
            'operating_expenses': 54847000000,  # $54.8B
            'operating_income_loss': 114301000000,  # $114.3B
            'interest_expense_operating': None,
            'interest_income_expense_net': 3750000000,  # $3.75B
            'income_loss_from_continuing_operations_before_tax': 118105000000,  # $118.1B
            'income_tax_expense_benefit': 16741000000,  # $16.7B
            'net_income_loss': 96995000000,  # $97.0B
            'net_income_loss_attributable_to_parent': 96995000000,  # $97.0B
            'earnings_per_share_basic': 6.16,
            'earnings_per_share_diluted': 6.13,
            'weighted_average_shares_outstanding_basic': 15744231000,
            'weighted_average_shares_outstanding_diluted': 15812547000
        }
        
        add_income_statement(filing_id, income_data)

    # 6. Example: Add some top movers
    top_gainers = [
        {
            'ticker_symbol': 'NVDA',
            'direction': 'gainers',
            'position_rank': 1,
            'todays_change': 15.50,
            'todays_change_perc': 8.25,
            'current_price': 203.45,
            'volume': 45000000
        },
        {
            'ticker_symbol': 'TSLA',
            'direction': 'gainers',
            'position_rank': 2,
            'todays_change': 12.30,
            'todays_change_perc': 6.75,
            'current_price': 194.80,
            'volume': 55000000
        }
    ]
    
    for mover in top_gainers:
        add_top_mover(mover)

    # 7. Example: Retrieve and display some data
    if company_id:
        print("\n--- Verifying Data Insertion ---")
        
        # Get company data
        retrieved_data = get_company_by_ticker('AAPL')
        if retrieved_data:
            print("Company data for AAPL:")
            print(f"  Company: {retrieved_data['company_name']}")
            print(f"  Market Cap: ${retrieved_data['market_cap']:,.0f}")
            print(f"  Current Price: ${retrieved_data['current_share_price']}")
            print(f"  P/E Ratio: {retrieved_data['pe_ratio_ttm']}")
        
        # Get financial summary
        financial_summary = get_financial_summary('AAPL')
        if financial_summary:
            print(f"\nFinancial Summary for AAPL (FY {financial_summary['fiscal_year']}):")
            print(f"  Revenue: ${financial_summary['revenues']:,.0f}")
            print(f"  Net Income: ${financial_summary['net_income_loss']:,.0f}")
            if financial_summary['assets']:
                print(f"  Total Assets: ${financial_summary['assets']:,.0f}")
            print(f"  EPS (Diluted): ${financial_summary['earnings_per_share_diluted']}")
        
        # Get top gainers
        top_gainers_data = get_top_movers('gainers', 5)
        if top_gainers_data:
            print(f"\nTop Gainers:")
            for mover in top_gainers_data:
                print(f"  {mover['position_rank']}. {mover['ticker_symbol']}: +{mover['todays_change_perc']:.2f}% (${mover['current_price']})")

if __name__ == '__main__':
    main()