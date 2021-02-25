from django.contrib import admin
from django.contrib.admin.forms import AdminPasswordChangeForm
from django.contrib.admin.options import InlineModelAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _

from order.admin import BasketItemsInline, OrderItemsInline
from product.models import Category, Product, ShopProduct, ProductImage, Comment, Like, ProductMeta, Brand, \
    ProductSingleSetting, CommentLike

User = get_user_model()  # give user as object not like setting.AUTH_USER_MODEL give string


class ChildrenItemInline(admin.TabularInline):
    model = Category
    extra = 2
    field = ('name', 'slug')
    show_change_link = True


class ProductInline(admin.TabularInline):
    model = Product
    extra = 1
    field = ('name', 'brand', 'category')
    show_change_link = True


class ProductMetaInline(admin.TabularInline):
    model = ProductMeta
    extra = 1
    field = ('product', 'label', 'value')
    show_change_link = True


class ShopProductInline(admin.TabularInline):
    model = ShopProduct
    extra = 3
    field = ('shop', 'product', 'price')
    show_change_link = True


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    field = ('shop', 'product', 'price')
    show_change_link = True


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 2
    field = ('product', 'author', 'content', 'create_at', 'update_at', 'is_confirmed')
    show_change_link = True


class ProductSingleSettingInline(admin.TabularInline):
    model = ProductSingleSetting
    extra = 3
    field = ('product', 'author', 'comment', 'allow_discussion')
    show_change_link = True


class LikeInline(admin.TabularInline):
    model = Like
    extra = 2
    field = ('product', 'user')
    show_change_link = True


class CommentLikeInline(admin.TabularInline):
    model = CommentLike
    extra = 2
    field = ('author', 'comment')
    show_change_link = True


class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'detail')
    search_fields = ('name',)
    list_filter = ('name',)
    inlines = [ProductInline]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'slug', 'detail')
    search_fields = ('name',)
    list_filter = ('name',)
    inlines = [ChildrenItemInline, ProductInline]


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'brand', 'slug', 'detail')
    search_fields = ('name', 'brand', 'category')
    list_filter = ('brand', 'category')
    inlines = [ProductMetaInline, ShopProductInline, ProductImageInline, CommentInline, LikeInline,
               ProductSingleSettingInline]


class ProductSingleSettingAdmin(admin.ModelAdmin):
    list_display = ('product', 'author', 'comment', 'allow_discussion')
    search_fields = ('product',)
    list_filter = ('product', 'author')


class ProductMetaAdmin(admin.ModelAdmin):
    list_display = ('product', 'label', 'value')
    search_fields = ('product', 'label')
    list_filter = ('product',)


class ShopProductAdmin(admin.ModelAdmin):
    list_display = ('shop', 'product', 'price', 'quantity')
    search_fields = ('shop', 'product')
    list_filter = ('shop', 'product')
    inlines = [BasketItemsInline, OrderItemsInline]


class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', )
    search_fields = ('product',)
    list_filter = ('product',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('product', 'author', 'content', 'create_at', 'update_at', 'is_confirmed')
    search_fields = ('product', 'author', 'is_confirmed')
    list_filter = ('product', 'author')
    inlines = [CommentLikeInline]


class LikeAdmin(admin.ModelAdmin):
    list_display = ('product', 'user')
    search_fields = ('product', 'user')
    list_filter = ('product', 'user')


class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ('author', 'comment', 'condition', 'create_at', 'update_at')
    search_fields = ('author', 'comment')
    list_filter = ('author', 'comment', 'condition')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(ShopProduct, ShopProductAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductMeta, ProductMetaAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(ProductSingleSetting, ProductSingleSettingAdmin)
admin.site.register(CommentLike, CommentLikeAdmin)

