from django.shortcuts import render,redirect,HttpResponse
from django.db.models  import Q
from store.models import Product,Category,Orders,OrderItem
from django.contrib.auth.decorators import login_required
from django import forms
from django.views.decorators.csrf import csrf_exempt
import razorpay
import json
# Create your views here.
from django.conf import settings

from .models import Product

class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        
        self.cart = cart

    def __iter__(self):
        for p in self.cart.keys():
            self.cart[str(p)]['product'] = Product.objects.get(pk=p)
        
        for item in self.cart.values():
            item['total_price'] = int(item['product'].price * item['quantity'])

            yield item
            
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True
        
    def add(self, product_id, quantity=1, update_quantity=False):
        product_id = str(product_id)   
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': int(quantity), 'id': product_id}
        
        else:
            self.cart[product_id]['quantity'] += int(quantity)
            
            if self.cart[product_id]['quantity'] == 0:
                self.remove(product_id)
        
        self.save()
     
    
    def remove(self, product_id):
        if str(product_id) in self.cart:
            del self.cart[str(product_id)]

            self.save()
    
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def get_total_cost(self):
        for p in self.cart.keys():
            self.cart[str(p)]['product'] = Product.objects.get(pk=p)
        
        return int(sum(item['product'].price * item['quantity'] for item in self.cart.values()))/1.0


   
def addtocart(request,product_id):
    cart=Cart(request)
    cart.add(product_id)
    return redirect('../')

def cartview(request):
    cart=Cart(request)
    
    return render(request,'store/cartview.html',{'cart':cart})

def change_quantity(request,product_id):
    action = request.GET.get('action', '')

    if action:
        quantity = 1

        if action == 'decrease':
            quantity = -1

        cart = Cart(request)
        cart.add(product_id, quantity, True)
    
    return redirect(cartview)

def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)

    return redirect(cartview)


def checkout(request):
    cart=Cart(request)
    if request.method=="POST":
        total_price = 0
        for item in cart:
                product = item['product']
                total_price += product.price * int(item['quantity'])
                
        order=Orders.objects.create(createdby=request.user,total=total_price)
        order.save()
        for item in cart:
                product = item['product']
                quantity = int(item['quantity'])
                price = product.price * quantity

                item = OrderItem.objects.create(order=order, product=product, price=price, quantity=quantity)
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        razorpay_order = client.order.create(
            {"amount": int(total_price) * 100, "currency": "INR", "payment_capture": "0"}
        )
        order.razorpay_order_id = razorpay_order['id']
        order.save()     
        cart.clear()
        return render(request, 'store/payment.html', {'order':order, 'order_id': razorpay_order['id'],'final_price':total_price*100, 'razorpay_merchant_id':settings.RAZORPAY_KEY_ID, 'callback_url':'../callback'})
    else:
        return HttpResponse("505 Not Found")   
                
                
@csrf_exempt
def callback(request):
    def verify_signature(response_data):
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings. RAZORPAY_KEY_SECRET))
        return client.utility.verify_payment_signature(response_data)

    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")
        order = Orders.objects.get(razorpay_order_id=order_id)
        order.razorpay_payment_id= payment_id
        order.razorpay_signature = signature_id
        order.save()
        if verify_signature(request.POST):
            order.payment_status = 1
            order.save()
            return render(request, "store/success.html", context={"status": order.payment_status})
        else:
            order.payment_status = 2
            order.save()
            return render(request, "store/failed.html", context={"status": order.payment_status})
    else:
        payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
        provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
            "order_id"
        )
        order = Orders.objects.get(provider_order_id=provider_order_id)
        order.razorpay_payment_id = payment_id
        order.payment_status = 2
        order.save()
        return render(request, "store/failed.html", context={"status": order.payment_status})
        

def cart(request):
    return {'cart':Cart(request)}

def search(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    return render(request, 'store/search.html', {
        'query': query,
        'products': products
    })
def product_deets(request,category_slug,slug):
    product=Product.objects.get(slug=slug)
    return render(request,"store/product_deets.html",context={'product':product})
    
def category_view(request,slug):
    category=Category.objects.get(slug=slug)
    products=category.product.all()
    return render(request,"store/category_deets.html",context={"category":category,"products":products})


