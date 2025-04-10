from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'college'

urlpatterns = [
    # 🏠 Core Pages
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # 📄 Document Upload
    path('upload-document/', views.upload_document, name='upload_document'),
    path('delete-document/<int:id>/', views.delete_document, name='delete_document'),

    # 💳 Payment & Admission
    path('payment/', views.payment_page, name='payment_page'),
    path('payment/complete/', views.complete_payment, name='complete_payment'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('admission-status/', views.admission_status, name='admission_status'),
]

# 📂 Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
