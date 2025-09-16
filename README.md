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

### 4. Set up PostgreSQL database

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

### 5. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a superuser (Admin)

```bash
python manage.py createsuperuser
```

### 7. Start Redis server

```bash
redis-server
```

### 8. Start Celery worker

```bash
celery -A alx-project-nexus worker -l info
```

### 9. Run the development server

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
