-- Customer Transaction Analysis: SQL queries (MySQL / PostgreSQL style)
-- Table: transactions(customer_id, first_name, surname, gender, birthdate, amount, date, merchant, category)

-- 1. Headline KPIs
SELECT COUNT(*) AS txns, ROUND(SUM(amount),0) AS revenue, ROUND(AVG(amount),2) AS avg_ticket
FROM transactions;

-- 2. Revenue and share by category
SELECT category, COUNT(*) AS txns, ROUND(SUM(amount),2) AS revenue,
       ROUND(AVG(amount),2) AS avg_ticket,
       ROUND(100*SUM(amount)/SUM(SUM(amount)) OVER (),1) AS revenue_share_pct
FROM transactions GROUP BY category ORDER BY revenue DESC;

-- 3. Monthly revenue trend with month-over-month change
WITH m AS (
  SELECT DATE_FORMAT(date,'%Y-%m') AS month, SUM(amount) AS revenue
  FROM transactions GROUP BY 1)
SELECT month, ROUND(revenue,0) AS revenue,
       ROUND(100*(revenue - LAG(revenue) OVER (ORDER BY month)) / LAG(revenue) OVER (ORDER BY month),1) AS mom_pct
FROM m ORDER BY month;

-- 4. Revenue by age group
SELECT CASE WHEN age<=24 THEN '17-24' WHEN age<=34 THEN '25-34' WHEN age<=44 THEN '35-44'
            WHEN age<=54 THEN '45-54' WHEN age<=64 THEN '55-64' ELSE '65+' END AS age_group,
       COUNT(*) AS txns, ROUND(SUM(amount),0) AS revenue
FROM (SELECT *, TIMESTAMPDIFF(YEAR, birthdate, date) AS age FROM transactions) t
GROUP BY age_group ORDER BY age_group;

-- 5. Top 10 merchants by revenue
SELECT merchant, COUNT(*) AS txns, ROUND(SUM(amount),2) AS revenue
FROM transactions GROUP BY merchant ORDER BY revenue DESC LIMIT 10;

-- 6. Top 10% of transactions: share of revenue
WITH r AS (SELECT amount, NTILE(10) OVER (ORDER BY amount DESC) AS decile FROM transactions)
SELECT ROUND(100*SUM(CASE WHEN decile=1 THEN amount END)/SUM(amount),1) AS top10_pct_share FROM r;

-- 7. Data quality: missing gender
SELECT SUM(gender IS NULL) AS missing_gender, ROUND(100*AVG(gender IS NULL),1) AS pct FROM transactions;
