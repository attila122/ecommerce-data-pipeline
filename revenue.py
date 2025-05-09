import sqlite3
import matplotlib.pyplot as plt
import pandas as pd

# Connect to the database
conn = sqlite3.connect('ecommerce.db')

# 1. Total Revenue by Product
def total_revenue_by_product():
    query = """
    SELECT p.name, SUM(oi.quantity * oi.unit_price) AS revenue
    FROM order_items oi
    JOIN products p ON oi.product_id = p.product_id
    GROUP BY p.name
    ORDER BY revenue DESC;
    """
    df = pd.read_sql(query, conn)
    plt.figure(figsize=(10,6))
    plt.bar(df['name'], df['revenue'], color='skyblue')
    plt.title('Total Revenue by Product')
    plt.xlabel('Product')
    plt.ylabel('Revenue ($)')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

# 2. Top 5 Most Sold Products
def top_sold_products():
    query = """
    SELECT p.name, SUM(oi.quantity) AS total_sold
    FROM order_items oi
    JOIN products p ON oi.product_id = p.product_id
    GROUP BY p.name
    ORDER BY total_sold DESC
    LIMIT 5;
    """
    df = pd.read_sql(query, conn)
    plt.figure(figsize=(10,6))
    plt.bar(df['name'], df['total_sold'], color='lightgreen')
    plt.title('Top 5 Most Sold Products')
    plt.xlabel('Product')
    plt.ylabel('Quantity Sold')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def revenue_by_day_of_week():
    query = """
    SELECT c.day_of_week, SUM(oi.quantity * oi.unit_price) AS daily_sales
    FROM order_items oi
    JOIN orders o ON oi.order_id = o.order_id
    JOIN calendar c ON o.order_date = c.date
    GROUP BY c.day_of_week
    """
    
    # Run the query and load the result into a dataframe
    df = pd.read_sql(query, conn)
    
    # Create a mapping for sorting days of the week
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    df['day_of_week'] = pd.Categorical(df['day_of_week'], categories=day_order, ordered=True)
    
    # Sort by day_of_week
    df = df.sort_values('day_of_week')
    
    # Plot the result
    plt.figure(figsize=(10,6))
    plt.bar(df['day_of_week'], df['daily_sales'], color='coral')
    plt.title('Sales by Day of the Week')
    plt.xlabel('Day of the Week')
    plt.ylabel('Revenue ($)')
    plt.tight_layout()
    plt.show()


# 4. Total Orders by Customer
def total_orders_by_customer():
    query = """
    SELECT c.name, COUNT(o.order_id) AS total_orders
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    GROUP BY c.name;
    """
    df = pd.read_sql(query, conn)
    plt.figure(figsize=(12,6))
    plt.barh(df['name'], df['total_orders'], color='lightblue')
    plt.title('Total Orders by Customer')
    plt.xlabel('Total Orders')
    plt.ylabel('Customer')
    plt.tight_layout()
    plt.show()

# Main function to call all visualizations
if __name__ == "__main__":
    total_revenue_by_product()
    top_sold_products()
    revenue_by_day_of_week()
    total_orders_by_customer()

    # Close the connection
    conn.close()
