from django.shortcuts import render
from store.models import Product,Category
from store.views import product_deets,category_view


# Create your views here.
def index(request):
    products=Product.objects.all()[0:6]
    category=Category.objects.all()
    return render(request,"base/home.html",context={'products':products,'category':category})

def about(request):
    return render(request,"base/about.html")

