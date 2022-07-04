from .models import *


class ContextMixin:
    def get_user_context(self, request,):
        try:
            cart = Cart.objects.get_or_create(owner=SiteUser.objects.get(user=request.user))[0]
            cart_products = cart.cartproduct_set.all()
            if cart_products:
                for cart_product in cart_products:
                    cart_product.save()
            else:
                cart_products = None

        except Exception:
            cart_products = None

        context = {
            'cart_length': cart_products.count(),
            'bonus_balance': SiteUser.objects.get(user=request.user).bonus_balance,
        }

        return context