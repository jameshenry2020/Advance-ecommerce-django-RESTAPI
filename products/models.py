from operator import mod
from django.db import models
from account.models import CustomUser
# Create your models here.


class Product(models.Model):
    user=models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)#admin user or staff user
    name=models.CharField(max_length=200)
    category=models.CharField(max_length=200)
    description=models.TextField()
    rating=models.DecimalField(max_digits=7, decimal_places=2)   
    brand=models.CharField(max_length=100)
    image=models.ImageField(upload_to='prod_thumbnail')
    numReviews=models.IntegerField(default=0)
    price=models.DecimalField(max_digits=8, decimal_places=2)
    countInstock=models.IntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.name

class ProductImgs(models.Model):
    item=models.ForeignKey(Product,on_delete=models.CASCADE)
    img=models.ImageField(upload_to='products')

    def __str__(self):
        return self.item.name

class Variation(models.Model):
    item=models.ForeignKey(Product, on_delete=models.CASCADE)
    name=models.CharField(max_length=200) #size or color

    def __str__(self):
        return self.name


class ItemVariation(models.Model):
    variation=models.ForeignKey(Variation, on_delete=models.CASCADE)
    value=models.CharField(max_length=50)# e.g small, medium or large
    
    def __str__(self):
        return self.value


class Reviews(models.Model):
    item=models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    user=models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)#customer user
    name=models.CharField(max_length=100)
    rating=models.IntegerField(default=0)
    comment=models.TextField()

    def __str__(self):
        return str(self.rating)


class OrderItem(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    item_variations=models.ManyToManyField(ItemVariation)
    quantity=models.IntegerField(default=1)
    completed=models.BooleanField(default=False)
    sub_price=models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    

    def __str__(self):
        return f"orderitem-{self.sub_price}"

class ShippingAddress(models.Model):
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    country=models.CharField(max_length=200)
    city=models.CharField(max_length=100)
    postal_code=models.CharField(max_length=10)
    address=models.CharField(max_length=200)

class Order(models.Model):
    user=models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    paymentMethod=models.CharField(max_length=50)
    reference_code=models.CharField(max_length=20, blank=True, null=True)
    shippingAd=models.ForeignKey(ShippingAddress, related_name='shipping_address', on_delete=models.SET_NULL, null=True)
    shippingFee=models.DecimalField(max_digits=7, decimal_places=2)
    totalPrice=models.DecimalField(max_digits=8, decimal_places=2)
    isPaid=models.BooleanField(default=False)
    being_delivered=models.BooleanField(default=False)
    isReceived=models.BooleanField(default=False)
    paidAt=models.DateTimeField()
    deliveredAt=models.DateTimeField()

    createdAt=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.createdAt)

