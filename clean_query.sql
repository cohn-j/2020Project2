SELECT timestamp, open, high, low, close, volume, Ticker, Sector, PERatio, EPS, DividendYield
FROM timestamp_stocks
JOIN overview 
ON (timestamp_stocks.Ticker = overview.Symbol)
WHERE timestamp BETWEEN '2015-12-31' AND '2021-01-08'
ORDER BY ticker ASC, timestamp DESC
;