import sqlite3

def run_analytics():
    # 1. Connect to a local SQLite database (creates the file if it doesn't exist)
    conn = sqlite3.connect('tech_store.db')
    cursor = conn.cursor()

    # 2. Build the schema using SQL
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sales (
        transaction_id INTEGER PRIMARY KEY,
        product_name TEXT,
        category TEXT,
        price REAL,
        quantity_sold INTEGER
    )
    ''')

    # 3. Load sample dataset
    dataset = [
        (1, 'Mechanical Keyboard', 'Hardware', 120.00, 15),
        (2, 'Wireless Mouse', 'Hardware', 45.50, 30),
        (3, 'Cloud Storage 1TB', 'Software', 99.99, 50),
        (4, 'IDE Pro License', 'Software', 199.00, 12),
        (5, '4K Monitor', 'Hardware', 350.00, 8)
    ]
    
    # Clear old data to prevent duplicates on multiple runs, then insert new data
    cursor.execute('DELETE FROM sales')
    cursor.executemany('INSERT INTO sales VALUES (?, ?, ?, ?, ?)', dataset)
    conn.commit()

    # 4. Execute an analytical SQL query
    print("📊 --- Tech Store Revenue Analytics --- 📊\n")
    
    cursor.execute('''
        SELECT 
            category, 
            SUM(price * quantity_sold) as total_revenue, 
            SUM(quantity_sold) as total_items
        FROM sales
        GROUP BY category
        ORDER BY total_revenue DESC
    ''')

    # 5. Process and display the results
    results = cursor.fetchall()
    for row in results:
        category, revenue, items = row
        print(f"Category: {category}")
        print(f"  ↳ Total Revenue: ${revenue:,.2f}")
        print(f"  ↳ Items Sold: {items}\n")

    conn.close()

if __name__ == '__main__':
    run_analytics()