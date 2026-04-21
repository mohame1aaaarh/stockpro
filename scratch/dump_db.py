import sqlite3
import json

conn = sqlite3.connect('database/stockpro.db')
conn.row_factory = sqlite3.Row

data = {}
tables = ['sales', 'sale_items', 'purchases', 'purchase_items']
for table in tables:
    rows = conn.execute(f"SELECT * FROM {table}").fetchall()
    data[table] = [dict(row) for row in rows]

print(json.dumps(data, indent=2))
conn.close()
