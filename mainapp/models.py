from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(max_length=128, verbose_name="Категория товара")

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=40, verbose_name='Название')
    description = models.TextField(max_length=255, verbose_name='Описание')
    actual_price = models.PositiveIntegerField(verbose_name='Актуальная цена')
    old_price = models.PositiveIntegerField(verbose_name='Старая цена', blank=True, null=True)
    author = models.ForeignKey('SiteUser', on_delete=models.CASCADE, blank=True, null=True)
    sale_status = models.BooleanField(verbose_name='Наличие скидки', blank=True, null=True)
    image = models.ImageField(verbose_name='Изображение', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="Категория товара", null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detailedView', kwargs={'id': self.pk})

class SiteUser(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    contentMakerStatus = models.BooleanField(verbose_name='Статус продавца')
    image = models.ImageField(blank=True, null=True, verbose_name='Аватар')

    '''TODO'''

    def __str__(self):
        return self.user.username

class CartProduct(models.Model):
    pass


class Cart(models.Model):
    owner = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)

class Commentary(models.Model):
    author = models.ForeignKey(SiteUser, on_delete=models.CASCADE, verbose_name='Автор комментария')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    content = models.TextField(max_length=3000, verbose_name='Содержание')
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата написания комментария')
    update_date = models.DateTimeField(auto_now=True, verbose_name='Дата изменения комментария')

    def __str__(self):
        return f'{str(self.product)} : {self.content[:50]}'


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

