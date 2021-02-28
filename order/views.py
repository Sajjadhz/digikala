import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, CreateView

from order.models import BasketItem, Basket, Order, OrderItem
from product.models import Category, Product, ShopProduct


class CartView(TemplateView):
    template_name = "order/cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['products'] = Product.objects.all()
        context['basket'] = self.get_basket_basket_items()[0]
        context['basket_items'] = self.get_basket_basket_items()[1]
        return context

    def get_basket_total_price(self, basket_items):
        total_price = 0
        for basket_item in basket_items:
            total_price += basket_item.total
        return total_price

    def get_basket_basket_items(self):
        if self.request.user.is_authenticated:
            basket = Basket.objects.filter(user=self.request.user)
            basket_items = BasketItem.objects.filter(basket__user=self.request.user)
            basket.total_price = self.get_basket_total_price(basket_items)
            basket.save()
            return [basket, basket_items]
        elif Basket.objects.filter(user=self.request.user.is_anonymous):
            basket = Basket.objects.filter(user=self.request.user.is_anonymous)
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


class ZarrinPallView(TemplateView):
    template_name = "order/zarrin_pall.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['products'] = Product.objects.all()
        context['basket_items'] = BasketItem.objects.filter(basket__user=self.request.user)
        if Order.objects.filter(draft=True):
            order = Order.objects.filter(draft=True).first()
        else:
            order = Order.objects.create(user=self.request.user)
        context['order_items'] = self.create_order_items(BasketItem.objects.filter(basket__user=self.request.user), order)
        basket = Basket.objects.get(user=self.request.user)
        basket.total_price = 0
        basket.save()
        order.total_price = self.get_basket_total_price(OrderItem.objects.filter(order__id=order.id))
        order.draft = False
        order.save()
        context['order'] = order
        context['basket'] = basket
        context['basket_items'] = BasketItem.objects.filter(basket__user=self.request.user)
        return context

    def get_basket_total_price(self, order_items):
        total_price = 0
        for order_item in order_items:
            total_price += order_item.total
        return total_price

    def create_order_items(self, basket_items, order):
        order_items = []
        for basket_item in basket_items:
            order_items.append(OrderItem.objects.create(order=order, shop_product=basket_item.shop_product, quantity=
                                basket_item.quantity, price=basket_item.price, total=basket_item.total))
            shop_product = ShopProduct.objects.get(basket_item=basket_item)
            print('basket_item_quantity : ', basket_item.quantity)
            print('basket_item : ', basket_item)
            print('shop_product : ', shop_product)
            print('shop_product quantity : ', shop_product.quantity)
            shop_product.quantity -= basket_item.quantity  # basket_item quantity must check smaller than shop_product quantity
            shop_product.save()
            basket_item.delete()
        return order_items


def get_basket_total_price(basket_items):
    total_price = 0
    for basket_item in basket_items:
        total_price += basket_item.total
    return total_price


@csrf_exempt
def create_basket_item(request):
    data = json.loads(request.body)
    try:
        basket_item = BasketItem.objects.get(basket_id=data['basket_id'], shop_product_id=data['shop_product_id'])
        basket_item.quantity += int(data['quantity'])
        basket_item.total = int(data['price']) * int(basket_item.quantity)
        basket_item.save()
        basket_item_count = BasketItem.objects.filter(basket__user=request.user).count()
        basket_total_price = get_basket_total_price(BasketItem.objects.filter(basket__user=request.user))
        basket = Basket.objects.get(user=request.user)
        basket.total_price = basket_total_price
        basket.save()
        response = {"mode": 1, "slug": basket_item.shop_product.product.slug,
                    'product_name': basket_item.shop_product.product.name,
                    'quantity': basket_item.quantity, "price": basket_item.price,
                    "basket_item_id": basket_item.id, "basket_item_count": basket_item_count,
                    'basket_total_price': basket_total_price}
        return HttpResponse(json.dumps(response), status=201)
    except:
        try:
            total = int(data['price']) * int(data['quantity'])
            print("total : ", total)
            basket_item = BasketItem.objects.create(basket_id=data['basket_id'],
                                                    shop_product_id=data['shop_product_id'],
                                                    quantity=data['quantity'], price=data['price'], total=total)
            basket_item_count = BasketItem.objects.filter(basket__user=request.user).count()
            basket_total_price = get_basket_total_price(BasketItem.objects.filter(basket__user=request.user))
            basket = Basket.objects.get(user=request.user)
            basket.total_price = basket_total_price
            basket.save()
            response = {"mode": 0, "slug": basket_item.shop_product.product.slug,
                        'product_name': basket_item.shop_product.product.name,
                        'quantity': basket_item.quantity, "price": basket_item.price,
                        "basket_item_id": basket_item.id, "basket_item_count": basket_item_count,
                        'basket_total_price': basket_total_price}
            return HttpResponse(json.dumps(response), status=201)
        except:
            response = {'error': 'Error'}
            print("error")
            return HttpResponse(json.dumps(response), status=400)


@csrf_exempt
def remove_basket_item(request):
    data = json.loads(request.body)
    try:
        BasketItem.objects.get(id=data['basket_item_id']).delete()
        basket_item_count = BasketItem.objects.filter(basket__user=request.user).count()
        basket_total_price = get_basket_total_price(BasketItem.objects.filter(basket__user=request.user))
        basket = Basket.objects.get(user=request.user)
        basket.total_price = basket_total_price
        basket.save()
        response = {'basket_item_id': data['basket_item_id'], "basket_item_count": basket_item_count,
                    'basket_total_price': basket_total_price}
        return HttpResponse(json.dumps(response), status=201)
    except:
        response = {'error': 'Error'}
        return HttpResponse(json.dumps(response), status=400)


@csrf_exempt
def update_basket_item(request):
    data = json.loads(request.body)
    try:
        basket_item = BasketItem.objects.get(id=data['basket_item_id'])
        basket_item.quantity += int(data['mode'])
        basket_item.total = int(basket_item.quantity) * int(basket_item.price)
        basket_item.save()
        basket_total_price = get_basket_total_price(BasketItem.objects.filter(basket__user=request.user))
        basket = Basket.objects.get(user=request.user)
        basket.total_price = basket_total_price
        basket.save()
        print('basket_total_price: ', basket_total_price)
        response = {'basket_item_id': data['basket_item_id'], 'basket_item_quantity': basket_item.quantity,
                    'basket_total_price': basket_total_price, 'basket_item_total_price': basket_item.total}
        return HttpResponse(json.dumps(response), status=201)
    except:
        response = {'error': 'Error'}
        return HttpResponse(json.dumps(response), status=400)
