import sqlite3
from datetime import datetime

conn = sqlite3.connect("database/stockpro.db")
cursor = conn.cursor()

# -------------------
# إضافة أقسام
# -------------------
cursor.execute("INSERT OR IGNORE INTO categories (name) VALUES ('الكترونيات')")
cursor.execute("INSERT OR IGNORE INTO categories (name) VALUES ('اثاث')")
cursor.execute("INSERT OR IGNORE INTO categories (name) VALUES ('مستلزمات مكتب')")

# -------------------
# إضافة موردين
# -------------------
cursor.execute("INSERT INTO suppliers (name, phone_number, email, address) VALUES ('شركة التقنية', '01000000000', 'tech@mail.com', 'القاهرة')")
cursor.execute("INSERT INTO suppliers (name, phone_number, email, address) VALUES ('شركة النور', '01100000000', 'noor@mail.com', 'الجيزة')")
cursor.execute("INSERT INTO suppliers (name, phone_number, email, address) VALUES ('شركة المستقبل', '01200000000', 'future@mail.com', 'الاسكندرية')")

# -------------------
# إضافة عملاء
# -------------------
cursor.execute("INSERT INTO customers (name, phone_number, email, address) VALUES ('محمد', '01011111111', 'mohamed@mail.com', 'المنصورة')")
cursor.execute("INSERT INTO customers (name, phone_number, email, address) VALUES ('احمد', '01022222222', 'ahmed@mail.com', 'القاهرة')")
cursor.execute("INSERT INTO customers (name, phone_number, email, address) VALUES ('علي', '01033333333', 'ali@mail.com', 'دمياط')")

# -------------------
# إضافة منتجات
# -------------------
cursor.execute("""
INSERT INTO products 
(name, category_id, price_for_sale, price_for_buy, photo_url, unit, quantity_by_unit, min_quantity)
VALUES ('لابتوب',1,15000,12000,'laptop.jpg','قطعة',10,2)
""")

cursor.execute("""
INSERT INTO products 
(name, category_id, price_for_sale, price_for_buy, photo_url, unit, quantity_by_unit, min_quantity)
VALUES ('موبايل',1,8000,6500,'phone.jpg','قطعة',20,3)
""")

cursor.execute("""
INSERT INTO products 
(name, category_id, price_for_sale, price_for_buy, photo_url, unit, quantity_by_unit, min_quantity)
VALUES ('مكتب',2,2000,1500,'desk.jpg','قطعة',5,1)
""")

cursor.execute("""
INSERT INTO products 
(name, category_id, price_for_sale, price_for_buy, photo_url, unit, quantity_by_unit, min_quantity)
VALUES ('كرسي',2,900,600,'chair.jpg','قطعة',10,2)
""")

cursor.execute("""
INSERT INTO products 
(name, category_id, price_for_sale, price_for_buy, photo_url, unit, quantity_by_unit, min_quantity)
VALUES ('قلم',3,10,5,'pen.jpg','قطعة',100,20)
""")

# -------------------
# إضافة عملية شراء
# -------------------
cursor.execute("""
INSERT INTO purchases (supplier_id, purchase_date, total_amount, info)
VALUES (1, ?, 20000, 'شراء بضاعة')
""", (datetime.now().strftime("%Y-%m-%d"),))

purchase_id = cursor.lastrowid

cursor.execute("""
INSERT INTO purchase_items (purchase_id, product_id, quantity, price)
VALUES (?,1,5,12000)
""", (purchase_id,))

# -------------------
# إضافة عملية بيع
# -------------------
cursor.execute("""
INSERT INTO sales (customer_id, sale_date, total_amount, info)
VALUES (1, ?, 15000, 'بيع لابتوب')
""", (datetime.now().strftime("%Y-%m-%d"),))

sale_id = cursor.lastrowid

cursor.execute("""
INSERT INTO sale_items (sale_id, product_id, quantity, price)
VALUES (?,1,1,15000)
""", (sale_id,))

conn.commit()
conn.close()

print("تم إدخال البيانات التجريبية بنجاح")