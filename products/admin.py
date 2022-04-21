from django.contrib import admin
from products.models import *
# Register your models here.


class ItemVariationAdmin(admin.ModelAdmin):
    list_display =['variation', 'value']
    list_filter =['variation', 'variation__item']
    search_fields=['value']

class ItemVariationInLineAdmin(admin.TabularInline):
    model=ItemVariation
    extra =1

class VariationAdmin(admin.ModelAdmin):
    list_display=['item', 'name']
    list_filter=['item']
    search_fields=['name']
    inlines =[ItemVariationInLineAdmin]


class ProductImgInLine(admin.TabularInline):
    model=ProductImgs
    extra =1

class ProductAdmin(admin.ModelAdmin):
    list_display=['name', 'category', 'brand', 'rating','countInstock', 'price']
    list_filter= ['name', 'category']
    search_fields =['name']
    inlines =[ProductImgInLine]

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImgs)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ItemVariation, ItemVariationAdmin)
admin.site.register(Reviews)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(TransactionHistory)
