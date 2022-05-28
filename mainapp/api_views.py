from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from .models import *
from .serializers import *
from rest_framework import generics


class ProductAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()

        return Response({'products': ProductSerializer(products, many=True).data})

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_data = ProductSerializer(request.data).data
        product = Product.objects.create(
            title=new_data['title'],
            description=new_data['description'],
            actual_price=new_data['actual_price'],
            old_price=new_data['old_price'],
            sale_status=new_data['sale_status'],
            author=SiteUser.objects.get(user__username=request.data['author']),
            image=new_data['image'],
            category=Category.objects.get(name=request.data['category']),
            published=new_data['published']
        )

        product.save()
        return Response(ProductSerializer(product).data)