# CSRF Troubleshooting Guide

## Problem: CSRF Verification Failed

If you're getting a CSRF verification error like:
```
Origin checking failed - https://alx-project-nexus-pf6x.onrender.com does not match any trusted origins.
```

## Solution Steps

### 1. Check Current CSRF Configuration

Run the CSRF check command:
```bash
python manage.py check_csrf
```

This will show you the current configuration and any issues.

### 2. Update Domain Configuration

The error occurs when your domain is not in the `CSRF_TRUSTED_ORIGINS` list. 

#### For the new domain `alx-project-nexus-pf6x.onrender.com`:

**Option A: Update Environment Variables (Recommended)**
Set these environment variables in your Render dashboard:
- `CSRF_TRUSTED_ORIGINS`: `https://alx-project-nexus-pf6x.onrender.com,https://alx-project-nexus-yyh0.onrender.com`
- `CORS_ALLOWED_ORIGINS`: `https://alx-project-nexus-pf6x.onrender.com,https://alx-project-nexus-yyh0.onrender.com`
- `ALLOWED_HOSTS`: `alx-project-nexus-pf6x.onrender.com,alx-project-nexus-yyh0.onrender.com,.onrender.com`

**Option B: Update Settings File**
The settings file has been updated to include both domains by default.

### 3. Verify Configuration

After updating, verify the configuration:
```bash
python manage.py check_csrf
```

You should see both domains in the trusted origins list.

### 4. Redeploy

After updating the configuration:
1. Commit your changes
2. Push to your repository
3. Redeploy on Render

## Common Issues and Solutions

### Issue 1: Domain Not in Trusted Origins
**Error**: `Origin checking failed - [domain] does not match any trusted origins`

**Solution**: Add your domain to `CSRF_TRUSTED_ORIGINS` in settings or environment variables.

### Issue 2: HTTP vs HTTPS Mismatch
**Error**: CSRF fails when using HTTPS

**Solution**: Ensure your trusted origins use `https://` for production domains.

### Issue 3: Wildcard Domains Not Working
**Error**: `*.onrender.com` not working

**Solution**: Django CSRF doesn't support wildcards. List specific domains instead.

### Issue 4: Development vs Production
**Error**: Works locally but fails in production

**Solution**: 
- Set `DEBUG=False` in production
- Use environment variables for production configuration
- Ensure all domains are properly configured

## Configuration Examples

### For Multiple Domains
```python
CSRF_TRUSTED_ORIGINS = [
    "https://alx-project-nexus-pf6x.onrender.com",
    "https://alx-project-nexus-yyh0.onrender.com",
    "https://your-custom-domain.com",
]
```

### For Environment Variables
```bash
CSRF_TRUSTED_ORIGINS=https://alx-project-nexus-pf6x.onrender.com,https://alx-project-nexus-yyh0.onrender.com
CORS_ALLOWED_ORIGINS=https://alx-project-nexus-pf6x.onrender.com,https://alx-project-nexus-yyh0.onrender.com
ALLOWED_HOSTS=alx-project-nexus-pf6x.onrender.com,alx-project-nexus-yyh0.onrender.com,.onrender.com
```

## Testing CSRF Configuration

### 1. Check Configuration
```bash
python manage.py check_csrf
```

### 2. Test API Endpoints
```bash
# Test registration
curl -X POST https://alx-project-nexus-pf6x.onrender.com/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test123","password2":"test123","email":"test@example.com","first_name":"Test","last_name":"User"}'
```

### 3. Test Frontend Forms
- Try submitting the registration form
- Check browser console for errors
- Verify CSRF token is present in form

## Prevention

To prevent future CSRF issues:

1. **Use Environment Variables**: Configure domains via environment variables
2. **Document Domains**: Keep a list of all domains that need access
3. **Test After Deployment**: Always test forms after deployment
4. **Monitor Logs**: Check application logs for CSRF errors

## Quick Fix Commands

### Add Domain to Trusted Origins
```bash
# Add to environment variables
export CSRF_TRUSTED_ORIGINS="https://alx-project-nexus-pf6x.onrender.com,https://alx-project-nexus-yyh0.onrender.com"
```

### Check Current Configuration
```bash
python manage.py check_csrf
```

### Test CSRF Token
```bash
# Get CSRF token
curl -c cookies.txt -b cookies.txt https://alx-project-nexus-pf6x.onrender.com/

# Use CSRF token in POST request
curl -X POST https://alx-project-nexus-pf6x.onrender.com/api/register/ \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: [token-from-cookies]" \
  -b cookies.txt \
  -d '{"username":"test","password":"test123","password2":"test123","email":"test@example.com","first_name":"Test","last_name":"User"}'
```
