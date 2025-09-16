from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('accounts.urls')),
    path('api/', include('polls.urls')),
    
    # API Schema documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # cspell:ignore redoc
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # Frontend routes
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('index.html', TemplateView.as_view(template_name='index.html'), name='index'),
    path('polls.html', TemplateView.as_view(template_name='polls.html'), name='polls-page'),
    path('poll-detail.html', TemplateView.as_view(template_name='poll-detail.html'), name='poll-detail-page'),
    path('poll-results.html', TemplateView.as_view(template_name='poll-results.html'), name='poll-results-page'),
    path('login.html', TemplateView.as_view(template_name='login.html'), name='login-page'),
    path('register.html', TemplateView.as_view(template_name='register.html'), name='register-page'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)