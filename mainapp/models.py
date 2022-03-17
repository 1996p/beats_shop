from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from decimal import Decimal

class Category(models.Model):
    name = models.CharField(max_length=128, verbose_name="Категория товара")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Категории'
        verbose_name = 'Категория'


class Product(models.Model):
    title = models.CharField(max_length=40, verbose_name='Название')
    description = models.TextField(max_length=255, verbose_name='Описание')
    actual_price = models.PositiveIntegerField(verbose_name='Актуальная цена')
    old_price = models.PositiveIntegerField(verbose_name='Старая цена', blank=True, null=True)
    author = models.ForeignKey('SiteUser', on_delete=models.CASCADE, blank=True, null=True)
    sale_status = models.BooleanField(verbose_name='Наличие скидки', blank=True, null=True)
    image = models.ImageField(verbose_name='Изображение', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="Категория товара", null=True)
    published = models.DateTimeField(verbose_name='Дата публикации', auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detailedView', kwargs={'id': self.pk})

    class Meta:
        verbose_name_plural = 'Товары'
        verbose_name = 'Товар'


class SiteUser(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    contentMakerStatus = models.BooleanField(verbose_name='Статус продавца')
    image = models.ImageField(blank=True, null=True, verbose_name='Аватар')

    '''TODO'''

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Пользователи(extended)'
        verbose_name = 'Пользователь(extended)'


class CartProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='Товар', null=True)
    qty = models.PositiveIntegerField(verbose_name='Количество', default=1)
    final_price = models.DecimalField(decimal_places=2, max_digits=30, verbose_name="Общая цена", default=0)
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        self.final_price = Decimal(self.qty) * Decimal(self.product.actual_price)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.title} | qty {self.qty} |cart {self.cart.owner.user.username}"

    class Meta:
        verbose_name_plural = 'Товары из корзины'
        verbose_name = 'Товар из корзины'


class Cart(models.Model):
    owner = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    # products = models.ManyToManyField(CartProduct)
    final_price = models.DecimalField(decimal_places=2, max_digits=30, verbose_name="Итого к оплате", default=0)
    total_product = models.PositiveIntegerField(verbose_name='Всего товаров', default=0)

    def save(self, *args, **kwargs):
        self.final_price = 0
        self.total_product = 0
        for cart_product in self.cartproduct_set.all():
            self.total_product += cart_product.qty
            self.final_price += Decimal(cart_product.final_price)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'Владелец - {self.owner.user.username} | cart id - {self.pk}'

    class Meta:
        verbose_name_plural = 'Корзины'
        verbose_name = 'Корзина'


class Commentary(models.Model):
    author = models.ForeignKey(SiteUser, on_delete=models.CASCADE, verbose_name='Автор комментария')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    content = models.TextField(max_length=3000, verbose_name='Содержание')
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата написания комментария')
    update_date = models.DateTimeField(auto_now=True, verbose_name='Дата изменения комментария')

    def __str__(self):
        return f'{str(self.product)} : {self.content[:50]}'

    class Meta:
        verbose_name_plural = 'Комментарии'
        verbose_name = 'Комментарий'


class GetSellerStatusRequest(models.Model):
    class RequestStatus(models.TextChoices):
        accepted = 'AC', _('ACCEPTED')
        denied = 'DN', _('DENIED')
        not_checked = 'NC', _('NOT CHECKED')

    requester = models.ForeignKey(SiteUser, on_delete=models.CASCADE, verbose_name='Запросивший статус')
    commentary = models.CharField(max_length=1000, verbose_name='Комментарий к заявке', blank=True, null=True)
    request_status = models.CharField(max_length=2, choices=RequestStatus.choices, default=RequestStatus.not_checked, verbose_name='Состояние заявки')
    request_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата написания заявки')

    def __str__(self):
        return f'{str(self.requester)} | {self.request_status}'

    class Meta:
        unique_together = ('request_date', 'requester')

