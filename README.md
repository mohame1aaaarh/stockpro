# 📋 مهام الفريق المتبقية — StockPro

> هذا الملف موجه لأعضاء الفريق لإكمال المشروع بعد ما تم إنجازه.
> اتبع المهام بالترتيب لأن كل مرحلة تعتمد على السابقة.

---

## ✅ اللي اتعمل بالفعل

| الصفحة | الحالة |
|--------|--------|
| المنتجات (عرض، إضافة، تعديل، حذف) | ✅ مكتمل |
| الفئات (عرض، إضافة، حذف) | ✅ مكتمل |

---

## 🗂️ هيكل الملفات الحالي

```
stockpro/
├── app.py                          ← الروتات (Flask)
├── database/
│   └── stockpro.db                 ← قاعدة البيانات
├── static/
│   ├── style.css
│   └── images/products/            ← صور المنتجات
└── templates/
    ├── base.html                   ← القالب الأساسي (sidebar + navbar)
    ├── dashboard.html
    ├── products.html
    ├── product_add.html
    ├── product_edit.html
    └── categories.html
```

---

## 🔴 مهمة ١ — صفحة الموردين (Suppliers)

### جدول الداتابيز

```sql
CREATE TABLE IF NOT EXISTS suppliers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT,
    email TEXT,
    address TEXT
);
```

### المطلوب في `app.py`

أضف الروتات دي:

```python
# ① عرض كل الموردين
@stokpro.route('/suppliers')
def suppliersPage():
    conn = get_db_connection()
    suppliers = conn.execute('SELECT * FROM suppliers').fetchall()
    conn.close()
    return render_template('suppliers.html', suppliers=suppliers)

# ② إضافة مورد جديد
@stokpro.route('/suppliers/add', methods=['POST'])
def suppliersPageadd():
    name    = request.form['name']
    phone   = request.form['phone']
    email   = request.form['email']
    address = request.form['address']
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO suppliers (name, phone, email, address) VALUES (?, ?, ?, ?)',
        (name, phone, email, address)
    )
    conn.commit()
    conn.close()
    flash('تم إضافة المورد بنجاح', 'success')
    return redirect(url_for('suppliersPage'))

# ③ حذف مورد
@stokpro.route('/suppliers/delete/<int:id>', methods=['POST'])
def suppliersPagedelete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM suppliers WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('تم حذف المورد بنجاح', 'success')
    return redirect(url_for('suppliersPage'))
```

### المطلوب في `base.html`

في الـ sidebar ابحث عن اللينك المعطل للموردين وغيره لـ:

```html
<a href="{{ url_for('suppliersPage') }}"
   class="sidebar-link {% if request.endpoint == 'suppliersPage' %}active{% endif %}">
    <i class="fas fa-truck"></i>
    <span>الموردون</span>
</a>
```

### المطلوب إنشاؤه: `suppliers.html`

صفحة فيها:
- **جدول** يعرض: الاسم، التليفون، الإيميل، العنوان، وأزرار الحذف
- **فورم إضافة** في نفس الصفحة أو في صفحة منفصلة

> 💡 نفس فكرة `categories.html` بالظبط بس بأعمدة أكتر

---

## 🟠 مهمة ٢ — صفحة العملاء (Customers)

### جدول الداتابيز

```sql
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT,
    email TEXT,
    address TEXT
);
```

### المطلوب في `app.py`

نفس نفس روتات الموردين بالظبط، بس غير كلمة `suppliers` بـ `customers`:

```python
@stokpro.route('/customers')
def customersPage(): ...

@stokpro.route('/customers/add', methods=['POST'])
def customersPageadd(): ...

@stokpro.route('/customers/delete/<int:id>', methods=['POST'])
def customersPagedelete(id): ...
```

### المطلوب في `base.html`

```html
<a href="{{ url_for('customersPage') }}"
   class="sidebar-link {% if request.endpoint == 'customersPage' %}active{% endif %}">
    <i class="fas fa-users"></i>
    <span>العملاء</span>
</a>
```

### المطلوب إنشاؤه: `customers.html`

