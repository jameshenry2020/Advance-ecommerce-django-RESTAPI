from operator import mod
from sqlite3 import Timestamp
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

    class Meta:
        unique_together=(
            ('item', 'name')
        )

    def __str__(self):
        return self.name


class ItemVariation(models.Model):
    variation=models.ForeignKey(Variation, on_delete=models.CASCADE)
    value=models.CharField(max_length=50)# e.g small, medium or large
    
    class Meta:
        unique_together=(
            ('variation', 'value')
        )
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
    user=models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    item_variations=models.ManyToManyField(ItemVariation)
    quantity=models.IntegerField(default=1)
    completed=models.BooleanField(default=False)
    sub_price=models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    

    def __str__(self):
        return f"orderitem- for-{self.user.first_name}"

    def get_total_item_price(self):
        return self.quantity * self.product.price

    def get_final_total_price(self):
        return self.get_total_item_price()


class ShippingAddress(models.Model):
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    country=models.CharField(max_length=200)
    city=models.CharField(max_length=100)
    postal_code=models.CharField(max_length=10)
    address=models.CharField(max_length=200)
    default_add=models.BooleanField(default=False)
    

    def __str__(self):
        return f"deliver order to-{self.city}-{self.id}"

class Order(models.Model):
    user=models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    payment=models.ForeignKey('TransactionHistory', on_delete=models.SET_NULL, null=True, blank=True)
    reference_code=models.CharField(max_length=20, blank=True, null=True)
    items=models.ManyToManyField(OrderItem)
    shippingAd=models.ForeignKey(ShippingAddress, related_name='orders', on_delete=models.SET_NULL, blank=True, null=True)
    shippingFee=models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    isPaid=models.BooleanField(default=False)
    being_delivered=models.BooleanField(default=False)
    isReceived=models.BooleanField(default=False)
    paidAt=models.DateTimeField(blank=True, null=True)
    deliveredAt=models.DateTimeField(blank=True, null=True)

    createdAt=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.createdAt)

    def get_total(self):
        total=0
        for order_item in self.items.all():
            total +=order_item.get_final_total_price()
        if self.shippingFee is not None:
            final_total= total + self.shippingFee
            return final_total
        return total


class TransactionHistory(models.Model):
    stripe_customer_id=models.CharField(max_length=50, null=True, blank=True)
    amount=models.DecimalField(max_digits=8, decimal_places=2)
    user=models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=50, null=True, blank=True)
    

    def __str__(self):
        return self.user.first_name