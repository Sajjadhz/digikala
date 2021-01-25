from django.contrib import admin
from django.contrib.admin.forms import AdminPasswordChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _

from order.models import OrderItems, Payment, Order, Basket, BasketItems

User = get_user_model()


class OrderItemsInline(admin.TabularInline):
    model = OrderItems
    extra = 1
    field = ('order', 'shop_product', 'price')
    show_change_link = True


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 1
    field = ('order', 'user', 'amount')
    show_change_link = True


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at', 'description')
    search_fields = ('user',)
    list_filter = ('user',)
    inlines = [OrderItemsInline, PaymentInline]


class OrderInline(admin.TabularInline):
    model = Order
    extra = 1
    field = ('user', 'created_at', 'updated_at', 'description')
    show_change_link = True


class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ('order', 'shop_product', 'quantity', 'price')
    search_fields = ('order', 'shop_product')
    list_filter = ('order',)





class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'user', 'amount')
    search_fields = ('order', 'user')
    list_filter = ('order',)





class BasketAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at', 'description')
    search_fields = ('user',)
    list_filter = ('user',)
    inlines = ['BasketItemsInline']


class BasketInline(admin.TabularInline):
    model = Basket
    extra = 1
    field = ('user', 'created_at', 'updated_at', 'description')
    show_change_link = True


class BasketItemsAdmin(admin.ModelAdmin):
    list_display = ('order', 'shop_product', 'quantity', 'price')
    search_fields = ('order', 'shop_product')
    list_filter = ('order',)


class BasketItemsInline(admin.TabularInline):
    model = BasketItems
    extra = 1
    field = ('order', 'shop_product', 'price')
    show_change_link = True