نفس تصميم `suppliers.html`

---

## 🟡 مهمة ٣ — صفحة المبيعات (Sales)

> ⚠️ **مهمة:** لازم تخلص مهمة ١ و٢ قبل دي عشان محتاجين العملاء والمنتجات.

### جدول الداتابيز

```sql
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    customer_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    total_amount REAL NOT NULL,
    sale_date TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);
```

### المطلوب في `app.py`

```python
# ① عرض المبيعات مع JOIN
@stokpro.route('/sales')
def salesPage():
    conn = get_db_connection()
    sales = conn.execute('''
        SELECT 
            sales.*,
            products.name AS product_name,
            customers.name AS customer_name
        FROM sales
        JOIN products  ON sales.product_id  = products.id
        JOIN customers ON sales.customer_id = customers.id
        ORDER BY sales.sale_date DESC
    ''').fetchall()
    products  = conn.execute('SELECT * FROM products').fetchall()
    customers = conn.execute('SELECT * FROM customers').fetchall()
    conn.close()
    return render_template('sales.html', sales=sales, products=products, customers=customers)

# ② تسجيل بيعة جديدة
@stokpro.route('/sales/add', methods=['POST'])
def salesPageadd():
    product_id  = request.form['product_id']
    customer_id = request.form['customer_id']
    quantity    = int(request.form['quantity'])

    conn = get_db_connection()

    # جيب سعر المنتج عشان تحسب الإجمالي
    product = conn.execute('SELECT price_for_sale FROM products WHERE id = ?', (product_id,)).fetchone()
    total_amount = product['price_for_sale'] * quantity

    # سجل البيعة
    conn.execute(
        'INSERT INTO sales (product_id, customer_id, quantity, total_amount) VALUES (?, ?, ?, ?)',
        (product_id, customer_id, quantity, total_amount)
    )

    # ⚠️ انقص الكمية من المخزون
    conn.execute(
        'UPDATE products SET quantity_by_unit = quantity_by_unit - ? WHERE id = ?',
        (quantity, product_id)
    )

    conn.commit()
    conn.close()
    flash('تم تسجيل البيعة بنجاح', 'success')
    return redirect(url_for('salesPage'))
```

### المطلوب في `base.html`

```html
<a href="{{ url_for('salesPage') }}"
   class="sidebar-link {% if request.endpoint == 'salesPage' %}active{% endif %}">
    <i class="fas fa-shopping-cart"></i>
    <span>المبيعات</span>
</a>
```

### المطلوب إنشاؤه: `sales.html`

صفحة فيها:
- **جدول** يعرض: اسم المنتج، اسم العميل، الكمية، الإجمالي، التاريخ
- **فورم إضافة بيعة** فيه:
  - `<select>` لاختيار المنتج (من `products`)
  - `<select>` لاختيار العميل (من `customers`)
  - `<input>` للكمية

---

## 🟢 مهمة ٤ — صفحة المشتريات (Purchases)

> ⚠️ **مهمة:** لازم تخلص مهمة ١ قبل دي عشان محتاجين الموردين.

### جدول الداتابيز

```sql
CREATE TABLE IF NOT EXISTS purchases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    supplier_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    total_cost REAL NOT NULL,
    purchase_date TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
);
```

### المطلوب في `app.py`

```python
# ① عرض المشتريات
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
        ORDER BY purchases.purchase_date DESC
    ''').fetchall()
    products  = conn.execute('SELECT * FROM products').fetchall()
    suppliers = conn.execute('SELECT * FROM suppliers').fetchall()
    conn.close()
    return render_template('purchases.html', purchases=purchases, products=products, suppliers=suppliers)

# ② تسجيل مشترى جديد
@stokpro.route('/purchases/add', methods=['POST'])
def purchasesPageadd():
    product_id  = request.form['product_id']
    supplier_id = request.form['supplier_id']
    quantity    = int(request.form['quantity'])

    conn = get_db_connection()

    # جيب سعر الشراء عشان تحسب التكلفة
    product = conn.execute('SELECT price_for_buy FROM products WHERE id = ?', (product_id,)).fetchone()
    total_cost = product['price_for_buy'] * quantity

    # سجل الشراء
    conn.execute(
        'INSERT INTO purchases (product_id, supplier_id, quantity, total_cost) VALUES (?, ?, ?, ?)',
        (product_id, supplier_id, quantity, total_cost)
    )

    # ⚠️ زود الكمية في المخزون
    conn.execute(
        'UPDATE products SET quantity_by_unit = quantity_by_unit + ? WHERE id = ?',
        (quantity, product_id)
    )

    conn.commit()
    conn.close()
    flash('تم تسجيل المشترى بنجاح', 'success')
    return redirect(url_for('purchasesPage'))
```

