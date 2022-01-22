from django.contrib import admin

# Register your models here.

# データベースの読み込み
from .models import Customer

admin.site.register(Customer)
