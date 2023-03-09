from django.urls import path
from users import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [ 
    
    path('validate-first-name', csrf_exempt(views.FirstNameValidation.as_view()), name='validate_first_name'),
    path('validate-last-name', csrf_exempt(views.LastNameValidation.as_view()), name='validate_last_name'),
    path('validate-email', csrf_exempt(views.EmailValidation.as_view()), name='validate_email'),
    path('register/', views.Registration.as_view(), name='registration'),
    path('account-activation/<uidb64>/<token>/', views.activate_customer_account, name='activate_account'),
    path('login/', views.login, name='login'), 
    path('dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('update-password/', views.update_password, name='update_password'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('validate-password/<uidb64>/<token>/', views.password_validation, name='password_validation'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('orders/', views.customer_orders, name='customer_orders'),
    path('order_detail/<int:order_id>/', views.order_detail, name='order_detail'),
    path('logout/', views.logout, name='logout'),

]