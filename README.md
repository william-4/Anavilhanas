# Anavilhanas

### This is a simple online shop application built with Django. It allows users to browse products, add them to the cart, and proceed to checkout. Admin users can manage products, view orders, and handle user accounts.

## Features
- User authentication (register, login, logout)
- Product management (add, edit, delete)
- Cart system
- Checkout and payment processing (in the works)
- Admin panel for managing products, users, and orders

## Requirements
- Python >= 3.8
- Django >= 4.0
- PostgreSQL (or your preferred database)
- Node / Tailwind

## Installation

### Clone the repository
```bash
git clone https://github.com/william-4/Anavilhanas.git
cd Anavilhanas
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```
### Create a PostgreSQL database (or another DB) and configure your database settings in settings.py.

### Run migrations
```bash
python manage.py migrate
```
### Create a superuser (for admin access)
```bash
python manage.py createsuperuser
```
### Run the Development Server
```bash
python manage.py runserver
```
