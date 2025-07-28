-- Create the main companies table
CREATE TABLE IF NOT EXISTS companies (
    company_id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_name VARCHAR(255) NOT NULL,
    ticker_symbol VARCHAR(10) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the company information table
CREATE TABLE IF NOT EXISTS company_info (
    info_id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    industry VARCHAR(100),
    sector VARCHAR(100),
    market_cap DECIMAL(20, 2),
    bid_price DECIMAL(10, 2),
    ask_price DECIMAL(10, 2),
    week_52_low DECIMAL(10, 2),
    week_52_high DECIMAL(10, 2),
    volume BIGINT,
    avg_volume BIGINT,
    beta DECIMAL(5, 3),
    pe_ratio_ttm DECIMAL(10, 2),
    eps_ttm DECIMAL(10, 2),
    earnings_date DATE,
    forward_dividend_yield DECIMAL(5, 2),
    ex_dividend_date DATE,
    shares_outstanding BIGINT,
    current_share_price DECIMAL(10, 2),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(company_id) ON DELETE CASCADE
);

-- Create the income statements table
CREATE TABLE IF NOT EXISTS income_statements (
    statement_id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    fiscal_year INTEGER NOT NULL,
    fiscal_period VARCHAR(10) NOT NULL, -- 'Q1', 'Q2', 'Q3', 'Q4', 'Annual'
    revenue DECIMAL(20, 2),
    cost_of_revenue DECIMAL(20, 2),
    gross_profit DECIMAL(20, 2),
    operating_expenses DECIMAL(20, 2),
    operating_income DECIMAL(20, 2),
    other_income_expense DECIMAL(20, 2),
    income_before_tax DECIMAL(20, 2),
    income_tax_expense DECIMAL(20, 2),
    net_income DECIMAL(20, 2),
    earnings_per_share DECIMAL(10, 4),
    diluted_earnings_per_share DECIMAL(10, 4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(company_id) ON DELETE CASCADE,
    UNIQUE(company_id, fiscal_year, fiscal_period)
);

-- Create the balance sheets table
CREATE TABLE IF NOT EXISTS balance_sheets (
    balance_sheet_id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    fiscal_year INTEGER NOT NULL,
    fiscal_period VARCHAR(10) NOT NULL,
    -- Assets
    cash_and_equivalents DECIMAL(20, 2),
    short_term_investments DECIMAL(20, 2),
    accounts_receivable DECIMAL(20, 2),
    inventory DECIMAL(20, 2),
    total_current_assets DECIMAL(20, 2),
    property_plant_equipment DECIMAL(20, 2),
    goodwill DECIMAL(20, 2),
    intangible_assets DECIMAL(20, 2),
    total_assets DECIMAL(20, 2),
    -- Liabilities
    accounts_payable DECIMAL(20, 2),
    short_term_debt DECIMAL(20, 2),
    total_current_liabilities DECIMAL(20, 2),
    long_term_debt DECIMAL(20, 2),
    total_liabilities DECIMAL(20, 2),
    -- Equity
    common_stock DECIMAL(20, 2),
    retained_earnings DECIMAL(20, 2),
    total_shareholders_equity DECIMAL(20, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(company_id) ON DELETE CASCADE,
    UNIQUE(company_id, fiscal_year, fiscal_period)
);

-- Create the cash flow statements table
CREATE TABLE IF NOT EXISTS cash_flow_statements (
    cash_flow_id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    fiscal_year INTEGER NOT NULL,
    fiscal_period VARCHAR(10) NOT NULL,
    -- Operating Activities
    net_income DECIMAL(20, 2),
    depreciation_amortization DECIMAL(20, 2),
    stock_based_compensation DECIMAL(20, 2),
    change_in_working_capital DECIMAL(20, 2),
    cash_from_operations DECIMAL(20, 2),
    -- Investing Activities
    capital_expenditures DECIMAL(20, 2),
    acquisitions DECIMAL(20, 2),
    investments DECIMAL(20, 2),
    cash_from_investing DECIMAL(20, 2),
    -- Financing Activities
    debt_issued DECIMAL(20, 2),
    debt_repaid DECIMAL(20, 2),
    stock_issued DECIMAL(20, 2),
    stock_repurchased DECIMAL(20, 2),
    dividends_paid DECIMAL(20, 2),
    cash_from_financing DECIMAL(20, 2),
    -- Summary
    net_change_in_cash DECIMAL(20, 2),
    free_cash_flow DECIMAL(20, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(company_id) ON DELETE CASCADE,
    UNIQUE(company_id, fiscal_year, fiscal_period)
);

-- Create indexes for better performance
CREATE INDEX idx_companies_ticker ON companies(ticker_symbol);
CREATE INDEX idx_income_year_period ON income_statements(fiscal_year, fiscal_period);
CREATE INDEX idx_balance_year_period ON balance_sheets(fiscal_year, fiscal_period);
CREATE INDEX idx_cashflow_year_period ON cash_flow_statements(fiscal_year, fiscal_period);

-- Create a view for easy access to current company data
CREATE VIEW current_company_overview AS
SELECT 
    c.company_id,
    c.company_name,
    c.ticker_symbol,
    ci.industry,
    ci.sector,
    ci.market_cap,
    ci.current_share_price,
    ci.pe_ratio_ttm,
    ci.eps_ttm,
    ci.beta
FROM companies c
LEFT JOIN company_info ci ON c.company_id = ci.company_id;