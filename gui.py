import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# Connect to SQLite database
conn = sqlite3.connect("ecommerce.db")

# Streamlit Page Configuration
st.set_page_config(page_title="Ecommerce Dashboard", layout="wide")
st.title("📊 Ecommerce Data Dashboard")

# Sidebar Navigation
chart_type = st.sidebar.selectbox("Select a visualization", [
    "Revenue by Product",
    "Revenue by Customer",
    "Revenue by Day of Week"
])

# Revenue by Product
if chart_type == "Revenue by Product":
    st.header("📦 Revenue by Product")
    query = """
        SELECT p.name, SUM(oi.quantity * oi.unit_price) AS revenue
        FROM order_items oi
        JOIN products p ON oi.product_id = p.product_id
        GROUP BY p.name
        ORDER BY revenue DESC
        LIMIT 10;
    """
    df = pd.read_sql(query, conn)
    st.bar_chart(df.set_index("name"))

# Revenue by Customer
elif chart_type == "Revenue by Customer":
    st.header("👤 Revenue by Customer")
    query = """
        SELECT c.name AS customer_name, SUM(oi.quantity * oi.unit_price) AS revenue
        FROM order_items oi
        JOIN orders o ON oi.order_id = o.order_id
        JOIN customers c ON o.customer_id = c.customer_id
        GROUP BY c.name
        ORDER BY revenue DESC
        LIMIT 10;
    """
    df = pd.read_sql(query, conn)
    st.bar_chart(df.set_index("customer_name"))


# Revenue by Day of Week
elif chart_type == "Revenue by Day of Week":
    st.header("📅 Revenue by Day of Week")
    query = """
        SELECT c.day_of_week, SUM(oi.quantity * oi.unit_price) AS daily_sales
        FROM order_items oi
        JOIN orders o ON oi.order_id = o.order_id
        JOIN calendar c ON o.order_date = c.date
        GROUP BY c.day_of_week
    """
    df = pd.read_sql(query, conn)
    # Ensure correct order of weekdays
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    df["day_of_week"] = pd.Categorical(df["day_of_week"], categories=weekdays, ordered=True)
    df = df.sort_values("day_of_week")
    st.bar_chart(df.set_index("day_of_week"))

# Close the connection
conn.close()
