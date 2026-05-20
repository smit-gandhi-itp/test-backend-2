# Flask User Authentication API

A production-ready Python Flask backend with JWT-based user authentication.

## Features

- ✅ User Login endpoint with JWT token generation
- ✅ User Registration endpoint
- ✅ Flask 3.x with app factory pattern
- ✅ SQLAlchemy 2.x ORM with proper typing
- ✅ JWT authentication using Flask-JWT-Extended
- ✅ Service layer architecture for clean separation of concerns
- ✅ Environment-based configuration
- ✅ CORS support
- ✅ Database migrations with Flask-Migrate
- ✅ Production-ready with Gunicorn
- ✅ Docker support

## Tech Stack

- **Python**: 3.11+
- **Framework**: Flask 3.1.x
- **ORM**: Flask-SQLAlchemy 3.x (SQLAlchemy 2.x style)
- **Authentication**: Flask-JWT-Extended
- **Database**: SQLite (development) / PostgreSQL-ready (production)
- **Server**: Gunicorn 26.x

## Project Structure

```
.
├── app.py                  # Application factory
├── config.py               # Configuration classes
├── requirements.txt        # Python dependencies
├── models/                 # SQLAlchemy models
│   ├── __init__.py
│   └── user.py            # User model
├── routes/                 # API blueprints
│   ├── __init__.py
│   └── auth_routes.py     # Authentication routes
├── services/               # Business logic layer
│   ├── __init__.py
│   └── auth_service.py    # Authentication service
├── .env.example            # Environment template
├── .gitignore
└── README.md
```

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/smit-gandhi-itp/test-backend-2.git
cd test-backend-2
```

### 2. Set up virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment

```bash
cp .env.example .env
# Edit .env and set your SECRET_KEY and JWT_SECRET_KEY
```

### 5. Initialize database

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 6. Run the application

```bash
python app.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Health Check

```bash
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "flask-auth-api"
}
```

### User Registration

```bash
POST /api/auth/register
Content-Type: application/json

{
  "username": "testuser",
  "password": "password123",
  "email": "test@example.com"
}
```

**Response (201 Created):**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00"
  }
}
```

### User Login

```bash
POST /api/auth/login
Content-Type: application/json

{
  "username": "testuser",
  "password": "password123"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00"
  }
}
```

**Note:** In demo mode, the login endpoint will generate a dummy JWT token for any username/password combination if the user doesn't exist in the database. This allows you to test the endpoint immediately without registration.

## Testing with cURL

### Register a user

```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "password123", "email": "test@example.com"}'
```

### Login

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "password123"}'
```

### Use the JWT token

```bash
# Save the token from login response
TOKEN="your-jwt-token-here"

# Use it in subsequent requests (example for a protected endpoint)
curl -X GET http://localhost:5000/api/protected \
  -H "Authorization: Bearer $TOKEN"
```

## Docker Support

### Build the image

```bash
docker build -t flask-auth-api .
```

### Run the container

```bash
docker run -p 5000:5000 \
  -e SECRET_KEY=your-secret-key \
  -e JWT_SECRET_KEY=your-jwt-secret \
  flask-auth-api
```

## Production Deployment

### Using Gunicorn

```bash
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app('production')"
```

### Environment Variables

For production, ensure these environment variables are set:

- `SECRET_KEY`: Flask secret key (generate with `python -c "import secrets; print(secrets.token_hex(32))"`)
- `JWT_SECRET_KEY`: JWT secret key (generate with `python -c "import secrets; print(secrets.token_hex(32))"`)
- `DATABASE_URL`: PostgreSQL connection string (e.g., `postgresql://user:password@localhost:5432/dbname`)
- `FLASK_DEBUG`: Set to `0` in production

### Database Migration

For PostgreSQL in production:

1. Update `DATABASE_URL` in `.env`:
   ```
   DATABASE_URL=postgresql://user:password@localhost:5432/dbname
   ```

2. Install PostgreSQL driver:
   ```bash
   pip install psycopg2-binary
   ```

3. Run migrations:
   ```bash
   flask db upgrade
   ```

## Security Notes

⚠️ **Important for Production:**

1. **Password Hashing**: The current implementation uses SHA-256 for demonstration. In production, use `bcrypt` or `argon2`:
   ```bash
   pip install flask-bcrypt
   ```

2. **Secret Keys**: Always use strong, randomly generated secret keys in production.

3. **HTTPS**: Always use HTTPS in production to protect JWT tokens in transit.

4. **Token Expiration**: Adjust `JWT_ACCESS_TOKEN_EXPIRES` in `config.py` based on your security requirements.

5. **CORS**: Configure CORS properly for your frontend domain in production.

## Development

### Running tests

```bash
pytest
```

### Code formatting

```bash
black .
flake8 .
```

## License

MIT

## Contributing

Pull requests are welcome! Please ensure your code follows the project structure and includes appropriate tests.
