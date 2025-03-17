from django.urls import path
from . import views

app_name = 'college'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
<<<<<<< HEAD
=======
    path("upload_document/", views.upload_document, name="upload_document"),
    path('delete_document/<int:id>/', views.delete_document, name='delete_document'),

    # Payment Routes
    path('payment/', views.payment_page, name='payment_page'),
    path('payment/complete/', views.complete_payment, name='complete_payment'),  # New route for completing payment
    path('admission_status/', views.admission_status, name='admission_status'),

>>>>>>> 69002000 (made changes)
]
