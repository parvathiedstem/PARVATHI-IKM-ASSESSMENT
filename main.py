import pyodbc
import psycopg2
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)

connection_postgres = psycopg2.connect(
    host="localhost",
    database="ecomdata",
    user="postgres",
    password="Parvathi2022")

connection_sql = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                                "Server=.;"
                                "Database=ecommerce;"
                                "Trusted_Connection=yes;")


def migrate_customers():
    cursor_postgres = connection_postgres.cursor()
    cursor_sql = connection_sql.cursor()
    # Execute a query
    cursor_sql.execute('SELECT * FROM customers')
    customers = cursor_sql.fetchall()
    count = 0
    for row in customers:
        count += 1
        name = row[1] if row[1] != None else ""
        email = row[2] if row[2] != None else ""
        cursor_postgres.execute(
            f"INSERT INTO customers (id,name,email,phone)  VALUES ('{row[0]}','{name}','{email}','{row[3]}')",

        )
        connection_postgres.commit()
    logging.info(f"{count} customers rows Migrated")
    cursor_postgres.close()


def migrate_orders():
    cursor_postgres = connection_postgres.cursor()
    cursor_sql = connection_sql.cursor()
    cursor_sql.execute('SELECT * FROM orders')
    orders = cursor_sql.fetchall()
    count = 0
    for row in orders:
        count += 1
        total_price = row[2] if row[2] != None else 0
        created_at = row[3] if row[3] != None else datetime.now()
        cursor_postgres.execute(
            f"INSERT INTO orders (id,customer_id,total_price,created_at)  VALUES ('{row[0]}','{row[1]}','{total_price}','{created_at}')",
        )
        connection_postgres.commit()
    logging.info(f"{count} orders rows Migrated")
    cursor_postgres.close()


def migrate_products():
    cursor_postgres = connection_postgres.cursor()
    cursor_sql = connection_sql.cursor()
    cursor_sql.execute('SELECT * FROM products')

    products = cursor_sql.fetchall()
    count = 0
    for row in products:
        count += 1
        name = row[1] if row[1] != None else ""
        price = row[2] if row[2] != None else 0
        cursor_postgres.execute(
            f"INSERT INTO products (id,name,price)  VALUES ('{row[0]}','{name}','{price}')",
        )
        connection_postgres.commit()
    logging.info(f"{count} products rows Migrated")
    cursor_postgres.close()


if __name__ == '__main__':
    migrate_customers()
    migrate_orders()
    migrate_products()
