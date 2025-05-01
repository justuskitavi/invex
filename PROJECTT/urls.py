"""
URL configuration for PROJECTT project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views 
from django.urls import path, include
from users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('verify-otp/', user_views.verify_otp, name='verify-otp'),    
    path('resend-otp/', user_views.resend_otp, name='resend-otp'),    
    path('profile/', user_views.profile, name='profile'),
    path('login/', user_views.loginView, name='login'),
    path('forgot-password/', user_views.forgot_password, name='forgot-password'),
    path('verify-reset-otp/', user_views.verify_reset_otp, name='verify-reset-otp'),
    path('resend-reset-otp/', user_views.resend_otp, name='resend-reset-otp'),
    path('set-new-password/', user_views.set_new_password,name='set-new-password'),
    path('change-password/', user_views.change_password_request, name='change-password'),
    path('verify-change-otp/', user_views.verify_change_otp, name='verify-change-otp'),
    path('set-changed-password/', user_views.set_changed_password, name='set-changed-password'),
    path('resend-change-otp/', user_views.resend_change_otp, name='resend-change-otp'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('create-shop/', user_views.create_shop, name='create-shop'),
    path('view-shop', user_views.view_shop, name='view-shop'),    
    path('', include('invex.urls')),
    path('shop/<str:shopID>/', user_views.shop_detail, name='shop-detail'),
    path('shop/<str:shopID>/add-product/', user_views.add_product, name='add-product'),
    path('shop/<str:shopID>/add-stock/<str:productID>/', user_views.add_stock, name='add-stock'),
    path('shop/<str:shopID>/sell-product/<str:productID>/', user_views.sell_product, name='sell-product'),
    path('employees/', user_views.employee_list, name='employee-list'),
    path('employees/add/', user_views.add_employee, name='add-employee'),
    path('employees/<str:employeeID>/fire/', user_views.fire_employee, name='fire-employee'),
    path('shop/<str:shopID>/edit-product/<str:productID>/', user_views.edit_product, name='edit-product'),
    path('shop/<str:shopID>/delete-product/<str:productID>/', user_views.delete_product, name='delete-product'),

    
    
]
