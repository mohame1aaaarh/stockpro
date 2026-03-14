from flask import Flask, render_template
import sqlite3
from datetime import datetime
def get_db_connection():
    conn = sqlite3.connect('database/stockpro.db')
    conn.row_factory = sqlite3.Row  # للوصول للبيانات كمصفوفة
    return conn

stokpro = Flask(__name__)
@stokpro.route('/')
def dashboard():
    conn = get_db_connection()
    products_count = conn.execute('SELECT COUNT(*) FROM products').fetchone()[0]
    customers_count = conn.execute('SELECT COUNT(*) FROM customers').fetchone()[0]
    suppliers_count = conn.execute('SELECT COUNT(*) FROM suppliers').fetchone()[0]
    today_sales_count = conn.execute("SELECT COUNT(*) FROM sales WHERE strftime('%Y-%m-%d', sale_date) = date('now')").fetchone()[0] or 0
    recent_sales = conn.execute('''
            SELECT 
                s.id,
                s.sale_date,
                s.total_amount,
                c.name as customer_name
            FROM sales s
            JOIN customers c ON s.customer_id = c.id
            ORDER BY s.sale_date DESC
            LIMIT 5
        ''').fetchall()
    conn.close()
    data = {
            'total_products': products_count,
            'total_customers': customers_count,
            'total_suppliers': suppliers_count,
            'today_sales': today_sales_count,
            'recent_sales': recent_sales
        }
    return render_template('dashboard.html', **data)

@stokpro.route('/products')
def productPage():
    return 'hello from product page'

@stokpro.route('/products/add')
def productPageadd():
    return 'hello from product page add'

@stokpro.route('/products/edit/<id>')
def productPageedit(id):
    return f'hello from product page edit {id}'

@stokpro.route('/products/delete/<id>')
def productPagedelete(id):
    return f'hello from product page delete {id}'

if __name__ == '__main__':
    stokpro.run(debug=True, port=5666)
