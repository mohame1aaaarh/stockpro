# 📦 StockPro - نظام إدارة المخزن التجاري

> مشروع تطبيقي لمقرر **قواعد البيانات** - ترم الربيع 2026

---

## 🧠 المشروع ده إيه؟

StockPro هو تطبيق ويب بسيط لإدارة مخزن تجاري، بيخلي صاحب المخزن يقدر يتابع:
- المنتجات اللي عنده وكمياتها
- الموردين اللي بيشتري منهم
- العملاء اللي بيبيعلهم
- عمليات البيع والشراء
- تقارير بسيطة زي أكتر المنتجات مبيعاً

الفكرة الأساسية إن كل البيانات دي محفوظة في **قاعدة بيانات** ومترابطة مع بعض بعلاقات، وده هو جوهر مقرر قواعد البيانات.

---

## ⚙️ التقنيات المستخدمة

| التقنية | الاستخدام |
|--------|-----------|
| **Python 3** | لغة البرمجة الأساسية |
| **Flask** | فريمووك الويب (بيشغل السيرفر) |
| **SQLite3** | قاعدة البيانات (مدمجة في Python - مفيش سيرفر) |
| **HTML + Jinja2** | عرض الصفحات |
| **Bootstrap 5** | تنسيق الواجهة |

---

## 🗂️ هيكل المشروع

```
stockpro/
│
├── app.py                  # نقطة البداية - تشغيل التطبيق
├── config.py               # الإعدادات (مسار DB مثلاً)
├── init_db.py              # سكريبت إنشاء قاعدة البيانات
├── stockpro.db             # ملف قاعدة البيانات (بيتعمل تلقائي)
│
├── templates/              # صفحات HTML
│   ├── base.html           # القالب الأساسي (navbar وsidebar)
│   ├── dashboard.html      # لوحة التحكم
│   ├── products.html       # المنتجات
│   ├── suppliers.html      # الموردون
│   ├── customers.html      # العملاء
│   ├── sales.html          # المبيعات
│   └── reports.html        # التقارير
│
├── static/
│   └── style.css           # تنسيقات إضافية
│
├── README.md               # الملف ده
└── requirements.txt        # المكتبات المطلوبة
```

---

## 🗄️ قاعدة البيانات - الجداول والعلاقات

المشروع عنده **6 جداول** مترابطة:

```
categories ──────────────────┐
                             ↓
suppliers ──────────── products ──────── sales ──────── customers
                             ↑
                         purchases
                             ↑
suppliers ───────────────────┘
```

### الجداول:

| الجدول | الوصف |
|--------|-------|
| `categories` | فئات المنتجات (إلكترونيات، أثاث...) |
| `suppliers` | الموردون |
| `products` | المنتجات (يرتبط بـ categories و suppliers) |
| `customers` | العملاء |
| `sales` | المبيعات (يرتبط بـ products و customers) |
| `purchases` | المشتريات من الموردين (يرتبط بـ products و suppliers) |

---

## 🚀 طريقة تثبيت البيئة وتشغيل المشروع

### المتطلبات الأساسية
- Python 3.8 أو أحدث
- Git

### خطوات التثبيت

**1. استنسخ المشروع:**
```bash
git clone https://github.com/"YOUR_USERNAME"/stockpro.git
cd stockpro
```

**2. أنشئ بيئة افتراضية (Virtual Environment):**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

**3. ثبت المكتبات المطلوبة:**
```bash
pip install -r requirements.txt
```

**4. أنشئ قاعدة البيانات:**
```bash
python init_db.py
```

**5. شغل التطبيق:**
```bash
python app.py
```

**6. افتح المتصفح على:**
```
http://127.0.0.1:5000
```

---

## ✅ Tasks - المهام بالترتيب

> كل task فيها هدف واضح ونتيجة تقدر تتحقق منها

---

### 🏗️ المرحلة الأولى: الإعداد والبنية الأساسية

