from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    title=models.CharField(max_length=30)
    slug=models.SlugField(max_length=30)
    class Meta:
        verbose_name_plural="Categories"
    
    def __str__(self):
        return self.title 
    

class Product(models.Model):
    user=models.ForeignKey(User,related_name="product",on_delete=models.CASCADE)
    category=models.ForeignKey(Category,related_name="product",on_delete=models.CASCADE)
    title=models.CharField(max_length=30)
    slug=models.SlugField(max_length=30)
    description=models.TextField(blank=True)
    price=models.IntegerField()
    image=models.ImageField(upload_to='uploads/productimages',blank=True,null=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering=('-created',)
    def display_price(self):
        return self.price/1.0
    
    def __str__(self):
        return self.title
    
    
class Orders(models.Model):
    payment_status_choices = (
        (1, 'SUCCESS'),
        (2, 'FAILURE' ),
        (3, 'PENDING'),
    )
    total=models.IntegerField(blank=True,null=True)
    payment_status = models.IntegerField(choices = payment_status_choices, default=3)
    createdby=models.ForeignKey(User,related_name='orders',on_delete=models.CASCADE)
    createdat=models.DateTimeField(auto_now_add=True)
    razorpay_order_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=500, null=True, blank=True)
    
    
class OrderItem(models.Model):
    order=models.ForeignKey(Orders,related_name='items',on_delete=models.CASCADE)
    product= models.ForeignKey(Product,related_name='items',on_delete=models.CASCADE)
    price=models.IntegerField()
    quantity=models.IntegerField(default=1)
    
    
    
    
    
    