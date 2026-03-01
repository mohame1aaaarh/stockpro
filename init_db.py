import sqlite3
import sys
from config import DATABASE_URL
sys.stdout.reconfigure(encoding='utf-8')

def init_db():
    conn = sqlite3.connect(DATABASE_URL)
    
    with open(DATABASE_URL.replace(".db", ".sql"), "r", encoding="utf-8") as f:
        sql = f.read()
    
    conn.executescript(sql)
    conn.commit()
    conn.close()
    print("✅ Database created successfully!")

init_db()