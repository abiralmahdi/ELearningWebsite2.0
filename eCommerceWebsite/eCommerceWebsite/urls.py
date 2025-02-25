from django.contrib import admin
from django.urls import path
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include('home.urls')),
    path('admin/', admin.site.urls), 
    path('accounts/', include('accounts.urls')), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)