from django.core.validators import MinValueValidator
from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=200)
    venue = models.CharField(max_length=100, default=None)
    is_in_messenger = models.BooleanField(default=False)
    is_payment_partial = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Product(models.Model):

    name = models.CharField(max_length=200)
    price = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    event = models.ForeignKey(Event, on_delete=models.CASCADE, default=1)
    total_sold = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Shop(models.Model):
    name = models.CharField(max_length=200)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, default=1)
    products = models.ManyToManyField(Product, through='ShopINProduct')
    venue = models.CharField(default=None, max_length=100, null=True, blank=True)
    is_in_messenger = models.BooleanField(default=False, null=True, blank=True)
    is_payment_partial = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.name


class ShopINProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=1)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, default=1)
    price = models.IntegerField(default=None, validators=[MinValueValidator(0)], null=True, blank=True)
    quantity = models.IntegerField(default=None, validators=[MinValueValidator(0)], null=True, blank=True)
    total_sold = models.IntegerField(default=0)

    # @property
    # def current_price(self):
    #     if self.price is None:
    #         return self.product.price
    #     return self.price