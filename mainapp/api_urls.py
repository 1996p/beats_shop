from django.urls import path, include
from rest_framework import routers
from .api_views import *


urlpatterns = [
    path('v1/productlist/', ProductListView.as_view()),
    path('v1/productupdate/<int:pk>/', ProductUpdateView.as_view()),
    path('v1/productdelete/<int:pk>/', ProductDeleteView.as_view())

]
