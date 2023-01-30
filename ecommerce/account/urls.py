from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from . import views
from .forms import  UserLoginForm, PwdResetForm, PwdResetConfirmForm

app_name = 'account'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='account/registration/login.html', form_class=UserLoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/account/login/'), name='logout'),
    path('signup/', views.account_signup, name='signup'),  
    path('activate/<slug:uidb64>/<slug:token>/', views.account_activate, name='activate'),
    #password
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="account/user/password_reset.html", success_url='password_reset_email_confirm', email_template_name='account/user/password_reset_email.html', form_class=PwdResetForm), name='reset_password'),
    path('password_reset_confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='account/user/password_reset_confirm.html', success_url='/account/password_reset_complete/', form_class=PwdResetConfirmForm), name='password_reset_confirm'),
    path('password_reset/password_reset_email_confirm/', TemplateView.as_view(template_name="account/user/reset_status.html"), name="password_reset_done"),
    path('password_reset_complete/', TemplateView.as_view(template_name="account/user/reset_status.html"), name='password_reset_complete'),
    #user dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/edit/', views.edit_details, name='edit_details'),
    path('profile/delete_user/', views.delete_user, name='delete_user'),
    path('profile/deleted_user/', TemplateView.as_view(template_name='account/user/user_deleted.html'), name='deleted_user'),    
    #address
    path('addresses/', views.view_addresses, name='addresses'),
    path('add_address/', views.add_address, name='add_address'),
    path('addresses/edit/<slug:id>/', views.edit_address, name="edit_address"),
    path('addresses/delete/<slug:id>/', views.delete_address, name="delete_address"),
    path('addresses/set_default/<slug:id>/', views.set_default, name="set_default"),
    path('user_orders/', views.user_orders, name="user_orders"),
    #wishlist
    path("wishlist", views.wishlist, name="wishlist"),
    path("wishlist/add_to_wishlist/<int:id>", views.add_to_wishlist, name="user_wishlist"),
]   