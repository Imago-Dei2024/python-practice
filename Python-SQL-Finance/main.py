import sqlite3
import os

DATABASE_FILE = "financial_data.db"
SCHEMA_FILE = "schema.sql"

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE_FILE)
    # This allows you to access columns by name
    conn.row_factory = sqlite3.Row
    return conn

def create_database():
    """Creates the database tables from the schema.sql file."""
    if os.path.exists(DATABASE_FILE):
        print("Database file already exists. Skipping creation.")
        return

    print("Creating database and tables...")
    try:
        with open(SCHEMA_FILE, 'r') as f:
            schema_sql = f.read()
        
        with get_db_connection() as conn:
            # Using executescript to run multiple SQL statements
            conn.executescript(schema_sql)
        print("Database and tables created successfully.")
    except FileNotFoundError:
        print(f"Error: {SCHEMA_FILE} not found. Please make sure it's in the same directory.")
    except sqlite3.Error as e:
        print(f"An error occurred during database creation: {e}")

def add_company_data(company_details):
    """
    Adds a new company and its general information to the database.
    `company_details` should be a dictionary.
    Returns the ID of the newly inserted company.
    """
    sql = """
        INSERT INTO companies (
            company_name, ticker_symbol, industry, sector, market_cap, 
            beta_5y_monthly, pe_ratio_ttm, eps_ttm, shares_outstanding, 
            current_share_price
        ) VALUES (
            :company_name, :ticker_symbol, :industry, :sector, :market_cap, 
            :beta_5y_monthly, :pe_ratio_ttm, :eps_ttm, :shares_outstanding, 
            :current_share_price
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

def main():
    """Main function to run the program."""
    # 1. Create the database if it doesn't exist
    create_database()

    # 2. Example: Add data for a sample company (e.g., Apple Inc.)
    # In a real application, you would fetch this data from an API.
    apple_data = {
        'company_name': 'Apple Inc.',
        'ticker_symbol': 'AAPL',
        'industry': 'Consumer Electronics',
        'sector': 'Technology',
        'market_cap': 3250000000000, # 3.25 Trillion
        'beta_5y_monthly': 1.29,
        'pe_ratio_ttm': 32.75,
        'eps_ttm': 6.43,
        'shares_outstanding': 15550000000, # 15.55 Billion
        'current_share_price': 209.15
    }
    
    company_id = add_company_data(apple_data)

    # 3. Example: Retrieve and print the data we just added
    if company_id:
        print("\n--- Verifying Data Insertion ---")
        retrieved_data = get_company_by_ticker('AAPL')
        if retrieved_data:
            print("Successfully retrieved data for AAPL:")
            for key, value in retrieved_data.items():
                print(f"  {key}: {value}")
        else:
            print("Could not retrieve data for AAPL.")
            
    # You can now add functions to insert data into the other tables
    # e.g., add_income_statement(company_id, statement_data)

if __name__ == '__main__':
    main()