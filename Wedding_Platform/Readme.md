
# Sallety Wedding Booking Platform – Documentation

## 🧾 Project Overview
Sallety is a wedding and event venue booking platform built with Django. The platform allows users to explore event venues, request visitations, book them, or even list their own venues. There are two user roles: **Customers** and **Venue Owners**, each with tailored functionality.

## 🚀 Installation Guide

**Requirements:**
- Python 3.8+
- pip
- virtualenv (recommended)
- Git

**Setup Steps:**
```bash
git clone https://github.com/webdeveloper510/Sallety-Wedding-Booking-Platform.git
cd Sallety-Wedding-Booking-Platform

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt

python3 manage.py makemigration
python3 manage.py migrate
python3 manage.py createsuperuser

python3 manage.py runserver
```

## 🗂 Project Structure
```
Sallety/
├── manage.py
├── requirements.txt
├── sallety/              # Main Django settings & URLs
│   └── settings.py
├── venues/               # Core app for venue logic
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── templates/
├── static/               # CSS, JS, images
├── media/                # User-uploaded content
```

## 💡 Features & Functionality

- **🔍 Homepage**: Displays all available venues in a card/grid format.
- **📖 Venue Details Page**: See full description and gallery. Option to *request a visit* or *book* the venue/table.
- **➕ Add Venue**: Multi-step form for adding venues: Basic Info, Gallery, Location, Amenities & Pricing.
- **📋 Venue Management**: Owners can view their venues, visit requests, and bookings.
- **👥 User Roles**:
  - Customer: can view, book, and request visits
  - Owner: can add/manage venues
- **🔐 Authentication System**: Register/Login with role selection. Protected dashboards per role.

## 🔄 Application URLs

| URL                  | Description                                  |
|----------------------|----------------------------------------------|
| `/`                  | Homepage with venue listings                 |
| `/venue/<id>/`       | View single venue                            |
| `/add-venue/`        | Add a new venue (multi-step)                |
| `/login/, /register/`| Auth system                                  |


## ⚙️ Environment Variables (Optional)

Create a `.env` file and add:
```env
SECRET_KEY=your_secret_key
DEBUG=True
```

## 🛠 Deployment Notes (Optional)

- Use **Gunicorn** and **Nginx** for production
- Set `DEBUG=False`
- Collect static files:
```bash
python3 manage.py collectstatic
```
- Set up a media folder and configure media URL properly