# College Admission Portal

A modern web application for managing college admissions, built with Django and deployed on Render.

## Features

- User Registration and Authentication
- Document Upload System
- Payment Processing
- Admission Status Tracking
- Admin Dashboard
- Responsive Design

## Tech Stack

- **Backend**: Django 5.1.7
- **Database**: PostgreSQL (Production), SQLite (Development)
- **Frontend**: HTML, CSS, Bootstrap 5
- **Deployment**: Render
- **Static Files**: WhiteNoise
- **Environment Variables**: python-dotenv

## Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Git

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Dhruv124/admissionportal.git
   cd admissionportal
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # On Windows
   .venv\Scripts\activate
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory with the following variables:
   ```
   DEBUG=True
   DJANGO_SECRET_KEY=your-secret-key-here
   DATABASE_URL=sqlite:///db.sqlite3
   ```

5. Run migrations:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Project Structure

```
admissionportal/
├── admissiom/              # Main project directory
│   ├── settings.py         # Project settings
│   ├── urls.py            # Main URL configuration
│   └── wsgi.py            # WSGI configuration
├── college/               # Main application
│   ├── models.py          # Database models
│   ├── views.py           # View functions
│   ├── urls.py            # App URL configuration
│   └── templates/         # HTML templates
├── static/                # Static files (CSS, JS, images)
├── media/                 # User-uploaded files
├── requirements.txt       # Project dependencies
├── render.yaml           # Render deployment configuration
└── manage.py             # Django management script
```

## Deployment

The project is configured for deployment on Render. The `render.yaml` file contains the necessary configuration for both the web service and database.

### Environment Variables for Production

- `DEBUG`: Set to False
- `DJANGO_SECRET_KEY`: A secure secret key
- `DATABASE_URL`: Provided by Render
- `ALLOWED_HOSTS`: Automatically configured

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add new feature'`)
5. Push to the branch (`git push origin feature/improvement`)
6. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

- Dhruv

## Acknowledgments

- Django Documentation
- Bootstrap Documentation
- Render Documentation

---

## 🚀 Features

- 🔐 User Registration & Login
- 📄 Upload & Manage Documents (with PDF/JPEG/PNG support)
- 💳 Payment Integration & Status Tracking
- ✅ Admin Dashboard to Manage Applications
- 📥 Media File Upload Handling
- 🔍 Clean & Organized Project Structure

---

## 🧰 Technologies Used

- Python 3.11+
- Django 5.x
- SQLite (default, can switch to PostgreSQL)
- Bootstrap 5 (UI styling)
- FontAwesome (icons)
- `django-cleanup`, `python-dotenv`, `django-extensions`

---

## ⚙️ Installation & Setup

1. **Clone the Repository**

```bash
git clone https://github.com/Dhruv124/admissionportal.git
cd admissiom
