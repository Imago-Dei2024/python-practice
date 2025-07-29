DROP TABLE IF EXISTS companies;
DROP TABLE IF EXISTS income_statements;
DROP TABLE IF EXISTS balance_sheets;
DROP TABLE IF EXISTS cash_flow_statements;

-- 1. Table for General Company Information
CREATE TABLE companies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_name TEXT NOT NULL,
    ticker_symbol TEXT NOT NULL UNIQUE,
    industry TEXT,
    sector TEXT,
    market_cap REAL,
    bid REAL,
    ask REAL,
    fifty_two_week_low REAL,
    fifty_two_week_high REAL,
    volume INTEGER,
    average_volume INTEGER,
    beta_5y_monthly REAL,
    pe_ratio_ttm REAL,
    eps_ttm REAL,
    earnings_date TEXT, -- Storing dates as text in 'YYYY-MM-DD' format is common
    forward_dividend_yield REAL,
    ex_dividend_date TEXT,
    shares_outstanding INTEGER,
    current_share_price REAL,
    last_updated TEXT DEFAULT CURRENT_TIMESTAMP -- To know when the data was last refreshed
);

-- 2. Table for Income Statement Data
CREATE TABLE income_statements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER,
    fiscal_year INTEGER NOT NULL,
    period TEXT NOT NULL, -- 'Annual' or 'Quarterly'
    revenue REAL,
    cost_of_goods_sold REAL,
    gross_profit REAL,
    operating_expenses REAL,
    operating_income REAL,
    interest_expense REAL,
    income_before_tax REAL,
    income_tax_expense REAL,
    net_income REAL,
    FOREIGN KEY (company_id) REFERENCES companies (id)
);

-- 3. Table for Balance Sheet Data
CREATE TABLE balance_sheets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER,
    fiscal_year INTEGER NOT NULL,
    period TEXT NOT NULL, -- 'Annual' or 'Quarterly'
    cash_and_equivalents REAL,
    accounts_receivable REAL,
    inventory REAL,
    total_current_assets REAL,
    property_plant_equipment REAL,
    total_assets REAL,
    accounts_payable REAL,
    short_term_debt REAL,
    total_current_liabilities REAL,
    long_term_debt REAL,
    total_liabilities REAL,
    common_stock REAL,
    retained_earnings REAL,
    total_stockholder_equity REAL,
    FOREIGN KEY (company_id) REFERENCES companies (id)
);

-- 4. Table for Cash Flow Statement Data
CREATE TABLE cash_flow_statements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER,
    fiscal_year INTEGER NOT NULL,
    period TEXT NOT NULL, -- 'Annual' or 'Quarterly'
    net_income_cf REAL, -- Starting point for cash flow from operations
    depreciation_amortization REAL,
    cash_from_operating_activities REAL,
    capital_expenditures REAL,
    cash_from_investing_activities REAL,
    debt_repayment REAL,
    dividends_paid REAL,
    cash_from_financing_activities REAL,
    net_change_in_cash REAL,
    FOREIGN KEY (company_id) REFERENCES companies (id)
);

-- Create indexes to speed up queries
CREATE INDEX idx_company_ticker ON companies (ticker_symbol);
CREATE INDEX idx_income_statement_company ON income_statements (company_id);
CREATE INDEX idx_balance_sheet_company ON balance_sheets (company_id);
CREATE INDEX idx_cash_flow_company ON cash_flow_statements (company_id);