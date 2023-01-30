from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from store.models import Product

from .cart import Cart

def cart_summary(request):
    cart = Cart(request)
    context = {
        'cart': cart
    }
    return render(request, 'cart/cart.html', context)

# view that will respond with add to cart button
def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        product = get_object_or_404(Product, id=product_id)
    
        cart.add(product=product, qty=product_qty)

        cartqty = cart.__len__()
        response = JsonResponse({'qty': cartqty})
        return response

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        cart.remove_item(product=product_id)
        

        cartqty = cart.__len__()
        carttotal = cart.get_total_price()
        response = JsonResponse({'qty':cartqty, 'subtotal':carttotal})
        return response

def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        cart.update_item(product=product_id, qty=product_qty)

        cartqty = cart.__len__()
        carttotal = cart.get_total_price()
        response = JsonResponse({'qty':cartqty, 'subtotal':carttotal})
        return response