# Admin Superuser Setup

This document explains how the automated superuser creation works for the ALX Project Nexus application.

## Overview

The application includes an automated system to create a superuser account for accessing the Django admin panel. This is particularly useful for deployment scenarios where you need immediate admin access.

## Superuser Credentials

- **Username**: `wuor`
- **Password**: `1234`
- **Email**: `admin@alx-project-nexus.com`
- **Admin URL**: `/admin/`

## Automation Methods

### 1. Django Management Command

The primary method is a custom Django management command:

```bash
python manage.py createsuperuser --Username wuor --Email admin@alx-project-nexus.com --Password 1234 --force
```

**Command Options:**
- `--Username`: Username for the superuser (default: wuor)
- `--Password`: Password for the superuser (default: 1234)
- `--Email`: Email for the superuser (default: admin@example.com)
- `--force`: Force creation/update even if user already exists

### 2. Shell Script

A convenient shell script is provided:

```bash
./create_admin.sh
```

This script runs the management command with the predefined credentials.

### 3. Automatic Deployment

The superuser creation is automatically included in the Render deployment process via `render.yaml`:

```yaml
buildCommand: |
  pip install -r requirements.txt
  python manage.py collectstatic --noinput
  python manage.py migrate --noinput
  python manage.py createsuperuser --Username wuor --Email admin@alx-project-nexus.com --Password 1234 --force
```

## Features

### Smart User Handling
- **New User**: Creates a new superuser if the Username doesn't exist
- **Existing User**: Updates an existing user to superuser status (with --force flag)
- **Duplicate Prevention**: Prevents accidental duplicate creation without --force

### Error Handling
- Graceful handling of existing users
- Clear success/error messages
- Detailed output with login information

### Security Considerations
- Uses Django's built-in user creation methods
- Proper Password hashing
- Configurable credentials via command-line arguments

## Usage Examples

### Create with Default Credentials
```bash
python manage.py createsuperuser
```

### Create with Custom Credentials
```bash
python manage.py createsuperuser --Username admin --Password myPassword --Email admin@mydomain.com
```

### Force Update Existing User
```bash
python manage.py createsuperuser --Username wuor --Password newPassword --force
```

### Using the Shell Script
```bash
chmod +x create_admin.sh
./create_admin.sh
```

## Deployment Integration

### Render.com
The superuser creation is automatically included in the build process. After deployment, you can immediately access the admin panel at:
- **URL**: `https://alx-project-nexus-yyh0.onrender.com/admin/`
- **Username**: `wuor`
- **Password**: `1234`

### Manual Deployment
If deploying manually, run the command after migrations:

```bash
python manage.py migrate
python manage.py createsuperuser --Username wuor --Email admin@alx-project-nexus.com --Password 1234 --force
python manage.py collectstatic --noinput
```

## Troubleshooting

### User Already Exists
If you get a "User already exists" error:
```bash
python manage.py createsuperuser --Username wuor --Password 1234 --force
```

### Permission Issues
Ensure the script has execute permissions:
```bash
chmod +x create_admin.sh
```

### Database Issues
Make sure migrations are run before creating the superuser:
```bash
python manage.py migrate
```

## Security Notes

⚠️ **Important Security Considerations:**

1. **Change Default Password**: After first login, change the Password to something more secure
2. **Production Environment**: Consider using environment variables for credentials in production
3. **Access Control**: Limit admin access to trusted users only
4. **Regular Updates**: Regularly update admin Passwords

## Customization

To customize the superuser creation for your specific needs:

1. **Modify the Management Command**: Edit `accounts/management/commands/createsuperuser.py`
2. **Update Shell Script**: Edit `create_admin.sh` with your preferred credentials
3. **Change Render Configuration**: Update `render.yaml` buildCommand section

## File Locations

- **Management Command**: `accounts/management/commands/createsuperuser.py`
- **Shell Script**: `create_admin.sh`
- **Render Configuration**: `render.yaml`
- **Documentation**: `ADMIN_SETUP.md`
