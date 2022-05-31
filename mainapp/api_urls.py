import djoser
from django.urls import path, include, re_path
from rest_framework import routers
from .api_views import *


urlpatterns = [
    path('v1/productlist/', ProductListView.as_view()),
    path('v1/productupdate/<int:pk>/', ProductUpdateView.as_view()),
    path('v1/productdelete/<int:pk>/', ProductDeleteView.as_view()),
    path('v1/auth', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken'))

]
