-- Check which stock grew the most overall
-- Shows best-performing stock over entire period.
SELECT 
    c.company_name,
    MIN(s.close_price) AS min_close,
    MAX(s.close_price) AS max_close,
    (MAX(s.close_price) - MIN(s.close_price)) AS absolute_growth,
    ((MAX(s.close_price) - MIN(s.close_price)) / MIN(s.close_price)) * 100 AS growth_percentage
FROM stock_price_daily s
JOIN company_master c ON s.company_id = c.company_id
GROUP BY c.company_name
ORDER BY growth_percentage DESC;

-- Find the most volatile stock (highest std dev)
-- High volatility = high risk + opportunity.
SELECT 
    c.company_name,
    STDDEV_SAMP(s.close_price) AS volatility
FROM stock_price_daily s
JOIN company_master c ON s.company_id = c.company_id
GROUP BY c.company_name
ORDER BY volatility DESC;

-- Monthly average close price
-- Useful for trend reports
SELECT 
    c.company_name,
    DATE_FORMAT(s.date, '%Y-%m') AS month,
    AVG(s.close_price) AS avg_close
FROM stock_price_daily s
JOIN company_master c ON s.company_id = c.company_id
GROUP BY c.company_name, month
ORDER BY month, c.company_name;

-- RSI Overbought / Oversold Signals
-- RSI > 70 → Overbought
-- RSI < 30 → Oversold

SELECT 
    c.company_name,
    t.date,
    t.rsi,
    CASE 
        WHEN t.rsi > 70 THEN 'Overbought'
        WHEN t.rsi < 30 THEN 'Oversold'
        ELSE 'Neutral'
    END AS s
FROM technical_indicators t
JOIN company_master c ON t.company_id = c.company_id
ORDER BY t.date;

-- MACD Crossover Bullish Signals
-- MACD > 0 → Bullish trend
SELECT 
    c.company_name,
    t.date,
    t.macd
FROM technical_indicators t
JOIN company_master c ON t.company_id = c.company_id
WHERE t.macd > 0
ORDER BY t.date;

-- Highest Trading Volume
-- Shows days with extreme trading activity.
SELECT 
    c.company_name,
    s.date,
    s.volume
FROM stock_price_daily s
JOIN company_master c ON s.company_id = c.company_id
WHERE s.volume = (
    SELECT MAX(volume) FROM stock_price_daily
);
