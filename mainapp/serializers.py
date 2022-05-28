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
    published = serializers.BooleanField(default=True)


# class ProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = ('title', 'actual_price')
