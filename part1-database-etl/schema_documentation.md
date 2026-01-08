# Database Schema Documentation – FlexiMart

## 1. Entity–Relationship Description (Text Format)

The FlexiMart database is designed to support an e-commerce system that manages customers, products, and sales transactions.  
The schema consists of four core entities: **customers**, **products**, **orders**, and **order_items**.

- A **customer** can place multiple **orders**.
- Each **order** belongs to exactly one customer.
- An **order** can contain multiple **products**, which are stored in the **order_items** table.
- The **order_items** table resolves the many-to-many relationship between orders and products.

This design ensures data integrity, avoids redundancy, and supports efficient transactional and analytical queries.

---

## 2. ENTITY: customers

### Purpose
Stores customer personal and registration information.

### Attributes
- **customer_id**: Unique identifier for each customer (Primary Key)
- **first_name**: Customer’s first name
- **last_name**: Customer’s last name
- **email**: Customer’s email address (Unique, Not Null)
- **phone**: Customer’s contact number
- **city**: City where the customer resides
- **registration_date**: Date when the customer registered

### Relationships
- One customer can place **many orders**  
  (1 : M relationship with the `orders` table)

---

## 3. ENTITY: products

### Purpose
Stores product catalog information.

### Attributes
- **product_id**: Unique identifier for each product (Primary Key)
- **product_name**: Name of the product
- **category**: Product category (e.g., Electronics, Fashion)
- **price**: Selling price of the product
- **stock_quantity**: Available inventory count

### Relationships
- One product can appear in **many order items**  
  (1 : M relationship with the `order_items` table)

---

## 4. ENTITY: orders

### Purpose
Stores order-level transaction information.

### Attributes
- **order_id**: Unique identifier for each order (Primary Key)
- **customer_id**: Identifier of the customer who placed the order (Foreign Key)
- **order_date**: Date on which the order was placed
- **total_amount**: Total monetary value of the order
- **status**: Current order status (Completed, Pending, Cancelled)

### Relationships
- Each order belongs to **one customer**
- One order can have **many order items**

---

## 5. ENTITY: order_items

### Purpose
Stores product-level details for each order.

### Attributes
- **order_item_id**: Unique identifier for each order item (Primary Key)
- **order_id**: Associated order identifier (Foreign Key)
- **product_id**: Associated product identifier (Foreign Key)
- **quantity**: Number of units purchased
- **unit_price**: Price per unit at the time of sale
- **subtotal**: Total cost for the item (quantity × unit_price)

### Relationships
- Many order items belong to **one order**
- Many order items reference **one product**

---

## 6. Normalization Explanation (3NF)

The FlexiMart database schema is designed in **Third Normal Form (3NF)** to eliminate redundancy and ensure data integrity.  
In this design, each table represents a single entity, and all non-key attributes depend only on the primary key.

**Functional Dependencies**:
- In the `customers` table, all attributes depend on `customer_id`.
- In the `products` table, attributes depend on `product_id`.
- In the `orders` table, attributes depend on `order_id`.
- In the `order_items` table, attributes depend on `order_item_id`.

There are **no partial dependencies**, as all tables use single-column primary keys.  
There are **no transitive dependencies**, because non-key attributes do not depend on other non-key attributes.

This design avoids:
- **Update anomalies**: Customer or product details are stored once and updated in a single location.
- **Insert anomalies**: New customers or products can be added without requiring an order.
- **Delete anomalies**: Deleting an order does not remove customer or product information.

By separating transactional data into related tables and enforcing foreign key constraints, the schema maintains consistency, scalability, and efficient query performance.

---

## 7. Sample Data Representation

### customers (Sample Records)

| customer_id | first_name | last_name | email                     | city       | registration_date |
|------------|------------|-----------|---------------------------|------------|-------------------|
| 1 | Rahul | Sharma | rahul.sharma@gmail.com | Bangalore | 2023-01-15 |
| 2 | Priya | Patel | priya.patel@yahoo.com | Mumbai | 2023-02-20 |
| 3 | Sneha | Reddy | sneha.reddy@gmail.com | Hyderabad | 2023-04-15 |

---

### products (Sample Records)

| product_id | product_name | category | price | stock_quantity |
|-----------|--------------|----------|-------|----------------|
| 1 | Samsung Galaxy S21 | Electronics | 45999.00 | 150 |
| 2 | Nike Running Shoes | Fashion | 3499.00 | 80 |
| 3 | Apple MacBook Pro | Electronics | 52999.00 | 45 |

---

### orders (Sample Records)

| order_id | customer_id | order_date | total_amount | status |
|---------|-------------|------------|--------------|--------|
| 101 | 1 | 2024-01-15 | 45999.00 | Completed |
| 102 | 2 | 2024-01-16 | 5998.00 | Completed |
| 103 | 3 | 2024-02-01 | 12999.00 | Completed |

---

### order_items (Sample Records)

| order_item_id | order_id | product_id | quantity | unit_price | subtotal |
|--------------|----------|------------|----------|------------|----------|
| 1 | 101 | 1 | 1 | 45999.00 | 45999.00 |
| 2 | 102 | 2 | 2 | 2999.00 | 5998.00 |
| 3 | 103 | 3 | 1 | 12999.00 | 12999.00 |
