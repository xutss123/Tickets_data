from django import forms
from django.db.models import Sum

from .models import Product, Event, Shop, ShopINProduct


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['name', 'quantity', 'price', 'event']
        widgets = {
            'event': forms.HiddenInput()
        }


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ['name', 'venue', 'is_in_messenger', 'is_payment_partial']


class ShopForm(forms.ModelForm):

    class Meta:
        model = Shop
        fields = ['name', 'event', 'venue', 'is_in_messenger', 'is_payment_partial']
        widgets = {
            'event': forms.HiddenInput()
        }


class ShopProductForm(forms.ModelForm):

    def __init__(self, event_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        products = Product.objects.filter(event_id=event_id)

        self.fields['product'].queryset = products
        self.fields['shop'].queryset = Shop.objects.filter(event_id=event_id)

    class Meta:
        model = ShopINProduct
        fields = ['product', 'shop', 'price', 'quantity']

    def clean(self):
        clean_data = super().clean()
        counted_amounts = ShopINProduct.objects.filter(product=clean_data.get('product')).aggregate(Sum('quantity'))

        if clean_data.get('quantity') is not None:
            if counted_amounts.get('quantity__sum') is None:
                counted_amounts['quantity__sum'] = 0
            if counted_amounts.get('quantity__sum') > clean_data.get('product').quantity:
                self.errors['quantity'] = ['Max amount reached']
            elif counted_amounts.get('quantity__sum') + clean_data['quantity'] > clean_data.get('product').quantity:
                self.errors['quantity'] = ['Max amount reached']
        return clean_data
