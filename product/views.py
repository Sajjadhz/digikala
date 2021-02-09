import json

from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView
from django.db.models import Q

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
        # context['shop_products'] = ShopProduct.objects.filter(product=kwargs['object'])
        # context['average_shop_products'] = sum(item.price for item in context['shop_products']) / len(
        #     [item.price for item in context['shop_products']])
        context['categories'] = Category.objects.all()
        return context


class CategoryDetailView(DetailView):
    model = Category
    template_name = "product/category.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(slug=self.kwargs['slug'])
        context['child_categories'] = Category.objects.filter(parent=context['category'])
        context['categories'] = Category.objects.all()
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "product/product-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = Product.objects.get(slug=self.kwargs['slug'])
        context['product_images'] = ProductImage.objects.filter(product=kwargs['object'])
        context['shop_products'] = ShopProduct.objects.filter(product=kwargs['object'])
        context['min_shop_products'] = min(item.price for item in context['shop_products'])
        context['max_shop_products'] = max(item.price for item in context['shop_products'])
        context['category_products'] = Product.objects.filter(category=context['product'].category). \
            filter(~Q(slug=self.kwargs['slug']))
        a = Product.objects.select_related('product_single_setting').get(slug=self.kwargs['slug'])
        context['settings'] = a.product_single_setting
        print("settings : ", context['settings'])
        context['comments'] = Comment.objects.filter(is_confirmed=True)
        print("comments : ", context['comments'])
        context['form'] = CommentForm()
        print("first form : ", context['form'])
        context['quantity'] = 0
        for i in context['shop_products']:
            context['quantity'] += i.quantity
        return context

    def get_success_url(self):
        return reverse('product_detail', kwargs={'slug': self.object.slug})

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        print("form in post : ", form)
        if form.is_valid():

            comment = form.save(commit=False)
            comment.author = request.user
            comment.product = Product.objects.get(slug=self.kwargs['slug'])
            comment.save()
            return redirect('product_detail')
        else:
            raise ValidationError('Comment is not valid')
    # def form_valid(self, form):
    #     form.instance.author = self.request.user
    #     form.instance.request = Request.objects.get(pk=self.object.pk)
    #     form.instance.created = timezone.now
    #     form.save()
    #     self.object = form.save(commit=False)
    #     self.object.author = self.request.user
    #     self.object.request = Request.objects.get(pk=self.object.pk)
    #     self.object.created = timezone.now
    #     self.object.save()
    #     return super(RequestDetailView, self).form_valid(form)


@csrf_exempt
def create_comment(request):
    print("request : ", request)
    print("request body : ", request.body)
    data = json.loads(request.body)
    print("date : ", data)
    user = request.user
    try:
        comment = Comment.objects.create(product_id=data['product_id'], content=data['content'], author=user)
        response = {"content": comment.content, "dislike_count": 0, "like_count": 0, 'first_name': user.first_name,
                    "comment_id": comment.id}
        return HttpResponse(json.dumps(response), status=201)
    except:
        response = {'error': 'Error'}
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