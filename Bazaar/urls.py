"""
URL configuration for Bazaar project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from users.views import vendor_deets
from store.views import search,product_deets,addtocart,cartview,remove_from_cart,change_quantity,category_view,checkout,callback
urlpatterns = [
    #path('vendor_signin',f"C:/Users/Adhesh/Desktop/heknite/Bazaar/users/templates/users/vendor_signin.html/views.vendor_signin",name = 'vendor_signin'),
    path('',include('base.urls')),
    path('admin/', admin.site.urls),
    path('search',search, name='search'),
    path('add-to-cart/<int:product_id>',addtocart),
    path('remove-from-cart/<int:product_id>',remove_from_cart),
    path('change-quantity/<int:product_id>',change_quantity),
    path('cart',cartview),
    path('',include('users.urls')),
    path('cart/payment',checkout),
    path('callback',callback),
    path('<slug:slug>',category_view),
    path('<slug:category_slug>/<slug:slug>',product_deets)
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
