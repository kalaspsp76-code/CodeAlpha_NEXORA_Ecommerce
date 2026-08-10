# NEXORA — CodeAlpha Task 1: Simple E-commerce Store

A professional full-stack e-commerce website built with HTML, CSS, JavaScript, Django and SQLite.

## Features
- Product listing and search
- Category filtering
- Product details page
- Session shopping cart
- Quantity updates/removal
- User registration/login/logout
- Checkout and order processing
- Order history
- Django admin for products and orders
- SQLite database

## Run in VS Code / Terminal

```bash
python -m venv venv
```

Windows:
```bash
venv\Scripts\activate
```

Install:
```bash
pip install -r requirements.txt
```

Database:
```bash
python manage.py migrate
python manage.py seed_products
```

Create admin:
```bash
python manage.py createsuperuser
```

Start:
```bash
python manage.py runserver
```

Open:
http://127.0.0.1:8000/

Admin:
http://127.0.0.1:8000/admin/

## GitHub
Repository name:
`CodeAlpha_NEXORA_Ecommerce`

Suggested description:
"Full-stack e-commerce store developed for the CodeAlpha Full Stack Development Internship using Django, HTML, CSS, JavaScript and SQLite."
