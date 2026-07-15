from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # Django Admin
    path('admin/', admin.site.urls),

    # Home Dashboard
    path('', include('dashboard.urls')),

    # Accounts
    path('accounts/', include('accounts.urls')),

    # Community Issues
    path('issues/', include('issues.urls')),

    # Community Events
    path('events/', include('events.urls')),

    # Notifications
    path('notifications/', include('notifications.urls')),

    path('opportunities/', include('opportunities.urls')),

]

# Serve uploaded media files during development
if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

    # Optional: serve static files during development
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )