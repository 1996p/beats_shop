from django.urls import path
from .api_views import *

urlpatterns = [
    path('v1/productlist/', ProductAPIView.as_view()),
    path('v1/product/<int:pk>/', ProductAPIView.as_view()),

]
