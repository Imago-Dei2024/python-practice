-- database: financial_data_1.db
DROP TABLE IF EXISTS companies; 
DROP TABLE IF EXISTS income_statements; 
DROP TABLE IF EXISTS balance_sheets; 
DROP TABLE IF EXISTS cash_flow_statements;


-- 1. Table for General Company Information 
CREATE TABLE companies ( 
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    company_name TEXT NOT NULL, 
    ticker_symbol TEXT NOT NULL, 
    industry TEXT NOT NULL UNIQUE,
    sector TEXT, 
    market_cap REAL, 
    bid REAL, 
    ask REAL, 
    fiftey_two_week_high REAL, 
    fiftey_two_week_low REAL, 
    volume INTEGER, 
    average_volume INTEGER, 
    beta_5y_monthly REAL, 
    pe_ratio_ttm REAL, 
    eps_ttm REAL, 
    earnings_date TEXT, -- Storing Dates as text in 'YYYY-MM-DD' format is common 
    forward_dividend_yield REAL, 
    ex_dividend_date TEXT, 
    shares_outstanding INTEGER, 
    current_share_price REAL, 
    last_updated TEXT DEFAULT CURRENT_TIMESTAMP -- To know when the data was last refreshed 
); 






-- 2. Table With Valuation Metrics for Companies 
CREATE TABLE valuation_metrics ( 
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    company_id INTEGER, 
    ticker_symbold TEXT NOT NULL, 
    shares_outstanding INTEGER, 
    current_share_price REAL, 
    market_cap REAL, 
    last_updated TEXT DEFAULT CURRENT_TIMESTAMP 
); 






-- 3. Create a Table for Ticker Overview 
CREATE TABLE ticker_details ( 
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    ticker_symbol TEXT NOT NULL UNIQUE, 
    company_name TEXT, 
    company_description TEXT, 
    company_market_cap REAL, 
    current_share_price REAL, 
    last_updated TEXT DEFAULT CURRENT_TIMESTAMP
);  







-- 4. Create Table for Related Tickers Query 
CREATE TABLE related_tickers ( 
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    base_ticker TEXT NOT NULL UNIQUE, 
    related_ticker TEXT NOT NULL, 
    relationship_strength INTEGER, 
    created_at TEXT DEFAULT CURRENT_TIMESTAMP, 
    UNIQUE(base_ticker, related_ticker) -- Prevents Duplicate Relationships 
); 






-- 5. Create Table for Full Market Snapshot 
CREATE TABLE full_market_snapshot ( 
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    ticker_symbol TEXT NOT NULL, 

    -- Main Market Snapshot Data 
    fmv REAL, 
    todays_change REAL, 
    todays_change_perc REAL, 
    updated_timestamp INTEGER, 

    -- Previous Day Data 
    prev_day_open REAL, 
    prev_day_high REAL, 
    prev_day_low REAL, 
    prev_day_close REAL,
    prev_day_volume INTEGER, 


    -- Current Day Data 
    day_open REAL, 
    day_high REAL, 
    day_low REAL, 
    day_close REAL,
    day_volume REAL, 

    -- Last Trade Data 
    last_trade_price REAL, 
    last_trade_size INTEGER, 
    last_trade_timestamp INTEGER, 

    -- Last Quote Data 
    last_quote_bid REAL, 
    last_quote_ask REAL,
    last_quote_bid_size INTEGER, 
    last_quote_ask_size INTEGER, 
    last_quote_timestamp INTEGER, 

    last_updated TEXT DEFAULT CURRENT_TIMESTAMP
);






-- 6. Create Table for Top Market Movers 
CREATE TABLE top_movers ( 
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    ticker_symbol TEXT NOT NULL, 
    direction TEXT NOT NULL, 
    position_rank INTEGER,  
    last_updated TEXT DEFAULT CURRENT_TIMESTAMP
);





-- 7. Create a Table for Financial Source Info (Financials Query) 
CREATE TABLE financial_filings ( 
   id INTEGER PRIMARY KEY AUTOINCREMENT, 
    
    -- Company Identification 
    ticker TEXT,
    cik TEXT NOT NULL,
    company_name TEXT,
    sic TEXT, 

    -- Filing metadata 
    filing_date TEXT,
    period_of_report_date TEXT, 
    start_date TEXT,
    end_date TEXT, 
    fiscal_period TEXT, 
    fiscal_year TEXT, 
    timeframe TEXT, 

    -- Source Information 
    acceptance_datetime TEXT,
    source_filing_url TEXT,
    source_filing_file_url TEXT, 

    -- metaData 
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(cik, fiscal_period, fiscal_year, timeframe) 
);





