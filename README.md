# Harshit-fleximart-data-architecture

# FlexiMart Data Architecture Project

**Student Name:** Harshit Dixit 
**Student ID:**  bitsom_ba_25071947
**Email:** hardixit@gmail.com
**Date:** 08 Jan 2026

---

## Project Overview

The FlexiMart Data Architecture Project demonstrates the end-to-end design and implementation of a modern data architecture for an e-commerce platform. The project covers relational ETL pipelines, NoSQL database analysis, and data warehousing with OLAP analytics to support business decision-making. It showcases practical data engineering skills using MySQL, MongoDB, and dimensional modeling techniques.

---

## 📂 Repository Structure

├── data/
│ ├── customers_raw.csv
│ ├── products_raw.csv
│ └── sales_raw.csv
│
├── part1-database-etl/
│ ├── etl_pipeline.py
│ ├── schema_documentation.md
│ ├── business_queries.sql
│ ├── data_quality_report.txt
│ └── requirements.txt
│
├── part2-nosql/
│ ├── nosql_analysis.md
│ ├── mongodb_operations.js
│ └── products_catalog.json
│
├── part3-datawarehouse/
│ ├── star_schema_design.md
│ ├── warehouse_schema.sql
│ ├── warehouse_data.sql
│ └── analytics_queries.sql
│
└── README.md


---

## 🛠 Technologies Used

- **Python 3.x** – ETL pipeline implementation  
- **pandas** – Data cleaning and transformation  
- **mysql-connector-python** – MySQL connectivity  
- **MySQL 8.0** – Relational database and data warehouse  
- **MongoDB 6.0** – NoSQL product catalog storage  
- **MongoDB Shell (mongosh)** – MongoDB operations  
- **SQL** – OLAP and business analytics queries  

---

##  Setup Instructions

###  Database Setup (MySQL)

```bash
# Create operational and warehouse databases
mysql -u root -p -e "CREATE DATABASE fleximart;"
mysql -u root -p -e "CREATE DATABASE fleximart_dw;"

# Run Part 1 – ETL Pipeline
python part1-database-etl/etl_pipeline.py

# Run Part 1 – Business Queries
mysql -u root -p fleximart < part1-database-etl/business_queries.sql

# Run Part 3 – Data Warehouse Schema
mysql -u root -p fleximart_dw < part3-datawarehouse/warehouse_schema.sql

# Load Warehouse Data
mysql -u root -p fleximart_dw < part3-datawarehouse/warehouse_data.sql

# Run OLAP Analytics Queries
mysql -u root -p fleximart_dw < part3-datawarehouse/analytics_queries.sql



# Import product catalog data
mongoimport --db fleximart_nosql --collection products \
--file part2-nosql/products_catalog.json --jsonArray

# Run MongoDB operations
mongosh part2-nosql/mongodb_operations.js

# Key Learnings

Through this project, I gained hands-on experience in building a complete data pipeline from raw transactional data to analytical insights. I learned how to clean and transform data using Python, design normalized relational schemas, and implement dimensional models for analytics. Additionally, I explored NoSQL concepts with MongoDB and understood trade-offs between relational and document-based databases.

# Challenges Faced

Handling inconsistent and dirty data
Solution: Implemented robust data validation, deduplication, and date standardization in the ETL pipeline.

Managing schema differences between RDBMS and NoSQL
Solution: Carefully mapped relational attributes to flexible MongoDB documents and used aggregation pipelines for analytics.