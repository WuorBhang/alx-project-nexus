from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Check CSRF configuration and trusted origins'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('CSRF Configuration Check')
        )
        self.stdout.write('=' * 50)
        
        # Check CSRF_TRUSTED_ORIGINS
        trusted_origins = getattr(settings, 'CSRF_TRUSTED_ORIGINS', [])
        self.stdout.write(f'CSRF_TRUSTED_ORIGINS: {trusted_origins}')
        
        # Check ALLOWED_HOSTS
        allowed_hosts = getattr(settings, 'ALLOWED_HOSTS', [])
        self.stdout.write(f'ALLOWED_HOSTS: {allowed_hosts}')
        
        # Check CORS_ALLOWED_ORIGINS
        cors_origins = getattr(settings, 'CORS_ALLOWED_ORIGINS', [])
        self.stdout.write(f'CORS_ALLOWED_ORIGINS: {cors_origins}')
        
        # Check DEBUG mode
        debug = getattr(settings, 'DEBUG', False)
        self.stdout.write(f'DEBUG: {debug}')
        
        # Check CSRF middleware
        middleware = getattr(settings, 'MIDDLEWARE', [])
        csrf_middleware = 'django.middleware.csrf.CsrfViewMiddleware' in middleware
        self.stdout.write(f'CSRF Middleware Enabled: {csrf_middleware}')
        
        self.stdout.write('=' * 50)
        
        # Recommendations
        self.stdout.write(
            self.style.WARNING('Recommendations:')
        )
        
        if not trusted_origins:
            self.stdout.write(
                self.style.ERROR('❌ CSRF_TRUSTED_ORIGINS is empty!')
            )
            self.stdout.write('Add your domain to CSRF_TRUSTED_ORIGINS')
        
        if debug:
            self.stdout.write(
                self.style.WARNING('⚠️  DEBUG is True - consider setting to False in production')
            )
        
        if not csrf_middleware:
            self.stdout.write(
                self.style.ERROR('❌ CSRF middleware is not enabled!')
            )
        
        self.stdout.write('=' * 50)
        self.stdout.write(
            self.style.SUCCESS('CSRF check completed!')
        )
