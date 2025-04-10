from django.contrib import admin
from django.urls import path, include
from college import views  # Import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),  # Django Admin Panel
    path('', views.home, name='home'),  # Homepage URL
    path('college/', include('college.urls')),  # Include URLs from the college app
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)