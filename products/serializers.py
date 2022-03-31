from rest_framework import serializers
from account.models import CustomUser
from products.models import *

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductImgs
        fields=['id', 'img']

class ItemVariationSerializer(serializers.ModelSerializer):
    class Meta:
        model= ItemVariation
        fields=(
            'id',
            'value'
        )

class VariationSerializer(serializers.ModelSerializer):
    item_variations=serializers.SerializerMethodField()
    class Meta:
        model=Variation
        fields=(
            'id',
            'name',
            'item_variations'
        )

    def get_item_variations(self, obj):
        return ItemVariationSerializer(obj.itemvariation_set.all(), many=True).data


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields='__all__'

class ProductDetailSerializer(serializers.ModelSerializer):
    thumbnails=serializers.SerializerMethodField()
    variations=serializers.SerializerMethodField()
    class Meta:
        model=Product
        fields=[
            'id',
             'name',
             'category',
             'description',
             'rating',
             'brand',
             'image', 
             'numReviews',
             'price',
             'countInstock',
             'thumbnails',
             'variations'
        ]

    def get_variations(self, obj):
        return VariationSerializer(obj.variation_set.all(), many=True).data

    def get_thumbnails(self, obj):
        return ProductImageSerializer(obj.productimgs_set.all(), many=True).data


class VariationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=Variation
        fields=('id','name')


class ItemVariationDetailSerializer(serializers.ModelSerializer):
    variation=serializers.SerializerMethodField()
    class Meta:
        model=ItemVariation
        fields=[
            'id',
            'value',
            'variation'
        ]

    def get_variation(self, obj):
        return VariationDetailSerializer(obj.variation).data

class OrderItemSerializer(serializers.ModelSerializer):
    item=serializers.SerializerMethodField()
    item_variations=serializers.SerializerMethodField()
    final_price=serializers.SerializerMethodField()

    class Meta:
        model=OrderItem
        fields=[
            'id',
            'item',
            'quantity',
            'item_variations',
            'final_price'
        ]

    def get_item(self, obj):
        return ProductSerializer(obj.product).data

    def get_final_price(self, obj):
        return obj.get_total_item_price()

    def get_item_variations(self, obj):
        return ItemVariationDetailSerializer(obj.item_variations.all(), many=True).data


class OrderSerializer(serializers.ModelSerializer):
    order_items=serializers.SerializerMethodField()
    total=serializers.SerializerMethodField()
    class Meta:
        model=Order
        fields=(
            'id',
            'order_items',
            'total'
        )

    def get_order_items(self, obj):
        return OrderItemSerializer(obj.items.all(), many=True).data

    def get_total(self, obj):
        return obj.get_total()