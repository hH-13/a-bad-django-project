from django.contrib import admin
from django.db import models

from .models import Client, Item, OrderItem, Type, made_by

# Register your models here
admin.site.register(Type)
admin.site.register(Item)
admin.site.register(Client)
admin.site.register(OrderItem)
admin.site.register(made_by)
