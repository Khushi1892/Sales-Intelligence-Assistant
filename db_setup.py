import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

# Connect to MySQL
connection = pymysql.connect(
    host=os.getenv("MYSQL_HOST"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD")
)

cursor = connection.cursor()
print(" Connected to MySQL!")

# Create Database
cursor.execute("CREATE DATABASE IF NOT EXISTS sales_db")
cursor.execute("USE sales_db")

print(" Database Created")

# Customers Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS customers(
customer_id INT AUTO_INCREMENT PRIMARY KEY,
customer_name VARCHAR(100),
region VARCHAR(50),
segment VARCHAR(50)
)
""")


# Products Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS products(
product_id INT AUTO_INCREMENT PRIMARY KEY,
product_name VARCHAR(100),
category VARCHAR(50),
price FLOAT
)
""")


# Employees Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS employees(
employee_id INT AUTO_INCREMENT PRIMARY KEY,
employee_name VARCHAR(100),
department VARCHAR(50)
)
""")


# Deals Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS deals(
deal_id INT AUTO_INCREMENT PRIMARY KEY,
customer_id INT,
product_id INT,
employee_id INT,
revenue FLOAT,
status VARCHAR(50),
close_date DATE,
FOREIGN KEY(customer_id) REFERENCES customers(customer_id),
FOREIGN KEY(product_id) REFERENCES products(product_id),
FOREIGN KEY(employee_id) REFERENCES employees(employee_id)
)
""")


# Tickets Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS tickets(
ticket_id INT AUTO_INCREMENT PRIMARY KEY,
customer_id INT,
issue TEXT,
resolved BOOLEAN,
created_date DATE,
FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
)
""")


print(" Tables Created")


# Customers
customers = [
("Acme Corp","North","Enterprise"),
("BrightTech","South","SMB"),
("CloudBase","East","Enterprise"),
("DataFlow","West","SMB"),
("EdgeSoft","North","Mid-Market")
]
cursor.executemany(
"INSERT INTO customers(customer_name,region,segment) VALUES(%s,%s,%s)",customers)

# Products
products=[
("DataSuite Basic","Software",5000),
("DataSuite Pro","Software",20000),
("Enterprise Suite","Software",50000),
("Analytics Dashboard","Analytics",15000)
]
cursor.executemany(
"INSERT INTO products(product_name,category,price) VALUES(%s,%s,%s)",products)

# Employees
employees=[
("Rahul Sharma","Sales"),
("Priya Singh","Sales"),
("Amit Verma","Support")
]
cursor.executemany(
"INSERT INTO employees(employee_name,department) VALUES(%s,%s)",employees)

# Deals
deals=[
(1,1,1,50000,"Closed Won","2025-01-15"),
(2,2,2,20000,"Closed Won","2025-02-01"),
(3,3,1,100000,"Open","2025-03-05"),
(4,2,2,30000,"Closed Lost","2025-02-10")
]
cursor.executemany(
"""INSERT INTO deals(customer_id,product_id,employee_id,revenue,status,close_date) VALUES(%s,%s,%s,%s,%s,%s)""",deals)

# Tickets
tickets=[
(1,"Unable to login",True,"2025-01-12"),
(2,"Invoice issue",False,"2025-02-05"),
(3,"Dashboard slow",True,"2025-02-18")
]
cursor.executemany(
"""INSERT INTO tickets(customer_id,issue,resolved,created_date) VALUES(%s,%s,%s,%s)""",tickets)

connection.commit()
cursor.close()
connection.close()

print(" Database Setup Complete!")