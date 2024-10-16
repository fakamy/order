import sqlite3
from datetime import datetime


def init_db():
    conn = sqlite3.connect('coffee_orders.db')
    c = conn.cursor()

    # Check if the completion_time column exists
    # c.execute("PRAGMA table_info(orders)")
    # columns = [column[1] for column in c.fetchall()]

    # if 'completion_time' not in columns:
    #     # Add the completion_time column if it doesn't exist
    #     c.execute("ALTER TABLE orders ADD COLUMN completion_time TEXT")

    # Create the table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS orders
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  item TEXT,
                  name TEXT,
                  phone TEXT,
                  location TEXT,
                  status TEXT,
                  order_date TEXT,
                  completion_time TEXT)''')
    conn.commit()
    conn.close()


def add_order(item, name, phone, location):
    conn = sqlite3.connect('coffee_orders.db')
    c = conn.cursor()
    order_date = datetime.now().isoformat()
    c.execute(
        "INSERT INTO orders (item, name, phone, location, status, order_date) VALUES (?, ?, ?, ?, ?, ?)",
        (item, name, phone, location, 'pending', order_date))
    order_id = c.lastrowid
    conn.commit()
    conn.close()
    return order_id


def get_orders(include_completed=True):
    conn = sqlite3.connect('coffee_orders.db')
    c = conn.cursor()
    if include_completed:
        c.execute("SELECT * FROM orders ORDER BY order_date DESC")
    else:
        c.execute(
            "SELECT * FROM orders WHERE status='pending' ORDER BY order_date DESC"
        )

    # Fetch column names
    column_names = [description[0] for description in c.description]

    orders = []
    for row in c.fetchall():
        order = {}
        for i, column in enumerate(column_names):
            if i < len(row):
                order[column] = row[i]
            else:
                order[column] = None
        orders.append(order)

    conn.close()
    return orders


def update_order_status(order_id, status, completion_time=None):
    conn = sqlite3.connect('coffee_orders.db')
    c = conn.cursor()
    if completion_time:
        c.execute("UPDATE orders SET status=?, completion_time=? WHERE id=?",
                  (status, completion_time, order_id))
    else:
        c.execute("UPDATE orders SET status=? WHERE id=?", (status, order_id))
    conn.commit()
    conn.close()


def get_order(order_id):
    conn = sqlite3.connect('coffee_orders.db')
    c = conn.cursor()
    c.execute("SELECT * FROM orders WHERE id=?", (order_id, ))
    order = c.fetchone()
    conn.close()
    if order:
        return {
            "id": order[0],
            "item": order[1],
            "name": order[2],
            "phone": order[3],
            "location": order[4],
            "status": order[5],
            "order_date": order[6],
            "completion_time": order[7]
        }
    return None
