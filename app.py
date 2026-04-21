from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime

def get_db_connection():
    conn = sqlite3.connect('database/stockpro.db')
    conn.row_factory = sqlite3.Row
    return conn

stockpro = Flask(__name__)
stockpro.secret_key = 'stockpro-secret-2026'

@stockpro.route('/')
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
        LEFT JOIN customers c ON s.customer_id = c.id
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


@stockpro.route('/products')
def product_page():
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


@stockpro.route('/products/add', methods=['GET'])
def product_add():
    conn = get_db_connection()
    categories = conn.execute('SELECT * FROM categories').fetchall()
    conn.close()
    return render_template('product_add.html', categories=categories)


@stockpro.route('/products/add', methods=['POST'])
def product_add_save():
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
    return redirect(url_for('product_page'))

@stockpro.route('/products/edit/<int:id>', methods=['GET'])
def product_edit(id):
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id = ?', (id,)).fetchone()
    categories = conn.execute('SELECT * FROM categories').fetchall()
    conn.close()
    return render_template('product_edit.html', product=product, categories=categories)


@stockpro.route('/products/edit/<int:id>', methods=['POST'])
def product_edit_save(id):
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
    return redirect(url_for('product_page'))


@stockpro.route('/products/delete/<int:id>', methods=['POST'])
def product_delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM products WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('تم حذف المنتج بنجاح', 'success')
    return redirect(url_for('product_page'))
@stockpro.route('/categories')
def categories_page():
    conn = get_db_connection()
    categories = conn.execute('SELECT * FROM categories').fetchall()
    conn.close()
    return render_template('categories.html', categories=categories)


@stockpro.route('/categories/add', methods=['POST'])
def categories_add():
    name = request.form['name']
    conn = get_db_connection()
    conn.execute('INSERT INTO categories (name) VALUES (?)', (name,))
    conn.commit()
    conn.close()
    flash('تم إضافة الفئة بنجاح', 'success')
    return redirect(url_for('categories_page'))


@stockpro.route('/categories/delete/<int:id>', methods=['POST'])
def categories_delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM categories WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('تم حذف الفئة بنجاح', 'success')
    return redirect(url_for('categories_page'))

@stockpro.route('/suppliers')
def suppliers_page():
    conn = get_db_connection()
    suppliers = conn.execute('SELECT * FROM suppliers').fetchall()
    conn.close()
    return render_template('suppliers.html', suppliers=suppliers)


@stockpro.route('/suppliers/add', methods=['POST'])
def suppliers_add():
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

    return redirect(url_for('suppliers_page'))


@stockpro.route('/suppliers/delete/<int:id>', methods=['POST'])
def suppliers_delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM suppliers WHERE id = ?', (id,))

    conn.commit()
    conn.close()
    
    flash('تم حذف المورد بنجاح', 'success')
    return redirect(url_for('suppliers_page'))

@stockpro.route('/customers')
def customers_page():
    conn = get_db_connection()
    customers = conn.execute('SELECT * FROM customers').fetchall()
    conn.close()
    return render_template('customers.html', customers=customers)


@stockpro.route('/customers/add', methods=['POST'])
def customers_add():
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
    return redirect(url_for('customers_page'))


@stockpro.route('/customers/delete/<int:id>', methods=['POST'])
def customers_delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM customers WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    flash('تم حذف العميل بنجاح', 'success')
    return redirect(url_for('customers_page'))

@stockpro.route('/reports')
def reports_page():
    conn = get_db_connection()

    # أكتر 5 منتجات مبيعاً
    top_products = conn.execute('''
        SELECT 
            p.name,
            SUM(si.quantity) AS total_sold,
            SUM(si.quantity * si.price) AS total_revenue
        FROM sale_items si
        JOIN products p ON si.product_id = p.id
        GROUP BY p.id
        ORDER BY total_sold DESC
        LIMIT 5
    ''').fetchall()

    # المنتجات اللي وصلت للحد الأدنى
    low_stock = conn.execute('''
        SELECT name, quantity_by_unit, min_quantity
        FROM products
        WHERE quantity_by_unit <= min_quantity
    ''').fetchall()

    # إجمالي الأرباح (مبيعات - مشتريات)
    total_sales = conn.execute('SELECT SUM(total_amount) FROM sales').fetchone()[0] or 0
    total_cost  = conn.execute('SELECT SUM(total_amount) FROM purchases').fetchone()[0] or 0
    total_profit = total_sales - total_cost

    conn.close()
    return render_template('reports.html',
        top_products=top_products,
        low_stock=low_stock,
        total_sales=total_sales,
        total_cost=total_cost,
        total_profit=total_profit
    )

@stockpro.route('/sales')
def sales_page():
    conn = get_db_connection()
    sales = conn.execute('''
        SELECT 
            s.id,
            s.sale_date,
            s.total_amount,
            p.name AS product_name,
            c.name AS customer_name,
            si.quantity
        FROM sales s
        LEFT JOIN customers c ON s.customer_id = c.id
        LEFT JOIN sale_items si ON s.id = si.sale_id
        LEFT JOIN products p ON si.product_id = p.id
        ORDER BY s.sale_date DESC
    ''').fetchall()
    products  = conn.execute('SELECT * FROM products').fetchall()
    customers = conn.execute('SELECT * FROM customers').fetchall()
    conn.close()
    return render_template('sales.html', sales=sales, products=products, customers=customers)

