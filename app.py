from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime

def get_db_connection():
    conn = sqlite3.connect('database/stockpro.db')
    conn.row_factory = sqlite3.Row
    return conn

stokpro = Flask(__name__)
stokpro.secret_key = 'stockpro-secret-2026'

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
    conn = get_db_connection()
    products = conn.execute('''
        SELECT 
            products.*,
            categories.name AS category_name
        FROM products
        JOIN categories ON products.category_id = categories.id
    ''').fetchall()
    conn.close()
    return render_template('products.html', products=products)


@stokpro.route('/products/add', methods=['GET'])
def productPageadd():
    conn = get_db_connection()
    categories = conn.execute('SELECT * FROM categories').fetchall()
    conn.close()
    return render_template('product_add.html', categories=categories)


@stokpro.route('/products/add', methods=['POST'])
def productPageaddSave():
    name           = request.form['name']
    category_id    = request.form['category_id']
    price_for_sale = request.form['price_for_sale']
    price_for_buy  = request.form['price_for_buy']
    unit           = request.form['unit']
    min_quantity   = request.form['min_quantity']
    photo_url      = request.form['photo_url']

    conn = get_db_connection()
    conn.execute('''
        INSERT INTO products (name, category_id, price_for_sale, price_for_buy, unit, min_quantity, photo_url)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (name, category_id, price_for_sale, price_for_buy, unit, min_quantity, photo_url))
    conn.commit()
    conn.close()

    flash('تم إضافة المنتج بنجاح', 'success')
    return redirect(url_for('productPage'))

@stokpro.route('/products/edit/<int:id>', methods=['GET'])
def productPageedit(id):
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id = ?', (id,)).fetchone()
    categories = conn.execute('SELECT * FROM categories').fetchall()
    conn.close()
    return render_template('product_edit.html', product=product, categories=categories)


@stokpro.route('/products/edit/<int:id>', methods=['POST'])
def productPageeditSave(id):
    name           = request.form['name']
    category_id    = request.form['category_id']
    price_for_sale = request.form['price_for_sale']
    price_for_buy  = request.form['price_for_buy']
    unit           = request.form['unit']
    min_quantity   = request.form['min_quantity']

    conn = get_db_connection()
    conn.execute('''
        UPDATE products
        SET name=?, category_id=?, price_for_sale=?, price_for_buy=?, unit=?, min_quantity=?
        WHERE id=?
    ''', (name, category_id, price_for_sale, price_for_buy, unit, min_quantity, id))
    conn.commit()
    conn.close()

    flash('تم تعديل المنتج بنجاح', 'success')
    return redirect(url_for('productPage'))


@stokpro.route('/products/delete/<int:id>', methods=['POST'])
def productPagedelete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM products WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('تم حذف المنتج بنجاح', 'success')
    return redirect(url_for('productPage'))
@stokpro.route('/categories')
def categoriesPage():
    conn = get_db_connection()
    categories = conn.execute('SELECT * FROM categories').fetchall()
    conn.close()
    return render_template('categories.html', categories=categories)


@stokpro.route('/categories/add', methods=['POST'])
def categoriesPageadd():
    name = request.form['name']
    conn = get_db_connection()
    conn.execute('INSERT INTO categories (name) VALUES (?)', (name,))
    conn.commit()
    conn.close()
    flash('تم إضافة الفئة بنجاح', 'success')
    return redirect(url_for('categoriesPage'))


@stokpro.route('/categories/delete/<int:id>', methods=['POST'])
def categoriesPagedelete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM categories WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('تم حذف الفئة بنجاح', 'success')
    return redirect(url_for('categoriesPage'))

@stokpro.route('/suppliers')
def suppliersPage():
    conn = get_db_connection()
    suppliers = conn.execute('SELECT * FROM suppliers').fetchall()
    conn.commit()
    conn.close()
    return render_template('suppliers.html', suppliers=suppliers)


@stokpro.route('/suppliers/add', methods=['POST'])
def suppliersPageadd():
    name    = request.form['name']
    phone   = request.form['phone']
    email   = request.form['email']
    address = request.form['address']
    
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO suppliers (name, phone_number, email, address) VALUES (?, ?, ?, ?)',
        (name, phone, email, address)
    )

    conn.commit() 
    conn.close()
    
    flash('تم إضافة المورد بنجاح', 'success')

    return redirect(url_for('suppliersPage'))


@stokpro.route('/suppliers/delete/<int:id>', methods=['POST'])
def suppliersPagedelete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM suppliers WHERE id = ?', (id,))

    conn.commit()
    conn.close()
    
    flash('تم حذف المورد بنجاح', 'success')
    return redirect(url_for('suppliersPage'))

@stokpro.route('/customers')
def customersPage():
    conn = get_db_connection()
    customers = conn.execute('SELECT * FROM customers').fetchall()
    conn.close()
    return render_template('customers.html', customers=customers)


@stokpro.route('/customers/add', methods=['POST'])
def customersPageadd():
    name    = request.form['name']
    phone   = request.form['phone']
    email   = request.form['email']
    address = request.form['address']

    conn = get_db_connection()
    conn.execute(
        'INSERT INTO customers (name, phone_number, email, address) VALUES (?, ?, ?, ?)',
        (name, phone, email, address)
    )
    conn.commit()
    conn.close()

    flash('تم إضافة العميل بنجاح', 'success')
    return redirect(url_for('customersPage'))


@stokpro.route('/customers/delete/<int:id>', methods=['POST'])
def customersPagedelete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM customers WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    flash('تم حذف العميل بنجاح', 'success')
    return redirect(url_for('customersPage'))
@stokpro.route('/purchases')
def purchasesPage():
    conn = get_db_connection()

    purchases = conn.execute('''
        SELECT 
            purchases.*,
            products.name  AS product_name,
            suppliers.name AS supplier_name
        FROM purchases
        JOIN products  ON purchases.product_id  = products.id
        JOIN suppliers ON purchases.supplier_id = suppliers.id
    ''').fetchall()

    products  = conn.execute('SELECT * FROM products').fetchall()
    suppliers = conn.execute('SELECT * FROM suppliers').fetchall()

    conn.close()

    return render_template(
        'purchases.html',
        purchases=purchases,
        products=products,
        suppliers=suppliers
    )
    
@stokpro.route('/purchases/add', methods=['POST'])
def purchasesPageadd():
    product_id  = request.form['product_id']
    supplier_id = request.form['supplier_id']
    quantity    = int(request.form['quantity'])

    conn = get_db_connection()

    product = conn.execute(
        'SELECT price_for_buy FROM products WHERE id = ?',
        (product_id,)
    ).fetchone()

    total_cost = product['price_for_buy'] * quantity

    conn.execute(
        'INSERT INTO purchases (product_id, supplier_id, quantity, total_cost) VALUES (?, ?, ?, ?)',
        (product_id, supplier_id, quantity, total_cost)
    )

    conn.execute(
        'UPDATE products SET quantity_by_unit = quantity_by_unit + ? WHERE id = ?',
        (quantity, product_id)
    )

    conn.commit()
    conn.close()

    return redirect(url_for('purchasesPage'))

if __name__ == '__main__':
    stokpro.run(debug=True, port=5666)


