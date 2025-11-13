CREATE DATABASE IF NOT EXISTS stock_market;

USE stock_market;

SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS stock_price_daily;
DROP TABLE IF EXISTS technical_indicators;
DROP TABLE IF EXISTS company_master;

SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE company_master (
    company_id INT AUTO_INCREMENT PRIMARY KEY,
    company_name VARCHAR(100),
    ticker VARCHAR(20),
    sector VARCHAR(50)
);

CREATE TABLE stock_price_daily (
    price_id INT AUTO_INCREMENT PRIMARY KEY,
    company_id INT,
    date DATE,
    open_price DECIMAL(10,2),
    high_price DECIMAL(10,2),
    low_price DECIMAL(10,2),
    close_price DECIMAL(10,2),
    adj_close_price DECIMAL(10,2),
    volume BIGINT,
    FOREIGN KEY (company_id) REFERENCES company_master(company_id)
);

CREATE TABLE technical_indicators (
    indicator_id INT AUTO_INCREMENT PRIMARY KEY,
    company_id INT,
    date DATE,
    sma_20 DECIMAL(10,2),
    sma_50 DECIMAL(10,2),
    ema_20 DECIMAL(10,2),
    ema_50 DECIMAL(10,2),
    rsi DECIMAL(10,2),
    macd DECIMAL(10,2),
    FOREIGN KEY (company_id) REFERENCES company_master(company_id)
);

SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE stock_price_daily;
TRUNCATE TABLE technical_indicators;
TRUNCATE TABLE company_master;
SET FOREIGN_KEY_CHECKS = 1;

SELECT * FROM company_master;

SELECT DISTINCT company_id FROM stock_price_daily;

SELECT * FROM technical_indicators LIMIT 20;


