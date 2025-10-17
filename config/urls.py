from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Group App-Level URLs under a Common API Path
app_urls = [
    path('users/', include('users.urls')),
    path('courses/', include('courses.urls')),
    path('enrolls/', include('enrolls.urls')),
    path('payment/', include('payment.urls')),
    path('contact/', include('contact.urls')),
    path('sadaqah/', include('sadaqah.urls')),
    path('support/', include('support.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(app_urls)),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)