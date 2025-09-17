# Online Voting System

A complete full-stack online voting system built with Django, Django REST Framework, and PostgreSQL.

## Features

- User authentication with role-based permissions (Admin and Voter)
- Poll creation and management
- Position and candidate management
- Secure voting functionality
- Real-time results calculation
- Automated notifications when polls end
- API documentation with Swagger and ReDoc

## Tech Stack

- **Backend**: Django 5.2.6, Django REST Framework 3.16.1
- **Database**: PostgreSQL
- **Asynchronous Tasks**: Celery 5.5.3 with Redis 6.4.0
- **API Documentation**: drf-spectacular 0.28.0
- **Frontend**: HTML, CSS, JavaScript

## Setup Instructions

### Prerequisites

- Python 3.11+
- PostgreSQL
- Redis

### 1. Clone the repository

```bash
git clone https://github.com/WuorBhang/alx-project-nexus.git
cd alx-project-nexus
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Variables

Create a `.env` file in the project root with the following variables:

```bash
# Copy the example file
cp env.example .env
```

Then edit `.env` with your actual values:

```env
# Database Configuration
DB_NAME=voting_system
DB_USER=postgres
DB_PASSWORD=your_secure_password_here

# Django Configuration
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# CORS Configuration (for development)
CORS_ALLOWED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000

# CSRF Configuration (for development)
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000

# Celery Configuration (if using Redis)
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

**Important Security Notes:**
- Never commit the `.env` file to version control
- Use strong, unique passwords for production
- Generate a secure SECRET_KEY for production
- Set DEBUG=False in production

### 5. Set up PostgreSQL database

```bash
# Start PostgreSQL service
sudo service postgresql start

# Create database and user
sudo -u postgres psql

postgres=# CREATE DATABASE voting_system;
postgres=# CREATE USER postgres WITH PASSWORD 'postgres';
postgres=# ALTER ROLE postgres SET client_encoding TO 'utf8';
postgres=# ALTER ROLE postgres SET default_transaction_isolation TO 'read committed';
postgres=# ALTER ROLE postgres SET timezone TO 'UTC';
postgres=# GRANT ALL PRIVILEGES ON DATABASE voting_system TO postgres;
postgres=# \q
```

### 6. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create a superuser (Admin)

#### Option 1: Automated Superuser Creation
```bash
python manage.py create_superuser --username wuor --password 1234 --email admin@alx-project-nexus.com
```

#### Option 2: Using the Shell Script
```bash
./create_admin.sh
```

#### Option 3: Manual Creation
```bash
python manage.py createsuperuser
```

**Default Admin Credentials:**
- Username: `wuor`
- Password: `1234`
- Admin URL: `/admin/`

### 9. Start Redis server

```bash
redis-server
```

### 10. Start Celery worker

```bash
celery -A alx-project-nexus worker -l info
```

### 11. Run the development server

```bash
python manage.py runserver
```

## API Endpoints

### Authentication

- `POST /api/register/`: Register a new voter
- `POST /api/login/`: Authenticate a user and return a token

### Polls

- `GET /api/polls/`: List all polls
- `GET /api/polls/<id>/`: Get details of a specific poll
- `POST /api/polls/<id>/vote/`: Cast a vote for a specific candidate
- `GET /api/polls/<id>/results/`: Get the results of a poll

### API Documentation

- `/api/docs/`: Swagger UI documentation
- `/api/redoc/`: ReDoc documentation
- `/api/schema/`: Raw schema

## Postman API Examples

### Register a new voter

```
POST /api/register/
Content-Type: application/json

{
    "username": "voter1",
    "password": "securepassword123",
    "password2": "securepassword123",
    "email": "voter1@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "1234567890"
}
```

### Login

```
POST /api/login/
Content-Type: application/json

{
    "username": "voter1",
    "password": "securepassword123"
}
```

### Get all polls

```
GET /api/polls/
Authorization: Token <your-token>
```

### Get poll details

```
GET /api/polls/1/
Authorization: Token <your-token>
```

### Cast a vote

```
POST /api/polls/1/vote/
Authorization: Token <your-token>
Content-Type: application/json

{
    "position": 1,
    "candidate": 3
}
```

### Get poll results

```
GET /api/polls/1/results/
Authorization: Token <your-token>
```

## Frontend

The frontend is built with HTML, CSS, and JavaScript. It communicates with the backend via API calls.

To access the frontend, navigate to:

- Landing Page: `http://localhost:8000/`
- Registration Page: `http://localhost:8000/register.html`
- Login Page: `http://localhost:8000/login.html`
- Polls List Page: `http://localhost:8000/polls.html`
- Poll Detail Page: `http://localhost:8000/poll-detail.html?id=1`
- Results Page: `http://localhost:8000/poll-results.html?id=1`
- Admin Panel: `http://localhost:8000/admin/` (Username: wuor, Password: 1234)

## Deployment on Render

### Environment Variables Setup

When deploying to Render, you need to set the following environment variables in your Render dashboard:

#### Database Service Environment Variables:
- `DB_NAME`: Your database name (e.g., `voting_system_13u3`)
- `DB_USER`: Your database user (e.g., `root`)
- `DB_PASSWORD`: Your secure database password

#### Web Service Environment Variables:
- `DATABASE_URL`: Automatically provided by Render when linking to PostgreSQL service
- `SECRET_KEY`: Generate a secure secret key (Render can auto-generate this)
- `DEBUG`: Set to `False` for production
- `ALLOWED_HOSTS`: Set to your domain (e.g., `.onrender.com,your-app-name.onrender.com`)
- `CORS_ALLOWED_ORIGINS`: Set to your frontend domain
- `CSRF_TRUSTED_ORIGINS`: Set to your frontend domain

### Render Configuration

The `render.yaml` file is configured to use environment variables instead of hardcoded secrets. Make sure to set all required environment variables in your Render dashboard before deploying.

### Security Best Practices

1. **Never commit secrets to version control**
2. **Use strong, unique passwords**
3. **Generate secure SECRET_KEY for production**
4. **Set DEBUG=False in production**
5. **Use HTTPS in production**
6. **Regularly rotate secrets and passwords**
