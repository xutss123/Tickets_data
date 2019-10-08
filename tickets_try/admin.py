from django.contrib import admin

from .models import Shop, Product, Event

# Register your models here.
admin.site.register(Shop)
admin.site.register(Product)
admin.site.register(Event)