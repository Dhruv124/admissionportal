from django.contrib import admin
from django.urls import path, include
from college import views  # Import home view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # Default homepage
    path('college/', include('college.urls')),  # Include college app URLs
]
