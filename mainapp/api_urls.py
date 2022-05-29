from django.urls import path, include
from rest_framework import routers
from .api_views import *


router = routers.SimpleRouter()
router.register(r'products', ProductViewSet)


urlpatterns = [
    # path('v1/productlist/', ProductAPIView.as_view()),
    # path('v1/product/<int:pk>/', ProductAPIView.as_view()),
    path('v1/', include(router.urls))

]
