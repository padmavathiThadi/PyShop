# 🛒 PyShop

A full-stack e-commerce web application built with Django.

PyShop allows users to browse products, search and filter products, manage a shopping cart, apply discount codes, place orders, and track order status.

## 🚀 Features

### 🛍️ Product Management

- Product catalogue
- Product images
- Stock management
- Search products
- Filter products by price
- Out-of-stock handling

### 🛒 Shopping Cart

- Add products to cart
- Increase/decrease quantity
- Remove products
- Automatic cart totals

### 💳 Checkout

- Checkout page
- Discount codes
- Discount calculation
- Stock validation
- Order placement

### 👤 Authentication

- User registration
- User login
- User logout
- User-specific orders

### 📦 Order Management

- Order creation
- Order items
- Order history
- Order details
- Order status tracking
- Pending, Processing, Shipped and Delivered statuses

### 🔐 Django Admin

Administrators can manage:

- Products
- Offers
- Orders
- Order items
- Customers
- Order status

## 🛠️ Tech Stack

- Python
- Django
- SQLite
- HTML
- CSS
- Bootstrap
- Git
- GitHub

## 📁 Project Structure

- `accounts/` — authentication and user management
- `products/` — products, cart, checkout and orders
- `pyshop/` — Django project configuration
- `manage.py` — Django management script
- `.gitignore` — Git ignored files

## ⚙️ How to Run

### 1. Clone the repository

`git clone https://github.com/padmavathiThadi/PyShop.git`

### 2. Enter the project directory

`cd PyShop`

### 3. Create a virtual environment

`python -m venv .venv`

### 4. Activate the virtual environment on Windows

`.venv\Scripts\activate`

### 5. Install Django

`pip install django`

### 6. Apply migrations

`python manage.py migrate`

### 7. Create an admin user

`python manage.py createsuperuser`

### 8. Start the development server

`python manage.py runserver`

Open `http://127.0.0.1:8000/products/` in your browser.

## 🎯 What I Learned

- Django project and app structure
- Django models and relationships
- Database migrations
- Django ORM
- User authentication
- Sessions and shopping carts
- Form handling
- Django templates
- Django Admin customization
- Order and inventory management
- Git and GitHub

## 🔮 Future Improvements

- Online payment integration
- Product categories
- Product reviews and ratings
- Email notifications
- Production deployment

## 👩‍💻 Author

**Padmavathi Thadi**

GitHub: https://github.com/padmavathiThadi/PyShop