-- 8. Create a Table for Income Statements 
CREATE TABLE income_statements ( 
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filing_id INTEGER NOT NULL,  

    -- Revenue Items 
    revenues REAL, 
    cost_of_revenue REAL, 
    gross_profit REAL, 

    -- Operating Expenses 
    research_and_development_expenses REAL,
    selling_general_and_administrative_expenses REAL,
    operating_expenses REAL, 
    operating_income_loss REAL, 

    -- Non-Operating Items 
    interest_expense_operating REAL,
    interest_income_expense_net REAL, 
    other_comprehensive_income_loss REAL, 

    -- Pre Tax and Taxes 
    income_loss_from_continuing_operations_before_tax REAL, 
    income_tax_expense_benefit REAL, 

    -- Net Income 
    net_income_loss REAL, 
    net_income_loss_attributable_to_parent REAL, 

    -- Per Share Data 
    earnings_per_share_basic REAL, 
    earnings_per_share_diluted REAL, 
    weighted_average_shares_outstanding_basic REAL, 
    weighted_average_shares_outstanding_diluted REAL, 

    -- Timestamp column MUST come before constraints
    last_updated TEXT DEFAULT CURRENT_TIMESTAMP,
    
    -- Table constraints come last
    FOREIGN KEY (filing_id) REFERENCES financial_filings(id), 
    UNIQUE(filing_id)
);





-- 9.) Create Table for Balance Sheets 
CREATE TABLE balance_sheets ( 
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    filing_id INTEGER NOT NULL,  

    -- Current Assets 
    cash_and_cash_equivalents_at_carrying_value REAL,
    short_term_investments REAL, 
    accounts_recievable_net REAL, 
    inventory_net REAL, 
    prepaid_expenses_and_other_current_assets REAL,
    assets_current REAL, 

    -- Non Current Assets 
    property_plant_and_equipment_net REAL, 
    goodwill REAL,
    intangible_assets_net REAL, 
    long_term_investments REAL,
    other_assets_noncurrent REAL, 
    assets_noncurrent REAL,

    -- Total Assets 
    assets REAL, 

    -- Current Liabilities 
    accounts_payable_current REAL, 
    accrued_liabilities_current REAL, 
    short_term_debt REAL, 
    liabilities_current REAL, 

    -- Non-Current Liabilities 
    long_term_debt_noncurrent REAL,
    deferred_tax_liabilities_noncurrent REAL,
    other_liabilities_noncurrent REAL, 
    liabilities_noncurrent REAL, 

    -- Total Liabilities 
    liabilities REAL, 

    -- Equity 
    common_stock_shares_outstanding REAL,
    common_stock_par_or_stated_value_per_share REAL, 
    common_stock_value REAL,
    retained_earnings_accumulated_deficit REAL,
    accumulated_other_comprehensive_income_loss REAL,
    stockholders_equity REAL, 

    -- Total Liabilities & Equity 
    loabilities_and_stockholders_equity REAL, 

    last_updated TEXT DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (filing_id) REFERENCES financial_filings(id), 
    UNIQUE(filing_id)
);





-- 10. Create a Table for Cash Flow Statements 
CREATE TABLE cash_flow_statements ( 
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    filing_id INTEGER NOT NULL,  

    -- Operating Activities 
    net_income_loss REAL,
    depreciation_depletion_and_amortization REAL,
    stock_based_compensation REAL,
    deferred_income_tax_expense_benefit REAL, 

    -- Changes in working capital 
    increase_decrease_in_accounts_recievable REAL,
    increase_decrease_in_inventory REAL, 
    increase_decrease_in_accounts_payable REAL, 
    increase_decrease_in_accrues_liabilities REAL, 

    net_cash_provided_by_used_in_operating_activities REAL, 

    -- Investing Activities 
    payments_to_acquire_property_plant_and_equipment REAL,
    payments_to_acquire_businesses_net_of_cash_acquired REAL,
    payments_for_proceeds_from_short_term_investments_net REAL,
    payments_for_proceeds_from_long_term_investments_net REAL, 

    net_cash_provided_by_used_in_investing_activities REAL, 

    -- Financing Activities 
    proceeds_from_issuance_of_long_term_debt REAL,
    repayments_of_long_term_debt REAL,
    payments_of_ordinary_dividends REAL,
    payments_for_repurchase_of_common_stock REAL,
    proceeds_from_issuance_of_common_stock REAL,
    
    net_cash_provided_by_used_in_financing_activities REAL, 

    -- Cash Flow Summary 
    cash_cash_equivalents_and_short_term_investments_period_increase_decrease REAL,
    cash_and_cash_equivalents_at_carrying_value_beginning REAL,
    cash_and_cash_equivalents_at_carrying_value_ending REAL, 

    -- Supplimental Disclosure 
    income_tax_paid_net REAL,
    interest_paid_net REAL,
    
    last_updated TEXT DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (filing_id) REFERENCES financial_filings(id),
    UNIQUE(filing_id)  
);






