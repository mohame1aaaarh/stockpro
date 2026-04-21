# StockPro 📦
**Modern & Lightweight Inventory Management System**

## ✨ مقدمة عن المشروع (Arabic)
**StockPro** هو نظام متكامل وبسيط لإدارة المخازن تم تطويره ليوفر حلاً فعالاً وسهلاً للشركات الصغيرة والمتوسطة. يهدف المشروع إلى تبسيط عمليات تتبع المخزون، إدارة الموردين والعملاء، وتسجيل عمليات البيع والشراء بشكل فوري، مما يساعد في الحفاظ على تدفق عمل منظم وتقارير دقيقة حول أداء المخزن.

---

## 🚀 Key Features

- **📊 Comprehensive Dashboard:** Get a bird's-eye view of your business with real-time stats on products, customers, and today's sales.
- **📦 Inventory Management:** Easily manage your products, categorize them, and track stock levels with automated alerts.
- **🤝 Stakeholder Management:** Dedicated sections for managing both **Suppliers** and **Customers** database.
- **💸 Sales & Purchase Tracking:** Record transactions seamlessly. The system automatically adjusts stock quantities based on sales (decrease) and purchases (increase).
- **📈 Advanced Reporting:** Generate insights on top-selling products, low-stock warnings, and profit/loss calculations.
- **🎨 Modern UI:** A clean, responsive interface with a professional sidebar navigation for smooth user experience.

## 🛠️ Technology Stack

- **Backend:** [Python](https://www.python.org/) with [Flask](https://flask.palletsprojects.com/)
- **Database:** [SQLite3](https://www.sqlite.org/index.html) (Lightweight and efficient)
- **Frontend:** HTML5, Modern CSS, and [Jinja2](https://palletsprojects.com/p/jinja/) Templating.
- **Icons:** FontAwesome for a modern look.

## ⚙️ Installation & Setup

Follow these steps to get a local copy up and running:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mohame1aaaarh/stockpro.git
   ```

2. **Navigate to the project directory:**
   ```bash
   cd stockpro
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database:**
   *Make sure to run the initialization script to set up the tables.*
   ```bash
   python init_db.py
   ```

5. **Run the application:**
   ```bash
   python app.py
   ```

6. **Access the App:**
   Open your browser and visit: `http://127.0.0.1:5666`

## 📸 Screenshots
*(Add your project screenshots here to showcase the UI)*

| Dashboard | Product Management |
|-----------|--------------------|
| ![Dashboard Placeholder](https://via.placeholder.com/400x200?text=Dashboard+View) | ![Products Placeholder](https://via.placeholder.com/400x200?text=Products+Management) |

## 📂 Project Structure
```text
stockpro/
├── app.py              # Main application logic & routes
├── config.py           # Configuration settings
├── init_db.py          # Database initialization script
├── database/           # SQLite database storage
├── static/             # CSS, JS, and product images
└── templates/          # Jinja2 HTML templates
```

## 📝 License
This project is open-source and available under the [MIT License](LICENSE).

---
**StockPro** — *Smart Inventory, Simplified.*