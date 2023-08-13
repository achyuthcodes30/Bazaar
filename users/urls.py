from django.urls import path
from . import views
from django.contrib.auth import views as logviews

urlpatterns=[path('signup',views.signup,name='signup'),
             path('logout',logviews.LogoutView.as_view(),name='logout'),
             path('login', logviews.LoginView.as_view(template_name='users/login.html'), name='login'),
             path('myaccount',views.account,name='account'),
             path('vendors/<int:pk>',views.vendor_deets)]