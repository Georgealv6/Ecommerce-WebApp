from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.store, name='home'),
    path('item/<slug:slug>/', views.product_detail, name='product_detail'),
    path('shop/<slug:category_slug>/', views.category_list, name='category_list'),
    path('', views.cart, name='cart'),
    path('', views.checkout, name='checkout'),
]


