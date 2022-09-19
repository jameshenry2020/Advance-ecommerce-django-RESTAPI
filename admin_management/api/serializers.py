from unicodedata import category
from rest_framework import serializers
from products.models import Product, ProductImgs



class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductImgs
        fields = ['id','img']

class ProductCreateSerializer(serializers.ModelSerializer):
    thumbnails=ProductImageSerializer(many=True)
    class Meta:
        model = Product
        fields = [
                'productname',
                'category',
                'description',
                'brand',
                'image',
                'price',
                'countInstock',
                'thumbnails'          
             ]
        
    def create(self, validated_data):
        request=self.context.get('request')
        thumbnails=validated_data.pop('thumbnails')
        product = Product.objects.create(
            user=request.user,
            productname=validated_data.get('productname'),
            category=validated_data.get('category'),
            description=validated_data.get('description'),
            brand=validated_data.get('brand'),
            image=validated_data.get('image'),
            price=validated_data.get('price'),
            countInstock=validated_data.get('countInstock')
        )
        for thumbnail in thumbnails:
            ProductImgs.objects.create(item=product, img=thumbnail['img'])
        return product

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.category = validated_data.get('category', instance.category)
        instance.description = validated_data.get('description', instance.description)
        instance.brand = validated_data.get('brand', instance.brand)
        instance.image = validated_data.get('image', instance.image)
        instance.price = validated_data.get('price', instance.price)
        instance.countInstock = validated_data.get('countInstock', instance.countInstock)
        instance.save()

        

