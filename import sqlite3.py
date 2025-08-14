import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------
# 1. Create sample SQLite database and sales table
# -------------------------------
conn = sqlite3.connect("sales_data.db")
cursor = conn.cursor()

# Create table (if not exists)
cursor.execute("""
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product TEXT,
    quantity INTEGER,
    price REAL
)
""")

# Sample data
sample_data = [
    ("Apples", 10, 2.5),
    ("Apples", 5, 2.5),
    ("Bananas", 8, 1.2),
    ("Bananas", 12, 1.2),
    ("Cherries", 3, 5.0),
    ("Cherries", 6, 5.0)
]

# Clear old data (optional)
cursor.execute("DELETE FROM sales")

# Insert data
cursor.executemany("INSERT INTO sales (product, quantity, price) VALUES (?, ?, ?)", sample_data)
conn.commit()

# -------------------------------
# 2. Run SQL query for summary
# -------------------------------
query = """
SELECT 
    product, 
    SUM(quantity) AS total_qty, 
    SUM(quantity * price) AS revenue
FROM sales
GROUP BY product
"""

df = pd.read_sql_query(query, conn)

# -------------------------------
# 3. Display results
# -------------------------------
print("=== Sales Summary ===")
print(df)

# -------------------------------
# 4. Plot simple bar chart
# -------------------------------
plt.figure(figsize=(6,4))
plt.bar(df['product'], df['revenue'], color='skyblue')
plt.title("Revenue by Product")
plt.xlabel("Product")
plt.ylabel("Revenue")
plt.tight_layout()

# Save chart
plt.savefig("sales_chart.png")
plt.show()

# Close connection
conn.close()
