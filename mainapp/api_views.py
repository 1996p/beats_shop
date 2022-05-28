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
        serializer.save()

        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)

        if not pk:
            return Response({'error': 'Method is not allowed'})

        try:
            product = Product.objects.get(pk=pk)
        except Exception:
            return Response({'error': 'Product with same PK doesn\'t exist'})

        serializer = ProductSerializer(instance=product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'product': serializer.data})

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)

        if not pk:
            return Response({'error': 'Method is not allowed'})

        try:
            product = Product.objects.get(pk=pk)
        except Exception:
            return Response({'error': 'Product with same PK doesn\'t exist'})

        product.delete()

        return Response({'deleted': f'product {product.title}'})


