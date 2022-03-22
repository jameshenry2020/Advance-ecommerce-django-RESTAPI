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