### المطلوب في `base.html`

```html
<a href="{{ url_for('purchasesPage') }}"
   class="sidebar-link {% if request.endpoint == 'purchasesPage' %}active{% endif %}">
    <i class="fas fa-file-invoice"></i>
    <span>المشتريات</span>
</a>
```

### المطلوب إنشاؤه: `purchases.html`

نفس فكرة `sales.html` بالظبط بس:
- بدل العميل → المورد
- بدل سعر البيع → سعر الشراء

---

## 🔵 مهمة ٥ — صفحة التقارير (Reports)

> ⚠️ **مهمة:** لازم تخلص كل المهام السابقة قبل دي.

### المطلوب في `app.py`

```python
@stokpro.route('/reports')
def reportsPage():
    conn = get_db_connection()

    # أكتر 5 منتجات مبيعاً
    top_products = conn.execute('''
        SELECT 
            products.name,
            SUM(sales.quantity) AS total_sold,
            SUM(sales.total_amount) AS total_revenue
        FROM sales
        JOIN products ON sales.product_id = products.id
        GROUP BY products.id
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
    total_cost  = conn.execute('SELECT SUM(total_cost) FROM purchases').fetchone()[0] or 0
    total_profit = total_sales - total_cost

    conn.close()
    return render_template('reports.html',
        top_products=top_products,
        low_stock=low_stock,
        total_sales=total_sales,
        total_cost=total_cost,
        total_profit=total_profit
    )
```

### المطلوب في `base.html`

```html
<a href="{{ url_for('reportsPage') }}"
   class="sidebar-link {% if request.endpoint == 'reportsPage' %}active{% endif %}">
    <i class="fas fa-chart-bar"></i>
    <span>التقارير</span>
</a>
```

### المطلوب إنشاؤه: `reports.html`

صفحة فيها 3 أجزاء:

**١. كروت الإجمالي:**
- إجمالي المبيعات (`total_sales`)
- إجمالي التكلفة (`total_cost`)
- صافي الربح (`total_profit`)

**٢. جدول أكتر المنتجات مبيعاً:**
- الاسم، الكمية المباعة، الإيراد

**٣. جدول المنتجات الناقصة:**
- الاسم، الكمية الحالية، الحد الأدنى
- لون أحمر لو الكمية وصلت للحد الأدنى

---

## 🧪 اختبار المشروع قبل التسليم

بعد إنهاء كل المهام، تأكد من:

- [ ] إضافة مورد جديد وحذفه
- [ ] إضافة عميل جديد وحذفه
- [ ] تسجيل بيعة والتأكد إن الكمية نقصت
- [ ] تسجيل مشترى والتأكد إن الكمية زادت
- [ ] صفحة التقارير بتعرض بيانات صح
- [ ] المنتجات الناقصة بتظهر في التقارير

---

## 💡 ملاحظات مهمة

- **لا تغير الكمية يدوياً** — بتتغير تلقائياً من المبيعات والمشتريات فقط
- **كل روت POST** لازم يكون فيه `conn.commit()` قبل `conn.close()`
- **الـ flash messages** شغالة تلقائياً في `base.html` مش محتاج تضيف حاجة
- **اسم الـ endpoint** في `url_for` لازم يطابق اسم الدالة بالظبط

---

*StockPro — مشروع قواعد البيانات · ترم الربيع 2026*