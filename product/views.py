import json

from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, TemplateView
from django.db.models import Q
from django.views.generic.edit import FormMixin

from order.models import BasketItem, Basket
from product.forms import CommentForm
from product.models import Category, Product, ProductImage, ShopProduct, Comment, CommentLike, ProductLike, Brand


# Create your views here.


class SubCategoryDetailView(DetailView):
    model = Category
    template_name = "product/sub_category.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(slug=self.kwargs['slug'])
        context['products'] = list(map(self.get_min_price, Product.objects.filter(category=kwargs['object'])))
        context['categories'] = Category.objects.all()
        context['brands'] = Brand.objects.all()
        if self.request.user.is_authenticated:
            context['basket'] = self.get_basket_basket_items()[0]
            context['basket_items'] = self.get_basket_basket_items()[1]
        return context

    def get_basket_total_price(self, basket_items):
        total_price = 0
        for basket_item in basket_items:
            total_price += basket_item.total
        return total_price

    def get_min_price(self, product):
        min_price = min(item.price for item in product.shop_product.all())
        print("min_price : ", min_price)
        return [product, min_price]

    def get_basket_basket_items(self):
        basket = Basket.objects.get(user=self.request.user)
        basket_items = BasketItem.objects.filter(basket__user=self.request.user)
        basket.total_price = self.get_basket_total_price(basket_items)
        basket.save()
        return [basket, basket_items]


class CategoryDetailView(DetailView):
    model = Category
    template_name = "product/category.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(slug=self.kwargs['slug'])
        context['child_categories'] = Category.objects.filter(parent=context['category'])
        context['categories'] = Category.objects.all()
        context['brands'] = Brand.objects.all()
        if self.request.user.is_authenticated:
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


class SearchView(DetailView):
    model = Category
    template_name = "product/sub_category.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print('kwargs : ', kwargs)
        context['category'] = Category.objects.get(slug=self.kwargs['slug'])
        context['products'] = self.get_queryset_of_search()
        context['categories'] = Category.objects.all()
        context['brands'] = Brand.objects.all()
        if self.request.user.is_authenticated:
            context['basket'] = self.get_basket_basket_items()[0]
            context['basket_items'] = self.get_basket_basket_items()[1]
        return context

    def get_queryset_of_search(self):
        result = super(SearchView, self).get_queryset()
        query = self.request.GET.get('q')
        if query:
            product_result = list(map(self.get_min_price, Product.objects.filter(Q(category__name=query))))
            result = product_result
        else:
            result = None
        return result

    def get_basket_total_price(self, basket_items):
        total_price = 0
        for basket_item in basket_items:
            total_price += basket_item.total
        return total_price

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


class LowToHighPriceView(DetailView):
    model = Category
    template_name = "product/sub_category.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(slug=self.kwargs['slug'])
        context['products'] = list(map(self.get_min_price, Product.objects.filter(category=kwargs['object']))).sort()
        context['categories'] = Category.objects.all()
        context['brands'] = Brand.objects.all()
        if self.request.user.is_authenticated:
            context['basket'] = self.get_basket_basket_items()[0]
            context['basket_items'] = self.get_basket_basket_items()[1]
        return context

    def get_basket_total_price(self, basket_items):
        total_price = 0
        for basket_item in basket_items:
            total_price += basket_item.total
        return total_price

    def get_min_price(self, product):
        min_price = min(item.price for item in product.shop_product.all())
        print("min_price : ", min_price)
        return [product, min_price]

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


class HighToLowPriceView(DetailView):
    model = Category
    template_name = "product/sub_category.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(slug=self.kwargs['slug'])
        context['brands'] = Brand.objects.all()
        context['products'] = list(map(self.get_min_price, Product.objects.filter(category=kwargs['object']))).sort()
        if self.request.user.is_authenticated:
            context['basket'] = self.get_basket_basket_items()[0]
            context['basket_items'] = self.get_basket_basket_items()[1]
        context['categories'] = Category.objects.all()
        return context

    def get_basket_total_price(self, basket_items):
        total_price = 0
        for basket_item in basket_items:
            total_price += basket_item.total
        return total_price

    def get_min_price(self, product):
        min_price = min(item.price for item in product.shop_product.all())
        print("min_price : ", min_price)
        return [product, min_price]

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
            return [basket, basket_items]
        else:
            basket = Basket.objects.create(user=self.request.user.is_anonymous)
            basket_items = []
            basket.total_price = self.get_basket_total_price(basket_items)
            return [basket, basket_items]


