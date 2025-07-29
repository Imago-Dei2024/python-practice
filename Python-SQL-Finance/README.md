# ** SQL KEYWORD CHEAT SHEET 

## Key Words 
    
    '''markdown 
        id = Column Name (Like a spreadsheet column header) 
        INTEGER = This Column Stores Whole Numbers 
        PRIMARY KEY = Makes the column the unique identifier for each row (like a customer number) 
        AUTOINCREMENT = Database automatically asigns the next numbers when you add new rows 
        
        TEXT = These columns store text/words 
        NOT NULL = This Field is Required 
        UNIQUE = No Two companies can have the same ticker symbol  

        REAL = These store decimal numbers (like 45.67 or 1234.50) 
        DEFAULT CURRENT_TIMESTAMP = Automatically fills in the current date/time when a new row is created'

## Indexes for Performance 

    '''markdown
        CREATE INDEX idx_filings_ticker ON financial_filings(ticker);
        CREATE INDEX idx_filings_cik ON financial_filings(cik);
        CREATE INDEX idx_filings_period ON financial_filings(fiscal_period, fiscal_year);
        CREATE INDEX idx_filings_timeframe ON financial_filings(timeframe);

        CREATE INDEX idx_income_filing ON income_statements(filing_id);
        CREATE INDEX idx_balance_filing ON balance_sheets(filing_id);
        CREATE INDEX idx_cashflow_filing ON cash_flow_statements(filing_id);
        CREATE INDEX idx_comprehensive_filing ON comprehensive_income_statements(filing_id);' 

## Inserting New Company Info Example 
    
    '''markdown 

        -- First insert the filing metadata
        INSERT INTO financial_filings (
            ticker, cik, company_name, fiscal_period, fiscal_year, 
            timeframe, filing_date
        ) VALUES (
            'AAPL', '0000320193', 'Apple Inc', 'FY', '2023', 
            'annual', '2023-11-03'
        );
        
            '
