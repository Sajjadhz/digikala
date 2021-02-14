import json

from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView
from django.db.models import Q
from django.views.generic.edit import FormMixin

from order.models import BasketItem, Basket
from product.forms import CommentForm
from product.models import Category, Product, ProductImage, ShopProduct, Comment, CommentLike


# Create your views here.


class SubCategoryDetailView(DetailView):
    model = Category
    template_name = "product/sub_category.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(slug=self.kwargs['slug'])
        context['products'] = Product.objects.filter(category=kwargs['object'])
        context['basket_items'] = BasketItem.objects.filter(basket__user=self.request.user)
        # context['shop_products'] = ShopProduct.objects.filter(product=kwargs['object'])
        # context['average_shop_products'] = sum(item.price for item in context['shop_products']) / len(
        #     [item.price for item in context['shop_products']])
        context['categories'] = Category.objects.all()
        basket = Basket.objects.get(user=self.request.user)
        basket.total_price = self.get_basket_total_price(context['basket_items'])
        basket.save()
        context['basket'] = basket
        return context

    def get_basket_total_price(self, basket_items):
        total_price = 0
        for basket_item in basket_items:
            total_price += basket_item.total
        return total_price


class CategoryDetailView(DetailView):
    model = Category
    template_name = "product/category.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(slug=self.kwargs['slug'])
        context['child_categories'] = Category.objects.filter(parent=context['category'])
        context['basket_items'] = BasketItem.objects.filter(basket__user=self.request.user)
        context['categories'] = Category.objects.all()
        basket = Basket.objects.get(user=self.request.user)
        basket.total_price = self.get_basket_total_price(context['basket_items'])
        basket.save()
        context['basket'] = basket
        return context

    def get_basket_total_price(self, basket_items):
        total_price = 0
        for basket_item in basket_items:
            total_price += basket_item.total
        return total_price


class ProductDetailView(FormMixin, DetailView):
    model = Product
    template_name = "product/product-detail.html"
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = Product.objects.get(slug=self.kwargs['slug'])
        context['product_images'] = ProductImage.objects.filter(product=kwargs['object'])
        context['shop_products'] = ShopProduct.objects.filter(product=kwargs['object'])
        context['basket_items'] = BasketItem.objects.filter(basket__user=self.request.user)
        context['min_shop_products'] = min(item.price for item in context['shop_products'])
        context['max_shop_products'] = max(item.price for item in context['shop_products'])
        context['category_products'] = Product.objects.filter(category=context['product'].category). \
            filter(~Q(slug=self.kwargs['slug']))
        context['settings'] = Product.objects.select_related('product_single_setting').get(
            slug=self.kwargs['slug']).product_single_setting
        context['comments'] = Comment.objects.filter(is_confirmed=True)
        context['categories'] = Category.objects.all()
        context['form'] = CommentForm()
        context['quantity'] = 0
        for i in context['shop_products']:
            context['quantity'] += i.quantity
        basket = Basket.objects.get(user=self.request.user)
        basket.total_price = self.get_basket_total_price(context['basket_items'])
        basket.save()
        context['basket'] = basket
        return context

    def get_basket_total_price(self, basket_items):
        total_price = 0
        for basket_item in basket_items:
            total_price += basket_item.total
        return total_price

    def get_success_url(self):
        return reverse('product_detail', kwargs={'slug': self.object.slug})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        print("post : ")
        form = CommentForm(request.POST)
        print("form in post : ", form)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        # if form.is_valid():
        #
        #     comment = form.save(commit=False)
        #     comment.author = request.user
        #     comment.product = Product.objects.get(slug=self.kwargs['slug'])
        #     comment.save()
        #     return redirect('product_detail')
        # else:
        #     raise ValidationError('Comment is not valid')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.product = Product.objects.get(slug=self.object.slug)
        form.save()


@csrf_exempt
def create_comment(request):
    print("request : ", request)
    print("request body : ", request.body)
    data = json.loads(request.body)
    print("date : ", data)
    try:
        user = request.user
    except:
        response = {"content": ''}
        return HttpResponse(json.dumps(response), status=201)
    try:
        comment = Comment.objects.create(product_id=data['product_id'], content=data['content'], author=user)
        response = {"content": comment.content, "dislike_count": 0, "like_count": 0, 'first_name': user.first_name,
                    'last_name': user.last_name, "comment_id": comment.id}
        return HttpResponse(json.dumps(response), status=201)
    except:
        response = {'error': 'Error'}
        print("error")
        return HttpResponse(json.dumps(response), status=400)


@csrf_exempt
def like_comment(request):
    data = json.loads(request.body)
    print(data)
    user = request.user
    try:
        comment = Comment.objects.get(id=data['comment_id'])
    except Comment.DoesNotExist:
        return HttpResponse('bad request', status=404)
    try:
        comment_like = CommentLike.objects.get(author=user, comment=comment)
        comment_like.condition = data['condition']
        comment_like.save()
    except CommentLike.DoesNotExist:
        CommentLike.objects.create(author=user, comment=comment, condition=data['condition'])
    response = {"like_count": comment.like_count, "dislike_count": comment.dislike_count}
    print(response)
    return HttpResponse(json.dumps(response), status=201)


class ShopProductView(FormMixin, DetailView):
    model = Product
    template_name = "product/shop_product.html"
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = Product.objects.get(slug=self.kwargs['slug'])
        context['shop_products'] = ShopProduct.objects.filter(product=kwargs['object'])
        context['basket_items'] = BasketItem.objects.filter(basket__user=self.request.user)
        context['categories'] = Category.objects.all()
        context['quantity'] = 0
        for i in context['shop_products']:
            context['quantity'] += i.quantity
        basket = Basket.objects.get(user=self.request.user)
        basket.total_price = self.get_basket_total_price(context['basket_items'])
        basket.save()
        context['basket'] = basket
        return context

    def get_basket_total_price(self, basket_items):
        total_price = 0
        for basket_item in basket_items:
            total_price += basket_item.total
        return total_price
