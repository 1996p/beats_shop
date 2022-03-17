from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ValidationError
from django.db.models import F
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, View, DetailView, ListView
from django.contrib.auth import logout, login
from .forms import *
from .models import *
from django.shortcuts import render
from django.template import RequestContext

# Create your views here.

class Index(ListView):
    template_name = 'homepage.html'
    context_object_name = 'products'
    model = Product
    queryset = Product.objects.all().order_by('-published')[:4]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            cart = Cart.objects.get(owner=SiteUser.objects.get(user=self.request.user))
            context['cart_length'] = cart.cartproduct_set.count()
        except Exception:
            pass
        return context

def test(request):
    product_val = Product.objects.values('title', 'actual_price')

    return redirect('home')


class AuthenticationView(LoginView):
    template_name = 'loginpage.html'
    form_class = UserAuthentication


class RegisterView(CreateView):
    template_name = 'registerpage.html'
    form_class = UserRegister
    success_url = '/'

    def form_valid(self, form):
        user = form.save()
        newSiteUser = SiteUser.objects.create(user=user, contentMakerStatus=False)
        newSiteUser.save()
        login(self.request, user)
        return redirect('home')


class AddProduct(CreateView):
    template_name = 'add-product.html'
    form_class = AddProductForm
    success_url = '/'
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['access'] = SiteUser.objects.get(user=self.request.user).contentMakerStatus
        except:
            context['access'] = False

        return context


class MakeDiscountView(View):
    def get(self, request, *args, **kwargs):
        try:
            product = Product.objects.get(pk=kwargs['id'])
        except:
            raise Http404
        form = MakeDiscountForm(request.POST or None)
        context = {'product': product,
                   'form': form}
        return render(request, 'discount.html', context)

    def post(self, request, *args, **kwargs):
        try:
            product = Product.objects.get(pk=kwargs['id'])
        except:
            raise Http404
        form = MakeDiscountForm(request.POST or None)

        context = {'product': product,
                   'form': form
                   }

        if form.is_valid():
            product.old_price = product.actual_price
            product.actual_price = form.cleaned_data['new_price']

            if form.cleaned_data['make_discount'] and product.actual_price < product.old_price:
                product.sale_status = True
            else:
                product.sale_status = False

            product.save()
            return redirect('/')

        return render(request, 'discount.html', context)


class DetailedView(View):
    def get(self, request, *args, **kwargs):

        try:
            product = Product.objects.get(pk=kwargs['id'])
        except:
            raise Http404
        try:
            author = SiteUser.objects.get(user=request.user)
        except:
            author = AnonymousUser()
        comments = Commentary.objects.filter(product=product)
        if len(comments) == 0:
            have_comments = False
        else:
            have_comments = True

        form = AddCommentaryForm()
        is_anonymous = isinstance(request.user, AnonymousUser)
        context = {
                    'id': kwargs['id'],
                    'product': product,
                    'author': author,
                    'comments': comments,
                    'have_comments': have_comments,
                    'form': form,
                    'is_anonymous': is_anonymous,
                    }

        return render(request, 'detailed_product.html', context)

    def post(self, request, *args, **kwargs):
        if not isinstance(request.user, AnonymousUser):
            form = AddCommentaryForm(request.POST or None)
            if form.is_valid():
                new_comment = Commentary.objects.create(
                    author=SiteUser.objects.get(user=request.user),
                    product=Product.objects.get(pk=kwargs['id']),
                    content=form.cleaned_data['content'],
                )

                new_comment.save()

            return redirect(request.path)
        else:
            print(type(request.user))
            return redirect('/')


class MyCabinet(View):
    def get(self, request, *agrs, **kwargs):
        try:
            site_user = SiteUser.objects.get(user=request.user)
            user = site_user.user
        except:
            return redirect('/')

        if site_user.image:
            profile_image_url = site_user.image.url
        else:
            profile_image_url = '#'

        if user.is_superuser:
            request_list = GetSellerStatusRequest.objects.filter(
                request_status=GetSellerStatusRequest.RequestStatus.not_checked
            )
        else:
            request_list = None

        context = {
            'site_user': site_user,
            'user': user,
            'profile_image_url': profile_image_url,
            'request_list': request_list,
        }

        return render(request, 'cabinet.html', context=context)

    def post(self, request, *args, **kwargs):
        pass


