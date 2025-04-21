
# Sallety Wedding Booking Platform

Sallety is a Django-based web application for discovering, listing, and booking wedding venues. It supports two user roles — **Customers** and **Venue Owners** — with distinct functionalities.

## 🚀 Features

- 🏠 **Homepage**: Displays all venues.
- 📄 **Venue Detail Page**: Includes image gallery, description, request for visit, and booking option.
- 📝 **Add Venue**: Multi-step form for venue submission (info, gallery, location, amenities, pricing).
- 📋 **Venue Management**: Venue owners can manage their listings, bookings, and visit requests.
- 🔐 **User Authentication**: Register/Login with role selection (Customer or Owner).
- 📊 **Dashboard**: Personalized views for Owners and Customers.

## 📁 Folder Structure

```
Sallety-Wedding-Booking-Platform/
├── Wedding_Platform/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── user/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   ├── static/
│   ├── templates/
│   └── migrations/
├── media/
├── static/
├── db.sqlite3
├── manage.py
└── new-index.html
```

## ⚙️ Setup Instructions

**Requirements:**
- Python 3.8+
- pip
- virtualenv (optional but recommended)
- Git

### 📦 Installation

```bash
git clone https://github.com/webdeveloper510/Sallety-Wedding-Booking-Platform.git
cd Sallety-Wedding-Booking-Platform

python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt

python3 manage.py migrate
python3 manage.py createsuperuser

python3 manage.py runserver
```

## 🔗 Main URLs

| URL                   | Description                            |
|-----------------------|----------------------------------------|
| `/`                   | Homepage with all venues               |
| `/venue/<id>/`        | Detailed view of a venue               |
| `/add-venue/`         | Add new venue                          |
| `/login/`, `/register/` | Authentication routes                 |


