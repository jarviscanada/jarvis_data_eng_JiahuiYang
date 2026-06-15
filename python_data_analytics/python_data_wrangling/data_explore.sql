-- Show table schema 
\d+ retail;

-- Show first 10 rows
SELECT * FROM retail limit 10;

-- Check # of records
SELECT COUNT(*) FROM retail;

-- number of clients (e.g. unique client ID)
SELECT COUNT(DISTINCT customer_id) FROM retail;

-- invoice date range (e.g. max/min dates)
SELECT
    MAX(invoice_date) as max,
    MIN(invoice_date) as min
FROM retail;

-- number of SKU/merchants (e.g. unique stock code)
SELECT COUNT(DISTINCT stock_code) FROM retail;

-- Calculate average invoice amount excluding invoices with a negative amount (e.g. canceled orders have negative amount)
WITH invoice_total AS(
    SELECT
        invoice_no,
        SUM(quantity * unit_price) AS invoice_total
    FROM retail
    GROUP BY invoice_no
    HAVING SUM(quantity * unit_price) > 0
)

SELECT
    AVG(invoice_total) as avg
FROM invoice_total;

-- Calculate total revenue (e.g. sum of unit_price * quantity)
SELECT
    SUM(unit_price * quantity) as total
FROM retail;

-- Calculate total revenue by YYYYMM
WITH YYYYMM AS (
    SELECT
        quantity * unit_price as price,
        to_char(invoice_date, 'YYYYMM') as YYYYMM
    FROM retail)

SELECT
    YYYYMM,
    SUM(price) as total_revenue
FROM YYYYMM
GROUP BY YYYYMM
ORDER BY YYYYMM;


