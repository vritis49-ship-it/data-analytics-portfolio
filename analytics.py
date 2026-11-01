import sqlite3
import matplotlib.pyplot as plt

def run_analytics():
    # 1. Connect to database and build schema
    conn = sqlite3.connect('tech_store.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sales (
        transaction_id INTEGER PRIMARY KEY,
        product_name TEXT,
        category TEXT,
        price REAL,
        quantity_sold INTEGER
    )
    ''')

    # 2. Load dataset
    dataset = [
        (1, 'Mechanical Keyboard', 'Hardware', 120.00, 15),
        (2, 'Wireless Mouse', 'Hardware', 45.50, 30),
        (3, 'Cloud Storage 1TB', 'Software', 99.99, 50),
        (4, 'IDE Pro License', 'Software', 199.00, 12),
        (5, '4K Monitor', 'Hardware', 350.00, 8)
    ]
    
    cursor.execute('DELETE FROM sales')
    cursor.executemany('INSERT INTO sales VALUES (?, ?, ?, ?, ?)', dataset)
    conn.commit()

    # 3. Execute SQL query
    cursor.execute('''
        SELECT 
            category, 
            SUM(price * quantity_sold) as total_revenue
        FROM sales
        GROUP BY category
        ORDER BY total_revenue DESC
    ''')

    results = cursor.fetchall()
    conn.close()

    # 4. Prepare data for visualization
    categories = [row[0] for row in results]
    revenues = [row[1] for row in results]

    # 5. Generate and save the Bar Chart
    plt.figure(figsize=(8, 5))
    bars = plt.bar(categories, revenues, color=['#2c3e50', '#b3c7f9'])
    
    # Add title and labels
    plt.title('Tech Store Revenue by Category', fontsize=14, fontweight='bold')
    plt.xlabel('Product Category', fontsize=12)
    plt.ylabel('Total Revenue ($)', fontsize=12)
    
    # Add exact numbers on top of the bars
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 100, f'${yval:,.2f}', ha='center', fontsize=10)

    # Save the chart as an image file instead of just showing it
    plt.tight_layout()
    plt.savefig('revenue_chart.png')
    print("✅ Analytics complete! Chart saved as 'revenue_chart.png'")

if __name__ == '__main__':
    run_analytics()