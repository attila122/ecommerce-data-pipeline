import sqlite3
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

def initialize_db():
    with open("db/schema.sql", "r") as f:
        schema = f.read()
    conn = sqlite3.connect("ecommerce.db")
    cursor = conn.cursor()
    cursor.executescript(schema)
    conn.commit()
    conn.close()
    print("✅ Database initialized.")

def load_fake_data():
    conn = sqlite3.connect("ecommerce.db")
    cursor = conn.cursor()

    # --- Customers ---
    customers = []
    for i in range(1, 21):
        customers.append((
            i,
            fake.name(),
            random.choice(["18-25", "26-35", "36-50", "50+"]),
            random.choice(["Male", "Female", "Other"]),
            fake.city()
        ))
    cursor.executemany("""
        INSERT INTO customers (customer_id, name, age_group, gender, location)
        VALUES (?, ?, ?, ?, ?);
    """, customers)

    # --- Products ---
    products = [
        (1, "iPhone 14", "Electronics", 799.99),
        (2, "Samsung TV", "Electronics", 499.99),
        (3, "Nike Shoes", "Apparel", 120.00),
        (4, "Gaming Chair", "Furniture", 250.00),
        (5, "Blender", "Home", 89.99)
    ]
    cursor.executemany("""
        INSERT INTO products (product_id, name, category, cost)
        VALUES (?, ?, ?, ?);
    """, products)

    # --- Calendar ---
    start_date = datetime(2023, 1, 1)
    calendar_rows = []
    for i in range(30):
        date = start_date + timedelta(days=i)
        calendar_rows.append((
            date.strftime("%Y-%m-%d"),
            date.year,
            date.month,
            date.day,
            date.strftime("%A")
        ))
    cursor.executemany("""
        INSERT INTO calendar (date, year, month, day, day_of_week)
        VALUES (?, ?, ?, ?, ?);
    """, calendar_rows)

    # --- Orders & Items ---
    order_id = 1
    order_item_id = 1
    orders = []
    order_items = []
    for _ in range(50):
        cust_id = random.randint(1, 20)
        date = (start_date + timedelta(days=random.randint(0, 29))).strftime("%Y-%m-%d")
        orders.append((order_id, cust_id, date))
        for _ in range(random.randint(1, 3)):
            product = random.choice(products)
            quantity = random.randint(1, 5)
            order_items.append((
                order_item_id,
                order_id,
                product[0],
                quantity,
                product[3]
            ))
            order_item_id += 1
        order_id += 1
    cursor.executemany("""
        INSERT INTO orders (order_id, customer_id, order_date)
        VALUES (?, ?, ?);
    """, orders)
    cursor.executemany("""
        INSERT INTO order_items (order_item_id, order_id, product_id, quantity, unit_price)
        VALUES (?, ?, ?, ?, ?);
    """, order_items)

    conn.commit()
    conn.close()
    print("✅ Fake data inserted.")

if __name__ == "__main__":
    initialize_db()
    load_fake_data()
