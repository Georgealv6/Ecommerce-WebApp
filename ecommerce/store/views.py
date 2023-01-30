from django.shortcuts import render, get_object_or_404
from .models import Category, Product

def store(request):
    products = Product.objects.all()
    context = {
        'product':products,
    }
    return render (request, 'store/home.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    context = {'product':product}
    return render(request, 'store/products/detail.html', context)

def category_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    context = {
        'category':category,
        'product': products
    }
    return render(request, 'store/products/category.html', context)

def cart(request):
    context = {}
    return render (request, 'store/cart.html', context)

def checkout(request):
    context = {}
    return render (request, 'store/checkout.html', context)
