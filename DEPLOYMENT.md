# Deployment Checklist

## Pre-Deployment Checklist

### 1. Environment Variables
Ensure all required environment variables are set in your Render dashboard:

#### Database Service:
- `DB_NAME`: Your database name
- `DB_USER`: Your database user
- `DB_PASSWORD`: Your secure database password

#### Web Service:
- `DATABASE_URL`: Automatically provided by Render
- `SECRET_KEY`: Generate a secure secret key
- `DEBUG`: Set to `False` for production
- `ALLOWED_HOSTS`: Set to `alx-project-nexus-yyh0.onrender.com,.onrender.com`
- `CORS_ALLOWED_ORIGINS`: Set to `https://alx-project-nexus-yyh0.onrender.com`
- `CSRF_TRUSTED_ORIGINS`: Set to `https://alx-project-nexus-yyh0.onrender.com`

### 2. Database Setup
- Ensure PostgreSQL service is running
- Run migrations: `python manage.py migrate`
- Create superuser if needed: `python manage.py createsuperuser`

### 3. Static Files
- Collect static files: `python manage.py collectstatic --noinput`

### 4. Security
- Set `DEBUG=False` in production
- Use strong, unique passwords
- Ensure HTTPS is enabled
- Verify CORS and CSRF settings

## Common Issues and Solutions

### DisallowedHost Error
**Error**: `Invalid HTTP_HOST header: 'alx-project-nexus-yyh0.onrender.com'`

**Solution**: 
1. Check that `ALLOWED_HOSTS` environment variable is set correctly
2. Ensure the domain is included in the ALLOWED_HOSTS list
3. Verify the environment variable is properly configured in Render dashboard

### Database Connection Issues
**Error**: Database connection failures

**Solution**:
1. Verify `DATABASE_URL` is set correctly
2. Check database service is running
3. Ensure database credentials are correct
4. Run migrations if needed

### CORS Issues
**Error**: CORS policy blocking requests

**Solution**:
1. Set `CORS_ALLOWED_ORIGINS` environment variable
2. Ensure the frontend domain is included
3. Check CSRF settings if applicable

## Testing Deployment

### 1. Health Check
Test the basic endpoints:
- `GET /` - Should return the home page
- `GET /api/` - Should return 404 (expected)
- `GET /register.html` - Should return registration page

### 2. API Testing
Test the API endpoints:
- `POST /api/register/` - Should create a new user
- `POST /api/login/` - Should authenticate user
- `GET /api/polls/` - Should return polls list (with auth)

### 3. Frontend Testing
- Test registration form
- Test login functionality
- Test poll viewing and voting

## Rollback Plan

If deployment fails:
1. Check Render logs for specific errors
2. Verify environment variables are set correctly
3. Check database connectivity
4. Review Django settings for production configuration
5. Test locally with production-like settings

## Monitoring

After successful deployment:
1. Monitor application logs
2. Check database performance
3. Monitor API response times
4. Verify all features are working correctly