@stockpro.route('/sales/add', methods=['POST'])
def sales_add():
    product_id  = request.form['product_id']
    customer_id = request.form['customer_id']
    quantity    = int(request.form['quantity'])

    conn = get_db_connection()

    # جيب سعر المنتج والكمية المتوفرة
    product = conn.execute('SELECT price_for_sale, quantity_by_unit FROM products WHERE id = ?', (product_id,)).fetchone()
    
    if not product:
        conn.close()
        flash('فشل: المنتج غير موجود', 'error')
        return redirect(url_for('sales_page'))

    if product['quantity_by_unit'] < quantity:
        conn.close()
        flash(f'فشل: الكمية المتوفرة غير كافية (المتاح: {product["quantity_by_unit"]})', 'error')
        return redirect(url_for('sales_page'))

    price = product['price_for_sale']
    total_amount = price * quantity
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # سجل البيعة في جدول sales
    cur = conn.execute(
        'INSERT INTO sales (customer_id, sale_date, total_amount, info) VALUES (?, ?, ?, ?)',
        (customer_id, now, total_amount, '')
    )
    sale_id = cur.lastrowid

    # سجل تفاصيل البيعة في جدول sale_items
    conn.execute(
        'INSERT INTO sale_items (sale_id, product_id, quantity, price) VALUES (?, ?, ?, ?)',
        (sale_id, product_id, quantity, price)
    )

    # انقص الكمية من المخزون
    conn.execute(
        'UPDATE products SET quantity_by_unit = quantity_by_unit - ? WHERE id = ?',
        (quantity, product_id)
    )

    conn.commit()
    conn.close()
    flash('تم تسجيل البيعة بنجاح', 'success')
    return redirect(url_for('sales_page'))


@stockpro.route('/purchases')
def purchases_page():
    conn = get_db_connection()
    purchases = conn.execute('''
        SELECT 
            p.id,
            p.purchase_date,
            p.total_amount,
            prod.name AS product_name,
            s.name AS supplier_name,
            pi.quantity
        FROM purchases p
        LEFT JOIN suppliers s ON p.supplier_id = s.id
        LEFT JOIN purchase_items pi ON p.id = pi.purchase_id
        LEFT JOIN products prod ON pi.product_id = prod.id
        ORDER BY p.purchase_date DESC
    ''').fetchall()
    products  = conn.execute('SELECT * FROM products').fetchall()
    suppliers = conn.execute('SELECT * FROM suppliers').fetchall()
    conn.close()
    return render_template('purchases.html', purchases=purchases, products=products, suppliers=suppliers)


@stockpro.route('/purchases/add', methods=['POST'])
def purchases_add():
    product_id  = request.form['product_id']
    supplier_id = request.form['supplier_id']
    quantity    = int(request.form['quantity'])

    conn = get_db_connection()

    product = conn.execute('SELECT price_for_buy FROM products WHERE id = ?', (product_id,)).fetchone()
    
    if not product:
        conn.close()
        flash('فشل: المنتج غير موجود', 'error')
        return redirect(url_for('purchases_page'))

    price = product['price_for_buy']
    total_amount = price * quantity
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    cur = conn.execute(
        'INSERT INTO purchases (supplier_id, purchase_date, total_amount, info) VALUES (?, ?, ?, ?)',
        (supplier_id, now, total_amount, '')
    )
    purchase_id = cur.lastrowid

    conn.execute(
        'INSERT INTO purchase_items (purchase_id, product_id, quantity, price) VALUES (?, ?, ?, ?)',
        (purchase_id, product_id, quantity, price)
    )

    # زود الكمية في المخزون
    conn.execute(
        'UPDATE products SET quantity_by_unit = quantity_by_unit + ? WHERE id = ?',
        (quantity, product_id)
    )

    conn.commit()
    conn.close()
    flash('تم تسجيل المشتريات بنجاح', 'success')
    return redirect(url_for('purchases_page'))


@stockpro.route('/sales/invoice/<int:id>')
def sales_invoice(id):
    conn = get_db_connection()
    sale = conn.execute('''
        SELECT s.*, c.name as customer_name, c.phone_number, c.address
        FROM sales s
        LEFT JOIN customers c ON s.customer_id = c.id
        WHERE s.id = ?
    ''', (id,)).fetchone()
    
    items = conn.execute('''
        SELECT si.*, p.name as product_name, p.unit
        FROM sale_items si
        LEFT JOIN products p ON si.product_id = p.id
        WHERE si.sale_id = ?
    ''', (id,)).fetchall()
    conn.close()
    
    if not sale:
        flash('الفاتورة غير موجودة', 'error')
        return redirect(url_for('sales_page'))
        
    return render_template('invoice.html', sale=sale, items=items)


@stockpro.route('/purchases/invoice/<int:id>')
def purchases_invoice(id):
    conn = get_db_connection()
    purchase = conn.execute('''
        SELECT p.*, s.name as supplier_name, s.phone_number, s.address
        FROM purchases p
        LEFT JOIN suppliers s ON p.supplier_id = s.id
        WHERE p.id = ?
    ''', (id,)).fetchone()
    
    items = conn.execute('''
        SELECT pi.*, prod.name as product_name, prod.unit
        FROM purchase_items pi
        LEFT JOIN products prod ON pi.product_id = prod.id
        WHERE pi.purchase_id = ?
    ''', (id,)).fetchall()
    conn.close()
    
    if not purchase:
        flash('الفاتورة غير موجودة', 'error')
        return redirect(url_for('purchases_page'))
        
    return render_template('invoice_purchase.html', purchase=purchase, items=items)

if __name__ == '__main__':
    stockpro.run(debug=True, port=5666)