from django.shortcuts import render, redirect
from django.views import View
from .models import Event, Shop, Product, ShopINProduct
from .forms import ProductForm, EventForm, ShopForm, ShopProductForm

# Create your views here.


class FormView(View):

    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        event_list = Event.objects.all()
        return render(request, template_name=self.template_name,
                      context={'event_form': EventForm, 'event_list': event_list})

    def post(self, request, *args, **kwargs):
        form_event = EventForm(data=request.POST)
        if form_event.is_valid():
            event_new = form_event.data.get('name')
            form_event.save()
            _event = Event.objects.get(name=event_new).id
            return redirect('tickets_app:start', _event)
        else:
            event_list = Event.objects.all()
            return render(request, template_name=self.template_name,
                          context={'event_form': EventForm, 'event_list': event_list})


class CongratsView(View):

    template_name = 'congrats.html'

    def get(self, request, event_id, *args, **kwargs):
        _event = Event.objects.get(pk=event_id)
        return render(request, template_name=self.template_name, context={'event': _event})


class ShopView(View):
    template_name = 'shop.html'

    def get(self, request, event_id,  *args, **kwargs):
        shop_list = Shop.objects.filter(event_id=event_id)
        _event = Event.objects.get(pk=event_id)
        for field in Shop._meta.fields:
            for shop in shop_list:
                if getattr(shop, field.name) is None:
                    setattr(shop, field.name, getattr(_event, field.name))

        return render(request, template_name=self.template_name,
                      context={'shop_form': ShopForm, 'event': _event, 'shop_list': shop_list})

    def post(self, request, *args, **kwargs):
        form_shop = ShopForm(data=request.POST)
        if form_shop.is_valid():
            _event = Event.objects.get(pk=form_shop.data.get('event'))
            form_shop.save()
        
        return redirect('tickets_app:shop', _event.id)


class ProductView(View):
    def get(self, request, event_id, *args, **kwargs):
        product_list = Product.objects.filter(event=event_id)
        _event = Event.objects.get(pk=event_id)
        return render(request, template_name='ticket.html',
                      context={'product_form': ProductForm,
                               'event': _event,
                               'product_list': product_list})

    def post(self, request, *args, **kwargs):
        form_product = ProductForm(data=request.POST)
        _event = Event.objects.get(pk=form_product.data.get('event'))
        product_list = Product.objects.filter(event=_event)
        if form_product.is_valid():
            form_product.save()
        return render(request, template_name='ticket.html',
                    context={'product_form': ProductForm,
                    'event': _event,
                    'product_list': product_list})


class Overview(View):
    template_name = 'overview.html'

    def get(self, request, event_id, *args, **kwargs):
        _event = Event.objects.get(pk=event_id)
        shops = Shop.objects.filter(event_id=event_id)
        shop_product_list = ShopINProduct.objects.all()
        return render(request, template_name=self.template_name,
                      context={'shop_list': shops, 'event': _event, 'shop_product_list': shop_product_list})


class AddShopToProductView(View):
    template_name = 'shopproduct.html'

    def get(self, request, event_id, *args, **kwargs):
        return render(request, template_name=self.template_name,
                      context={'event': event_id,
                               'shop_product_form': ShopProductForm(event_id=event_id)})

    def post(self, request, event_id, *args, **kwargs):
        shop_product_form = ShopProductForm(data=request.POST, event_id=event_id)
        if shop_product_form.is_valid():
            shop_product_form.save()
        return render(request, template_name=self.template_name,
                      context={'event': event_id,
                               'shop_product_form': shop_product_form})


class SellTickets(View):
    template_name = 'sell.html'

    def get(self, request, shop_id, *args, **kwargs):
        ticket_list = ShopINProduct.objects.filter(shop_id=shop_id)
        for field in ShopINProduct._meta.fields:
            for product in ticket_list:
                _product = Product.objects.get(pk=product.product_id)
                if getattr(product, field.name) is None:
                    setattr(product, field.name, getattr(_product, field.name))
        return render(request, template_name=self.template_name, context={'ticket_list': ticket_list})

    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('id')
        product = ShopINProduct.objects.get(product_id=product_id)
        _product = Product.objects.get(pk=product_id)
        buy_amount = request.POST.get('quantity')
        if product.quantity is None:
            if _product.quantity - _product.total_sold > int(buy_amount):
                self.substract(_product, buy_amount, product)
        else:
            if product.quantity - product.total_sold > int(buy_amount):
                self.substract(_product, buy_amount, product)

        return redirect('tickets_app:start', 23)

    def substract(self, _product, buy_amount, product):
        product.total_sold += int(buy_amount)
        _product.total_sold += int(buy_amount)
        product.save()
        _product.save()


