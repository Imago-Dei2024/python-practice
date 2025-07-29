# RealTimePolygonStockData URL Keys

# ** STOCKS 

## TICKERS 

### All Tickers -> (POLYGON_TICKERS_URL) 

    Retrieve a comprehensive list of ticker symbols supported by Polygon.io 
    across various asset classes (e.g., stocks, indices, forex, crypto). 
    Each ticker entry provides essential details such as symbol, name, market, currency, and active status.
    
    Use Cases: Asset discovery, data integration, filtering/selection, and application development. 

### Ticker Overview -> (POLYGON_TICKER_OVERVIEW_URL) 

    Retrieve comprehensive details for a single ticker supported by Polygon.io. 
    This endpoint offers a deep look into a company’s fundamental attributes, 
    including its primary exchange, standardized identifiers (CIK, composite FIGI, share class FIGI), market capitalization, industry classification, and key dates. 
    Users also gain access to branding assets (e.g., logos, icons), enabling them to enrich applications and analyses with visually consistent, contextually relevant information.
    
    Use Cases: Company research, data integration, application enhancement, due diligence & compliance. 

### Ticker Types -> (POLYGON_TICKER_TYPES_URL) 

    Retrieve a list of all ticker types supported by Polygon.io. 
    This endpoint categorizes tickers across asset classes, markets, and instruments, helping users understand the different classifications and their attributes.

    Use Cases: Data classification, filtering mechanisms, educational reference, system integration 

### Related Tickers -> (POLYGON_RELATED_TICKERS_URL) 

    Retrieve a list of tickers related to a specified ticker, identified through an analysis of news coverage and returns data. 
    This endpoint helps users discover peers, competitors, or thematically similar companies, aiding in comparative analysis, portfolio diversification, and market research.

    Use Cases: Peer identification, comparative analysis, portfolio diversification, market research. 

# ** FINANCIALS & MARKET SNAPSHOTS

## Polygon Financials -> (POLYGON_FINANCIALS_URL) 

    Retrieve historical financial data for a specified stock ticker, derived from company SEC filings and extracted via XBRL. 
    This experimental endpoint provides a wide range of financial metrics, including income statements, balance sheets, cash flow statements, 
    and comprehensive income figures. By examining these standardized, machine-readable financial details, users can conduct in-depth fundamental analysis, 
    track corporate performance trends, and compare financials across different reporting periods.

    Use Cases: Fundamental analysis, trend identification, cross-company comparisons, research & modeling. 

## Polygon Short Interest -> (POLYGON_SHORT_INTEREST_URL)   

    Retrieve bi-monthly aggregated short interest data reported to FINRA by broker-dealers for a specified stock ticker. Short interest represents the total number of shares sold short but not yet covered or closed out, serving as an indicator of market sentiment and potential price movements. High short interest can signal bearish sentiment or highlight opportunities such as potential short squeezes. This endpoint provides essential insights for investors monitoring market positioning and sentiment.

    Use Cases: Market sentiment analysis, short-squeeze prediction, risk management, trading strategy refinement 

## Polygon Short Volume -> (POLYGON_SHORT_VOLUME_URL) 

    Retrieve daily aggregated short sale volume data reported to FINRA from off-exchange trading venues and alternative trading systems (ATS) for a specified stock ticker. Unlike short interest, which measures outstanding short positions at specific reporting intervals, short volume captures the daily trading activity of short sales. Monitoring short volume helps users detect immediate market sentiment shifts, analyze trading behavior, and identify trends in short-selling activity that may signal upcoming price movements.

    Use Cases: Intraday sentiment analysis, short-sale trend identification, liquidity analysis, trading strategy optimization.

## Polygon Market Movers -> (POLYGON_TOP_MOVERS_URL) 

    Retrieve snapshot data highlighting the top 20 gainers or losers in the U.S. stock market. Gainers are stocks with the largest percentage increase since the previous day’s close, and losers are those with the largest percentage decrease. To ensure meaningful insights, only tickers with a minimum trading volume of 10,000 are included. Snapshot data is cleared daily at 3:30 AM EST and begins repopulating as exchanges report new information, typically starting around 4:00 AM EST. By focusing on these market movers, users can quickly identify significant price shifts and monitor evolving market dynamics.

    Use Cases: Market movers identification, trading strategies, market sentiment analysis, portfolio adjustments.

## Full Market Snapshot -> (POLYGON_FULL_MARKET_SNAPSHOT_URL) 

    Retrieve a comprehensive snapshot of the entire U.S. stock market, covering over 10,000+ actively traded tickers in a single response. This endpoint consolidates key information like pricing, volume, and trade activity to provide a full-market-snapshot view, eliminating the need for multiple queries. Snapshot data is cleared daily at 3:30 AM EST and begins to repopulate as exchanges report new data, which can start as early as 4:00 AM EST. By accessing all tickers at once, users can efficiently monitor broad market conditions, perform bulk analyses, and power applications that require complete, current market information.

    Use Cases: Market overview, bulk data processing, heat maps/dashboards, automated monitoring.

