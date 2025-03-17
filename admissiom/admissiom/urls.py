from django.contrib import admin
from django.urls import path, include
<<<<<<< HEAD
from college import views  # Import home view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # Default homepage
    path('college/', include('college.urls')),  # Include college app URLs
]
=======
from college import views  # Import views
from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = [
    path('admin/', admin.site.urls),  # Django Admin Panel
    path('', views.home, name='home'),  # Homepage URL
    path('college/', include('college.urls')),  # Include URLs from the college app
]

# ✅ Serve media files in development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
>>>>>>> 69002000 (made changes)
