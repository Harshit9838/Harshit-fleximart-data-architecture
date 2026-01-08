import pandas as pd
import mysql.connector
from mysql.connector import Error
import re
import os

# -----------------------------
# Database Configuration
# -----------------------------
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": os.getenv("MYSQL_PASSWORD"),
    "database": "fleximart"
}

# -----------------------------
# Helper Functions
# -----------------------------
def standardize_phone(phone):
    if pd.isna(phone):
        return None
    digits = re.sub(r"\D", "", str(phone))
    if len(digits) >= 10:
        return f"+91-{digits[-10:]}"
    return None


def standardize_category(cat):
    if pd.isna(cat):
        return None
    return str(cat).strip().title()


def standardize_date(date_val):
    if pd.isna(date_val):
        return None
    return pd.to_datetime(
        date_val,
        dayfirst=True,
        errors="coerce"
    ).date()


# -----------------------------
# ETL PROCESS
# -----------------------------
def run_etl():
    report = {}
    conn = None
    cursor = None


    # =============================
    # EXTRACT
    # =============================
    customers = pd.read_csv("data/customers_raw.csv")
    products = pd.read_csv("data/products_raw.csv")
    sales = pd.read_csv("data/sales_raw.csv")

    report["customers_records_read"] = len(customers)
    report["products_records_read"] = len(products)
    report["sales_records_read"] = len(sales)

    # =============================
    # TRANSFORM - CUSTOMERS
    # =============================
    customers = customers.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    before = len(customers)
    customers.drop_duplicates(inplace=True)
    report["customers_duplicates_removed"] = before - len(customers)

    customers["phone"] = customers["phone"].apply(standardize_phone)
    customers["registration_date"] = customers["registration_date"].apply(standardize_date)

    before = len(customers)
    customers.dropna(subset=["email", "registration_date"], inplace=True)
    report["customers_missing_removed"] = before - len(customers)

    # =============================
    # TRANSFORM - PRODUCTS
    # =============================
    products = products.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    before = len(products)
    products.drop_duplicates(inplace=True)
    report["products_duplicates_removed"] = before - len(products)

    products["category"] = products["category"].apply(standardize_category)
    products["stock_quantity"] = products["stock_quantity"].fillna(0)

    avg_price = products["price"].mean()
    products["price"] = products["price"].fillna(avg_price)

    # =============================
    # TRANSFORM - SALES
    # =============================
    sales = sales.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    # Normalize column names
    sales.rename(columns={
        "transaction_date": "order_date"
    }, inplace=True)

    before = len(sales)
    sales.drop_duplicates(subset=["transaction_id"], inplace=True)
    report["sales_duplicates_removed"] = before - len(sales)

    sales["order_date"] = sales["order_date"].apply(standardize_date)

    before = len(sales)
    sales.dropna(subset=["customer_id", "product_id", "order_date"], inplace=True)
    report["sales_invalid_records_removed"] = before - len(sales)

    sales["subtotal"] = sales["quantity"] * sales["unit_price"]

    # =============================
    # LOAD TO MYSQL
    # =============================
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Insert Customers
        for _, row in customers.iterrows():
            cursor.execute("""
                INSERT IGNORE INTO customers
                (first_name, last_name, email, phone, city, registration_date)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                row["first_name"],
                row["last_name"],
                row["email"],
                row["phone"],
                row["city"],
                row["registration_date"]
            ))

        # Insert Products
        for _, row in products.iterrows():
            cursor.execute("""
                INSERT IGNORE INTO products
                (product_name, category, price, stock_quantity)
                VALUES (%s, %s, %s, %s)
            """, (
                row["product_name"],
                row["category"],
                row["price"],
                int(row["stock_quantity"])
            ))

        conn.commit()

        # Insert Orders and Order Items
        for _, row in sales.iterrows():
            cursor.execute("""
                INSERT INTO orders (customer_id, order_date, total_amount, status)
                VALUES (%s, %s, %s, %s)
            """, (
                row["customer_id"],
                row["order_date"],
                row["subtotal"],
                row["status"]
            ))

            order_id = cursor.lastrowid

            cursor.execute("""
                INSERT INTO order_items
                (order_id, product_id, quantity, unit_price, subtotal)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                order_id,
                row["product_id"],
                int(row["quantity"]),
                row["unit_price"],
                row["subtotal"]
            ))

        conn.commit()
        report["records_loaded_successfully"] = "Yes"

    except Error as e:
        report["load_error"] = str(e)

    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None and conn.is_connected():
            conn.close()

    # =============================
    # DATA QUALITY REPORT
    # =============================
    with open("part1-database-etl/data_quality_report.txt", "w") as f:
        for key, value in report.items():
            f.write(f"{key}: {value}\n")


# -----------------------------
# RUN ETL
# -----------------------------
if __name__ == "__main__":
    run_etl()
    print("ETL Pipeline Completed Successfully")
