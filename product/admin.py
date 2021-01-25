from django.contrib import admin
from django.contrib.admin.forms import AdminPasswordChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _

from product.models import Category, Product, ShopProduct, ProductImages, Comment, Like

User = get_user_model()  # give user as object not like setting.AUTH_USER_MODEL give string


class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'image', 'slug', 'detail')
    search_fields = ('name',)
    list_filter = ('name',)
    inlines = ['ProductInline']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('parent', 'name', 'image', 'slug', 'detail')
    search_fields = ('name',)
    list_filter = ('name',)
    inlines = ['ChildrenItemInline', 'ProductInline']


class ChildrenItemInline(admin.TabularInline):
    model = Category
    extra = 1
    field = ('name', 'slug')
    show_change_link = True


class ProductAdmin(admin.ModelAdmin):
    list_display = ('brand', 'category', 'name', 'image', 'slug', 'detail')
    search_fields = ('name', 'brand', 'category')
    list_filter = ('brand', 'category')
    inlines = ['ProductMetaInline', 'ShopProductInline', 'ProductImagesInline', 'CommentInline', 'LikeInline']


class ProductInline(admin.TabularInline):
    model = Product
    extra = 1
    field = ('name', 'brand', 'category')
    show_change_link = True


class ProductMetaAdmin(admin.TabularInline):
    list_display = ('product', 'label', 'value')
    search_fields = ('product', 'label')
    list_filter = ('product',)


class ProductMetaInline(admin.TabularInline):
    model = Product
    extra = 1
    field = ('product', 'label', 'value')
    show_change_link = True


class ShopProductAdmin(admin.ModelAdmin):
    list_display = ('shop', 'product', 'price', 'quantity')
    search_fields = ('shop', 'product')
    list_filter = ('shop', 'product')


class ShopProductInline(admin.TabularInline):
    model = ShopProduct
    extra = 1
    field = ('shop', 'product', 'price')
    show_change_link = True


class ProductImagesAdmin(admin.ModelAdmin):
    list_display = ('product', 'image')
    search_fields = ('product',)
    list_filter = ('product',)


class ProductImagesInline(admin.TabularInline):
    model = ProductImages
    extra = 1
    field = ('shop', 'product', 'price')
    show_change_link = True


class CommentAdmin(admin.ModelAdmin):
    list_display = ('product', 'author', 'content', 'create_at', 'update_at', 'is_confirmed')
    search_fields = ('product', 'author', 'is_confirmed')
    list_filter = ('product', 'author')


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1
    field = ('product', 'author', 'content', 'create_at', 'update_at', 'is_confirmed')
    show_change_link = True


class LikeAdmin(admin.ModelAdmin):
    list_display = ('product', 'user')
    search_fields = ('product', 'user')
    list_filter = ('product', 'user')


class LikeInline(admin.TabularInline):
    model = Like
    extra = 1
    field = ('product', 'user')
    show_change_link = True
