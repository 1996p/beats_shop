from django.urls import path
from .api_views import *

urlpatterns = [
    path('v1/productlist/', ProductAPIView.as_view()),

]
