import sqlite3
import sys
sys.stdout.reconfigure(encoding='utf-8')

def init_db():
    conn = sqlite3.connect("database/stockpro.db")
    
    with open("database/database.sql", "r", encoding="utf-8") as f:
        sql = f.read()
    
    conn.executescript(sql)
    conn.commit()
    conn.close()
    print("✅ Database created successfully!")

init_db()