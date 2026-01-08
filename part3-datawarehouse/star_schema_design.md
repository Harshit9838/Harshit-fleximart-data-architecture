# Star Schema Design – FlexiMart Data Warehouse

## Section 1: Schema Overview

The FlexiMart data warehouse uses a **star schema** to support efficient analytical queries on historical sales data. The schema is centered around a single fact table connected to multiple dimension tables.

---

### FACT TABLE: fact_sales

**Grain:**  
One row per **product per order line item**.

**Business Process:**  
Sales transactions generated from customer purchases.

**Measures (Numeric Facts):**
- **quantity_sold**: Number of units sold for a product in an order
- **unit_price**: Price per unit at the time of sale
- **discount_amount**: Discount applied on the line item
- **total_amount**: Final amount calculated as  
  `(quantity_sold × unit_price) − discount_amount`

**Foreign Keys:**
- **date_key** → dim_date
- **product_key** → dim_product
- **customer_key** → dim_customer

---

### DIMENSION TABLE: dim_date

**Purpose:**  
Provides a standardized date dimension for time-based analysis.

**Type:**  
Conformed dimension

**Attributes:**
- **date_key (PK)**: Surrogate key in YYYYMMDD format
- **full_date**: Actual calendar date
- **day_of_week**: Monday, Tuesday, etc.
- **day_of_month**: Numeric day of month
- **month**: Month number (1–12)
- **month_name**: January, February, etc.
- **quarter**: Q1, Q2, Q3, Q4
- **year**: Calendar year
- **is_weekend**: Boolean flag indicating weekend

---

### DIMENSION TABLE: dim_product

**Purpose:**  
Stores descriptive product information for analysis.

**Attributes:**
- **product_key (PK)**: Surrogate product key
- **product_id**: Business product identifier
- **product_name**: Name of the product
- **category**: Product category (Electronics, Fashion, etc.)
- **subcategory**: Product subcategory
- **unit_price**: Standard selling price

---

### DIMENSION TABLE: dim_customer

**Purpose:**  
Stores customer demographic and segmentation details.

**Attributes:**
- **customer_key (PK)**: Surrogate customer key
- **customer_id**: Business customer identifier
- **customer_name**: Full name of the customer
- **city**: City of residence
- **state**: State of residence
- **customer_segment**: Segment such as High Value, Medium Value, Low Value

---

## Section 2: Design Decisions

The chosen granularity of **transaction line-item level** ensures the highest level of analytical detail. Each row in the fact table represents a single product sold within an order, allowing precise analysis of product performance, customer behavior, and revenue patterns. This granularity supports detailed reporting while still enabling aggregation at higher levels such as daily, monthly, or yearly sales.

Surrogate keys are used instead of natural keys to improve performance and maintain stability. Natural keys such as product IDs or customer IDs can change over time or differ across source systems. Surrogate keys provide compact, integer-based joins that improve query efficiency and simplify slowly changing dimension management.

The star schema design supports **drill-down and roll-up operations** effectively. Analysts can roll up sales data from daily to monthly or yearly levels using the date dimension, or drill down from category-level sales to individual products. Similarly, customer analysis can move between segments, cities, and individual customers with minimal query complexity.

---

## Section 3: Sample Data Flow

### Source Transaction
Order #101  
Customer: John Doe  
Product: Laptop  
Quantity: 2  
Unit Price: 50000  

---

### Data Warehouse Representation

**fact_sales**
```json
{
  "date_key": 20240115,
  "product_key": 5,
  "customer_key": 12,
  "quantity_sold": 2,
  "unit_price": 50000,
  "discount_amount": 0,
  "total_amount": 100000
}
