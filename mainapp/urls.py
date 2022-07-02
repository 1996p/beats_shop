from django.contrib import admin
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', Index.as_view(), name='home'),
    path('product/<int:id>/', DetailedView.as_view(), name='detailedView'),
    path('login/', AuthenticationView.as_view(), name='login_main'),
    path('logout/', LogoutUser, name='logout_main'),
    path('register/', RegisterView.as_view(), name='register_main'),
    path('add-product/', AddProduct.as_view(), name='add-product'),
    path('product/<int:id>/discount/', MakeDiscountView.as_view(), name='make-discount'),
    path('my/', MyCabinet.as_view(), name='my-cabinet'),
    path('my/change', MyCabinetChange.as_view(), name='my-cabinet-change'),
    path('work/request/<int:pk>/', GetSellerStatusRequestView.as_view(), name='get-seller-status-request'),
    path('work/request/<int:pk>/accept', SellerRequestAccept, name='seller-request-accept'),
    path('work/request/<int:pk>/deny', SellerRequestDeny, name='seller-request-deny'),
    path('my/get-seller-status/', MakeSellerRequest, name='make-seller-request'),
    path('all-products/', AllProduct.as_view(), name='all-products'),
    path('categories/', CategoriesView.as_view(), name='all-categories'),
    path('category/<int:pk>/', CategoryView.as_view(), name='category'),
    path('my-cart/', CartView.as_view(), name='cart'),
    path('my-cart/payment/', CartView.as_view(), name='payment'),
    path('add-to-card/<int:id>/', AddToCartView.as_view(), name='add-to-cart'),
    path('my-cart/increase/<int:id>', IncreaseQty.as_view(), name='increase-qty'),
    path('my-cart/reduce/<int:id>', ReduceQty.as_view(), name='reduce-qty'),
    path('test/', test, name='test-view')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