#### Task 1 - إعداد المستودع والبيئة
- [ ] إنشاء مستودع على GitHub باسم `stockpro`
- [ ] عمل `git clone` على جهازك
- [ ] إنشاء Virtual Environment وتفعيله
- [ ] إنشاء ملف `requirements.txt` وكتابة `flask` فيه
- [ ] تثبيت Flask بأمر `pip install -r requirements.txt`
- [ ] إنشاء هيكل المجلدات (templates/ و static/)
- [ ] أول `git add . && git commit && git push`

**✅ نتيجة Task 1:** البيئة شغالة وهيكل المشروع موجود على GitHub

---

#### Task 2 - تصميم قاعدة البيانات
- [ ] إنشاء ملف `init_db.py`
- [ ] كتابة `CREATE TABLE` لجدول `categories`
- [ ] كتابة `CREATE TABLE` لجدول `suppliers`
- [ ] كتابة `CREATE TABLE` لجدول `products` مع الـ Foreign Keys
- [ ] كتابة `CREATE TABLE` لجدول `customers`
- [ ] كتابة `CREATE TABLE` لجدول `sales` مع الـ Foreign Keys
- [ ] كتابة `CREATE TABLE` لجدول `purchases` مع الـ Foreign Keys
- [ ] تشغيل `python init_db.py` والتأكد من إنشاء `stockpro.db`
- [ ] فتح الـ DB بـ [DB Browser for SQLite](https://sqlitebrowser.org/) والتأكد من الجداول

**✅ نتيجة Task 2:** ملف `stockpro.db` موجود بـ 6 جداول مترابطة

---

#### Task 3 - بيانات تجريبية
- [ ] إضافة بيانات في `init_db.py` بـ `INSERT INTO`
- [ ] إضافة 3 فئات على الأقل (إلكترونيات، أثاث، مستلزمات مكتب)
- [ ] إضافة 3 موردين
- [ ] إضافة 5 منتجات على الأقل
- [ ] إضافة 3 عملاء
- [ ] إضافة 3 مبيعات تجريبية

**✅ نتيجة Task 3:** قاعدة البيانات مليانة بيانات حقيقية تقدر تتحقق منها

---

### ⚙️ المرحلة الثانية: الـ Backend

#### Task 4 - تشغيل Flask الأول
- [ ] إنشاء `app.py` وإعداد Flask
- [ ] إنشاء `config.py` بمسار قاعدة البيانات
- [ ] كتابة دالة `get_db_connection()` للاتصال بـ SQLite
- [ ] إنشاء أول route `/` يرجع "Hello StockPro"
- [ ] تشغيل `python app.py` والتأكد إنه يفتح على المتصفح

**✅ نتيجة Task 4:** السيرفر شغال وبيرد على المتصفح

---

#### Task 5 - Routes المنتجات (CRUD)
- [ ] Route `/products` يعرض كل المنتجات من DB بـ SELECT + JOIN
- [ ] Route `/products/add` (GET) يعرض فورم الإضافة
- [ ] Route `/products/add` (POST) يحفظ المنتج الجديد بـ INSERT
- [ ] Route `/products/edit/<id>` يعدل منتج بـ UPDATE
- [ ] Route `/products/delete/<id>` يحذف منتج بـ DELETE
- [ ] اختبار كل route من المتصفح

**✅ نتيجة Task 5:** CRUD المنتجات شغال كامل

---

#### Task 6 - Routes الموردين والعملاء
- [ ] نفس Task 5 بالظبط للموردين (`/suppliers`)
- [ ] نفس Task 5 بالظبط للعملاء (`/customers`)

**✅ نتيجة Task 6:** CRUD الموردين والعملاء شغال

---

#### Task 7 - Routes المبيعات والمشتريات
- [ ] Route `/sales` يعرض المبيعات بـ JOIN (اسم العميل واسم المنتج)
- [ ] Route `/sales/add` يسجل بيعة جديدة
- [ ] **مهم:** بعد تسجيل البيعة → UPDATE كمية المنتج (quantity - ?)
- [ ] Route `/purchases/add` يسجل طلب شراء جديد
- [ ] **مهم:** لما الطلب يتسلم → UPDATE كمية المنتج (quantity + ?)

**✅ نتيجة Task 7:** المخزون بيتحدث تلقائياً مع كل بيعة أو شراء

---

#### Task 8 - لوحة التحكم والتقارير
- [ ] Route `/` يجيب الإحصاءات: عدد المنتجات، الموردين، العملاء
- [ ] استعلام: مبيعات الشهر الحالي بـ SUM
- [ ] استعلام: المنتجات اللي وصلت للحد الأدنى (WHERE quantity <= min_quantity)
- [ ] Route `/reports` بأكتر 5 منتجات مبيعاً (GROUP BY + ORDER BY + LIMIT)

**✅ نتيجة Task 8:** لوحة التحكم بتعرض إحصاءات حقيقية

---

### 🎨 المرحلة الثالثة: الواجهة

#### Task 9 - القالب الأساسي
- [ ] إنشاء `base.html` بـ Bootstrap 5 مع دعم RTL
- [ ] Navbar علوي بـ اسم التطبيق
- [ ] Sidebar بـ لينكات (لوحة التحكم، المنتجات، الموردين...)
- [ ] `{% block content %}` للمحتوى المتغير

**✅ نتيجة Task 9:** كل الصفحات هتبقى شكلها موحد

---

#### Task 10 - صفحات العرض
- [ ] `dashboard.html` بـ كروت الإحصاءات وتنبيهات المخزون
- [ ] `products.html` بجدول المنتجات وأزرار التعديل والحذف
- [ ] `suppliers.html` نفس الفكرة للموردين
- [ ] `customers.html` نفس الفكرة للعملاء
- [ ] `sales.html` بجدول المبيعات
- [ ] فورمات الإضافة والتعديل لكل قسم

**✅ نتيجة Task 10:** الواجهة كاملة وشغالة بيانات حقيقية

---

#### Task 11 - التقارير
- [ ] `reports.html` بجدول أكتر المنتجات مبيعاً
- [ ] إجمالي الأرباح (مبيعات - تكلفة)
- [ ] قائمة المنتجات الناقصة

**✅ نتيجة Task 11:** صفحة التقارير كاملة

---

### 🧪 المرحلة الرابعة: الاختبار والتسليم

#### Task 12 - الاختبار الشامل
- [ ] تجربة إضافة منتج جديد والتأكد إنه اتحفظ
- [ ] تجربة عمل بيعة والتأكد إن الكمية اتخصمت
- [ ] تجربة استلام شراء والتأكد إن الكمية زادت
- [ ] تجربة حذف منتج عنده مبيعات (المفروض يرفض)
- [ ] التأكد من إن التنبيهات بتظهر للمنتجات الناقصة

**✅ نتيجة Task 12:** المشروع شغال بدون أي أخطاء

---

#### Task 13 - التسليم النهائي
- [ ] مراجعة الـ README وتحديثه
- [ ] `git add . && git commit -m "final version" && git push`
- [ ] التأكد إن حد تاني يقدر يستنسخ المشروع ويشغله من الصفر
- [ ] تجهيز شرح: إيه الجداول؟ إيه العلاقات؟ إيه أهم الاستعلامات؟

**✅ نتيجة Task 13:** المشروع على GitHub جاهز للتسليم 🎓

---

## 💡 استعلامات SQL مهمة في المشروع

```sql
-- عرض المنتجات مع اسم الفئة والمورد (JOIN)
SELECT p.*, c.name AS category, s.company AS supplier
FROM products p
JOIN categories c ON p.category_id = c.category_id
JOIN suppliers s ON p.supplier_id = s.supplier_id;

-- المنتجات اللي وصلت للحد الأدنى
SELECT * FROM products WHERE quantity <= min_quantity;

-- أكتر المنتجات مبيعاً
SELECT p.name, SUM(s.quantity) AS total_sold
FROM sales s
JOIN products p ON s.product_id = p.product_id
GROUP BY p.product_id
ORDER BY total_sold DESC
LIMIT 5;

-- تحديث المخزون بعد البيع
UPDATE products SET quantity = quantity - ? WHERE product_id = ?;
```

---

## 👥 المساهمون

| الاسم | الدور |
|-------|-------|
| [اسمك هنا] | Developer |

---

## 📄 الترخيص

مشروع أكاديمي - ترم الربيع 2026
