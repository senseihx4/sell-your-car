from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('signup/', views.register_user, name='signup'),
    path('register/', views.register_user, name='register'),
    path('register-user/', views.register_user, name='register_user'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('resend-otp/', views.resend_otp, name='resend_otp'),

    path('listings/', views.listings, name='listings'),
    path('sell/', views.sell, name='sell'),
    path('car/<int:pk>/edit/', views.edit_car, name='edit_car'),
    path('car/<int:pk>/delete/', views.delete_car, name='delete_car'),
    path('financing/', views.financing, name='financing'),
    path('about/', views.about, name='about'),
    path('search/', views.search, name='search'),
    path('car/<int:pk>/', views.car_detail, name='car_detail'),
    path('compare/', views.compare, name='compare'),

    path('careers/', views.careers, name='careers'),
    path('press/', views.press, name='press'),
    path('contact/', views.contact, name='contact'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    path('refund/', views.refund, name='refund'),
    path('update-profile/', views.update_profile, name='update_profile'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html') , name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html') , name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='reset_your_password.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
]