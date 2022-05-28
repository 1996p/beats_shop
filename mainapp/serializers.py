from rest_framework import serializers
from .models import *


class ProductSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=60)
    description = serializers.CharField(max_length=255)
    actual_price = serializers.IntegerField()
    old_price = serializers.IntegerField(default=None)
    author = serializers.CharField()
    sale_status = serializers.BooleanField(default=False)
    image = serializers.ImageField(default=None)
    category = serializers.CharField()

    def create(self, validated_data):
        return Product.objects.create(
            title=validated_data['title'],
            description=validated_data['description'],
            actual_price=validated_data['actual_price'],
            old_price=validated_data['old_price'],
            sale_status=validated_data['sale_status'],
            author=SiteUser.objects.get(user__username=validated_data['author']),
            image=validated_data['image'],
            category=Category.objects.get(name=validated_data['category']),
        )

    def update(self, instance: Product, validated_data: dict):
        category = Category.objects.get(name=validated_data.get('category'))
        author = SiteUser.objects.get(user__username=validated_data.get('author'))

        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.actual_price = validated_data.get('actual_price', instance.actual_price)
        instance.old_price = validated_data.get('old_price', instance.old_price)
        instance.sale_status = validated_data.get('sale_status', instance.sale_status)
        instance.author = author if author else instance.author
        instance.image = validated_data.get('image', instance.image)
        instance.category = category if category else instance.category
        print(instance.actual_price)
        instance.save()

        return instance

