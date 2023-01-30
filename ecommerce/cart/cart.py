from store.models import Product
from decimal import Decimal


from checkout.models import DeliveryOptions

class Cart():
    #providing some defualt behaviors thats can be inherited or overrided.

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('skey')
        if 'skey' not in request.session:
            cart = self.session['skey'] = {}
        self.cart = cart    

    def add(self, product, qty):
        #adding and updating the users basket session data

        product_id = str(product.id)
        
        if product_id in self.cart:
            self.cart[product_id]['qty'] = qty
        else:    
            self.cart[product_id] = {'price': str(product.regular_price), 'qty': qty}

        self.save()
    
    def __iter__(self):
        # collect the product_id in the session data to query the database and return products 

        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])   
            item['total_price'] = item['price'] * item['qty']
            yield item

    def __len__(self): 
        #get cart data and count of the qty if items

        return sum(item['qty'] for item in self.cart.values())

    def get_subtotal_price(self):
        return sum(Decimal(item["price"]) * item["qty"] for item in self.cart.values())

    def get_delivery_price(self):
        newprice = 0.00

        if "purchase" in self.session:
            newprice = DeliveryOptions.objects.get(id=self.session["purchase"]["delivery_id"]).delivery_price

        return newprice    

    def get_total_price(self):
        newprice = 0.00
        subtotal = sum(Decimal(item["price"]) * item["qty"] for item in self.cart.values())

        if "purchase" in self.session:
            newprice = DeliveryOptions.objects.get(id=self.session["purchase"]["delivery_id"]).delivery_price

        total = subtotal + Decimal(newprice)
        return total

    def update_item(self, product, qty):
        #update items on cart 

        product_id = str(product)
        if product_id in self.cart:
            self.cart[product_id]['qty'] = qty

        self.save()

    def cart_update_delivery(self, deliveryprice=0):
        subtotal = sum(Decimal(item["price"]) * item["qty"] for item in self.cart.values())
        total = subtotal + Decimal(deliveryprice)
        return total
            
    def remove_item(self, product):
        # removing items from cart 
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        del self.session['skey']
        del self.session['address']
        del self.session['purchase']
        self.save()

    def save(self):
        self.session.modified = True    
 