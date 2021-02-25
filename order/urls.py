from django.urls import path

from order.views import CartView, create_basket_item, remove_basket_item, update_basket_item, ZarrinPallView

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('zarrin_pall/', ZarrinPallView.as_view(), name='zarrin_pall'),
    path('creat_basket_item/', create_basket_item, name='create_basket_item'),
    path('remove_basket_item/', remove_basket_item, name='remove_basket_item'),
    path('update_basket_item/', update_basket_item, name='update_basket_item'),
]