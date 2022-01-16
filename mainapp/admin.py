from django.contrib import admin
from .models import *


# Register your models here.

admin.site.register(Product)
admin.site.register(SiteUser)
admin.site.register(Cart)
admin.site.register(Commentary)
admin.site.register(GetSellerStatusRequest)