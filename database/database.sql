create table if not exists admin ( --جدول تسجيل الد info (--جدول نحط في الباسورد و اسم المستخدم عشان نعمل واجهه تسجيل دخول
    id integer primary key autoincrement,
    username text unique not null ,
    password text not null
);

create table if not exists categories ( --جدول الاقسام
    id integer primary key autoincrement,
    name text not null unique
);

insert OR IGNORE into admin (username,password) values ("admin","admin123");--بيانات افتراضيه للتسجيل الدخول

create table if not exists products ( --جدول المنتجات
    id integer primary key autoincrement,
    name text not null,
    category_id integer not null,
    price_for_sale real not null,
    price_for_buy real not null,
    photo_url text not null,
    unit text not null,
    quantity_by_unit  integer default 0 not null,
    min_quantity integer default 0 not null,
    foreign key (category_id) references categories(id)
);

create table if not exists customers ( --جدول العملاء
    id integer primary key autoincrement,
    name text not null,
    phone_number text,
    email text,
    address text
);

create table if not exists suppliers ( --جدول الموردين
    id integer primary key autoincrement,
    name text not null,
    phone_number text,
    email text,
    address text
);

create table if not exists purchases (
    id integer primary key autoincrement,
    supplier_id integer not null,
    purchase_date text not null,
    total_amount real not null,
    info text,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
);

create table if not exists purchase_items (
    id integer primary key autoincrement,
    purchase_id integer not null,
    product_id integer not null,
    quantity integer not null,
    price real not null,
    FOREIGN KEY (purchase_id) REFERENCES purchases(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

create table if not exists sales (
    id integer primary key autoincrement,
    customer_id integer not null,
    sale_date text not null,
    total_amount real not null,
    info text,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

create table if not exists sale_items (
    id integer primary key autoincrement,
    sale_id integer not null,
    product_id integer not null,
    quantity integer not null,
    price real not null,
    FOREIGN KEY (sale_id) REFERENCES sales(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