class MyCabinetChange(View):
    def get(self, request, *args, **kwargs):
        try:
            site_user = SiteUser.objects.get(user=request.user)
            user = site_user.user
        except:
            return redirect('/')
        form = MyCabinetChangeForm({
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'username': user.username,

        })

        context = {
            'form': form,
        }

        return render(request, 'cabinet-change.html', context=context)


    def post(self, request, *args, **kwargs):

        try:
            site_user = SiteUser.objects.get(user=request.user)
            user = site_user.user
        except:
            return redirect('/')

        form = MyCabinetChangeForm(request.POST, request.FILES)

        if form.is_valid():
            new_username = form.cleaned_data['username']
            new_first_name = form.cleaned_data['first_name']
            new_last_name = form.cleaned_data['last_name']
            new_email = form.cleaned_data['email']

            if form.cleaned_data['image'] is not None:
                new_profile_image = form.cleaned_data['image']
                site_user.image = new_profile_image

            user.username = new_username
            user.first_name = new_first_name
            user.last_name = new_last_name
            user.email = new_email

            user.save()
            site_user.save()

            return redirect('/my')


        return redirect('/')


class GetSellerStatusRequestView(View):
    def get(self, request, *args, **kwargs):
        seller_request = GetSellerStatusRequest.objects.get(pk=kwargs['pk'])

        return render(request, 'seller-request.html', {})

    def post(self, request, *args, **kwargs):

        return render(request, 'seller-request.html', {})


def SellerRequestAccept(request, pk):
    seller_request = GetSellerStatusRequest.objects.get(pk=pk)
    seller_request.request_status = GetSellerStatusRequest.RequestStatus.accepted

    requester = seller_request.requester
    requester.contentMakerStatus = True

    requester.save()
    seller_request.save()

    return redirect('/my')


def SellerRequestDeny(request, pk):
    seller_request = GetSellerStatusRequest.objects.get(pk=pk)
    seller_request.request_status = GetSellerStatusRequest.RequestStatus.denied

    seller_request.save()

    return redirect('/my')


def MakeSellerRequest(request):
    requester = SiteUser.objects.get(user=request.user)
    new_seller_request = GetSellerStatusRequest.objects.get_or_create(requester=requester)
    print(new_seller_request)
    new_seller_request[0].save()
    return redirect('/my')


def view404(request, exception):
    response = render(request, 'error404page.html', {})
    return response


def LogoutUser(request):
    logout(request)
    return redirect('/')


class AllProduct(ListView):
    model = Product
    template_name = 'all-products.html'
    queryset = Product.objects.all()
    context_object_name = 'products'


class CategoriesView(ListView):
    model = Category
    template_name = 'all-categories.html'
    context_object_name = 'categories'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        print(context)
        return context


class CategoryView(ListView):
    template_name = 'category.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(category=self.kwargs['pk'])


class CartView(ListView):
    model = Cart
    template_name = 'cart.html'
    context_object_name = 'cart_products'

    def get_queryset(self):
        try:
            cart = Cart.objects.get_or_create(owner=SiteUser.objects.get(user=self.request.user))[0]
            cart_products = cart.cartproduct_set.all()
            for cart_product in cart_products:
                cart_product.save()
        except Exception:
            cart_products = None
        return cart_products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart.objects.get_or_create(owner=SiteUser.objects.get(user=self.request.user))[0]
        cart_length = cart.cartproduct_set.count
        cart.save()
        context['cart'] = cart
        context['cart_length'] = cart_length
        return context


class AddToCartView(View):
    def get(self, request, *args, **kwargs):
        user = SiteUser.objects.get(user=request.user)
        cart = Cart.objects.get_or_create(owner=user)
        cart[0].save()
        product = Product.objects.get(pk=kwargs['id'])
        cart_product, created = CartProduct.objects.get_or_create(product=product, cart=cart[0])
        if not created:
            cart_product.qty += 1
        cart_product.save()
        
        return redirect('cart')


class IncreaseQty(View):
    def get(self, request, *args, **kwargs):
        cart = Cart.objects.get(owner=SiteUser.objects.get(user=request.user))
        cart_product = cart.cartproduct_set.get(pk=kwargs['id'])
        cart_product.qty += 1
        cart_product.save()
        cart.save()
        return redirect('cart')


class ReduceQty(View):
    def get(self, request, *args, **kwargs):
        cart = Cart.objects.get(owner=SiteUser.objects.get(user=request.user))
        cart_product = cart.cartproduct_set.get(pk=kwargs['id'])
        cart_product.qty -= 1

        if cart_product.qty == 0:
            cart_product.delete()
            cart.save()
            return redirect('cart')
        cart_product.save()
        cart.save()
        return redirect('cart')













