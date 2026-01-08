/* =========================================================
   Query 1: Monthly Sales Drill-Down Analysis
   Business Scenario:
   The CEO wants to see sales performance broken down by
   year, quarter, and month for 2024.
   Demonstrates drill-down from Year → Quarter → Month.
   ========================================================= */

SELECT
    d.year,
    d.quarter,
    d.month_name,
    SUM(f.total_amount) AS total_sales,
    SUM(f.quantity_sold) AS total_quantity
FROM fact_sales f
JOIN dim_date d
    ON f.date_key = d.date_key
WHERE
    d.year = 2024
GROUP BY
    d.year,
    d.quarter,
    d.month,
    d.month_name
ORDER BY
    d.year,
    d.quarter,
    d.month;


/* =========================================================
   Query 2: Product Performance Analysis
   Business Scenario:
   Identify the top 10 products by revenue, showing category,
   total units sold, total revenue, and revenue contribution
   percentage.
   ========================================================= */

SELECT
    p.product_name,
    p.category,
    SUM(f.quantity_sold) AS units_sold,
    SUM(f.total_amount) AS revenue,
    ROUND(
        SUM(f.total_amount) * 100.0 /
        SUM(SUM(f.total_amount)) OVER (),
        2
    ) AS revenue_percentage
FROM fact_sales f
JOIN dim_product p
    ON f.product_key = p.product_key
GROUP BY
    p.product_name,
    p.category
ORDER BY
    revenue DESC
LIMIT 10;


/* =========================================================
   Query 3: Customer Segmentation Analysis
   Business Scenario:
   Segment customers into High, Medium, and Low Value
   based on total spending and show customer count and
   revenue metrics for each segment.
   ========================================================= */

WITH customer_spending AS (
    SELECT
        c.customer_key,
        c.customer_name,
        SUM(f.total_amount) AS total_spent
    FROM fact_sales f
    JOIN dim_customer c
        ON f.customer_key = c.customer_key
    GROUP BY
        c.customer_key,
        c.customer_name
)

SELECT
    CASE
        WHEN total_spent > 50000 THEN 'High Value'
        WHEN total_spent BETWEEN 20000 AND 50000 THEN 'Medium Value'
        ELSE 'Low Value'
    END AS customer_segment,
    COUNT(*) AS customer_count,
    SUM(total_spent) AS total_revenue,
    ROUND(AVG(total_spent), 2) AS avg_revenue_per_customer
FROM customer_spending
GROUP BY
    customer_segment
ORDER BY
    total_revenue DESC;