class ProductDetailView(FormMixin, DetailView):
    model = Product
    template_name = "product/product-detail.html"
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = Product.objects.get(slug=self.kwargs['slug'])
        context['product_images'] = ProductImage.objects.filter(product=kwargs['object'])
        context['shop_products'] = ShopProduct.objects.filter(product=kwargs['object'])
        context['min_shop_products'] = min(item.price for item in context['shop_products'])
        context['max_shop_products'] = max(item.price for item in context['shop_products'])
        context['category_products'] = list(
            map(self.get_min_price, Product.objects.filter(category__slug=context['product'].category.slug)))
        print('category_products', context['category_products'])
        context['settings'] = Product.objects.select_related('product_single_setting').get(
            slug=self.kwargs['slug']).product_single_setting
        context['comments'] = Comment.objects.filter(is_confirmed=True)
        context['categories'] = Category.objects.all()
        context['form'] = CommentForm()
        context['product_likes'] = ProductLike.objects.filter(product__id=context['product'].id, condition=True).count()
        context['product_dislikes'] = ProductLike.objects.filter(product__id=context['product'].id, condition=False).count()
        context['quantity'] = 0
        for i in context['shop_products']:
            context['quantity'] += i.quantity
        if self.request.user.is_authenticated:
            context['basket'] = self.get_basket_basket_items()[0]
            context['basket_items'] = self.get_basket_basket_items()[1]
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
        return form

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

    def get_min_price(self, product):
        min_price = min(item.price for item in product.shop_product.all())
        print("min_price : ", min_price)
        return [product, min_price]

    def get_product_like_user(self, product):
        if self.request.user.is_authenticated:
            product_like_user = ProductLike.objects.filter(product__id=product.id,
                                                           user=self.request.user, condition=True)
            return product_like_user
        else:
            return True


class BrandFilterView(TemplateView, generic.View):
    template_name = "product/brand_filter.html"
    extra_context = {}

    def get_context_data(self, **kwargs):
        print('salam : ', kwargs)
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        print('categories', context['categories'])
        # context['products'] = products
        # print('products', context['products'])
        context['brands'] = Brand.objects.all()
        print('brands', context['brands'])
        context.update(self.extra_context)
        print('extra_context', self.extra_context)
        if self.request.user.is_authenticated:
            context['basket'] = self.get_basket_basket_items()[0]
            context['basket_items'] = self.get_basket_basket_items()[1]
        return context

    def get_basket_total_price(self, basket_items):
        total_price = 0
        for basket_item in basket_items:
            total_price += basket_item.total
        return total_price

    def get_min_price(self, product):
        min_price = min(item.price for item in product.shop_product.all())
        print("min_price : ", min_price)
        return [product, min_price]

    def get_basket_basket_items(self):
        print('before : ')
        basket = Basket.objects.get(user=self.request.user)
        print('after : ')
        basket_items = BasketItem.objects.filter(basket__user=self.request.user)
        basket.total_price = self.get_basket_total_price(basket_items)
        basket.save()
        return [basket, basket_items]

    def get_products(self, brands):
        products = []
        for brand in brands:
            products.append(Product.objects.filter(brand__name=brand))
        return products

    def post(self, request, *args, **kwargs):
        brands = request.POST.getlist('brands')
        print('brands_name', brands)
        products = list(map(self.get_min_price, self.get_products(brands)))
        print('products : ', products)
        return True


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


@csrf_exempt
def like_product(request):
    data = json.loads(request.body)
    print(data)
    user = request.user
    try:
        product = Product.objects.get(id=data['product_id'])
    except Product.DoesNotExist:
        return HttpResponse('bad request', status=404)
    try:
        product_like = ProductLike.objects.get(user=user, product=product)
        product_like.condition = data['condition']
        product_like.save()
    except ProductLike.DoesNotExist:
        ProductLike.objects.create(user=user, product=product, condition=data['condition'])
    response = {"like_count": product.like_count, "dislike_count": product.dislike_count}
    print(response)
    return HttpResponse(json.dumps(response), status=201)
