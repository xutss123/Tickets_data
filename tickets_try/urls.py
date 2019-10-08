from django.urls import path

from . import views

app_name = 'tickets_app'

urlpatterns = [

    path('congrats/<event_id>', views.CongratsView.as_view(), name='start'),
    path('shop/<event_id>', views.ShopView.as_view(), name='shop'),
    path('pair/<event_id>', views.AddShopToProductView.as_view(), name='pair'),
    path('', views.FormView.as_view(), name='index'),
    path('ticket/<event_id>', views.ProductView.as_view(), name='ticket'),
    path('overview/<event_id>', views.Overview.as_view(), name='finally'),
    path('sell/<shop_id>', views.SellTickets.as_view(), name='sell'),
]