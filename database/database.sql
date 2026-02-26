create table if not exists admin (--جدول نحط في الباسورد و اسم المستخدم عشان نعمل واجهه تسجيل دخول
    id integer primary key autoincrement,
    username text not null unique,
    password text not null,
)

insert into admin (username,password) values ("admin","admin123")--بيانات افتراضيه للتسجيل الدخول

