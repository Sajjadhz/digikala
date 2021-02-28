from django.shortcuts import render
from django.views.generic import TemplateView

from order.models import BasketItem, Basket
from product.models import Category, Product
from .models import SlideShow
# Create your views here.


class HomeView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slides'] = SlideShow.objects.all()
        context['categories'] = Category.objects.all()
        context['products'] = list(map(self.get_min_price, Product.objects.all()))
        if self.request.user.is_authenticated:
            context['basket'] = self.get_basket_basket_items()[0]
            context['basket_items'] = self.get_basket_basket_items()[1]
        return context

    def get_min_price(self, product):
        min_price = min(item.price for item in product.shop_product.all())
        print("min_price : ", min_price)
        return [product, min_price]

    def get_basket_basket_items(self):
        if self.request.user.is_authenticated:
            basket = Basket.objects.get(user=self.request.user)
            basket_items = BasketItem.objects.filter(basket__user=self.request.user)
            basket.total_price = self.get_basket_total_price(basket_items)
            basket.save()
            return [basket, basket_items]
        elif Basket.objects.get(user=self.request.user.is_anonymous):
            basket = Basket.objects.get(user=self.request.user.is_anonymous)
            basket_items = BasketItem.objects.filter(basket__user=self.request.user.is_anonymous)
            basket.total_price = self.get_basket_total_price(basket_items)
            basket.save()
            return [basket, basket_items]
        else:
            basket = Basket.objects.create(user=self.request.user.is_anonymous)
            basket_items = []
            basket.total_price = self.get_basket_total_price(basket_items)
            basket.save()
            return [basket, basket_items]

    def get_basket_total_price(self, basket_items):
        total_price = 0
        for i in basket_items:
            total_price += i.total
        return total_price