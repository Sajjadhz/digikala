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
        context['products'] = Product.objects.all()
        context['basket'] = Basket.objects.filter(user=self.request.user)
        context['basket_items'] = BasketItem.objects.filter(basket__user=self.request.user)
        context['total_price'] = 0
        for i in context['basket_items']:
            context['total_price'] += i.price
        return context
