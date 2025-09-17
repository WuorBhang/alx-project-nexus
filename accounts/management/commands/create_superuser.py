from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()

class Command(BaseCommand):
    help = 'Create a superuser with predefined credentials'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            default='wuor',
            help='Username for the superuser (default: wuor)'
        )
        parser.add_argument(
            '--password',
            type=str,
            default='1234',
            help='Password for the superuser (default: 1234)'
        )
        parser.add_argument(
            '--email',
            type=str,
            default='admin@example.com',
            help='Email for the superuser (default: admin@example.com)'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force creation even if user already exists'
        )

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']
        email = options['email']
        force = options['force']

        try:
            # Check if user already exists
            if User.objects.filter(username=username).exists():
                if force:
                    # Update existing user to be superuser
                    user = User.objects.get(username=username)
                    user.is_superuser = True
                    user.is_staff = True
                    user.set_password(password)
                    user.email = email
                    user.save()
                    self.stdout.write(
                        self.style.SUCCESS(f'Updated existing user "{username}" to superuser')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'User "{username}" already exists. Use --force to update.')
                    )
                    return
            else:
                # Create new superuser
                user = User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password,
                    first_name='Admin',
                    last_name='User'
                )
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created superuser "{username}"')
                )

            # Display login information
            self.stdout.write(
                self.style.SUCCESS('\n' + '='*50)
            )
            self.stdout.write(
                self.style.SUCCESS('SUPERUSER CREATED SUCCESSFULLY')
            )
            self.stdout.write(
                self.style.SUCCESS('='*50)
            )
            self.stdout.write(
                self.style.SUCCESS(f'Username: {username}')
            )
            self.stdout.write(
                self.style.SUCCESS(f'Password: {password}')
            )
            self.stdout.write(
                self.style.SUCCESS(f'Email: {email}')
            )
            self.stdout.write(
                self.style.SUCCESS('='*50)
            )
            self.stdout.write(
                self.style.SUCCESS('You can now login to the admin panel at /admin/')
            )

        except IntegrityError as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating superuser: {e}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Unexpected error: {e}')
            )
