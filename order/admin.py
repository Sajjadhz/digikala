from django.contrib import admin
from django.contrib.admin.forms import AdminPasswordChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _

from order.models import OrderItem, Payment, Order, Basket, BasketItem

User = get_user_model()


class BasketInline(admin.TabularInline):
    model = Basket
    extra = 1
    field = ('user', 'created_at', 'updated_at', 'description', 'total_price')
    show_change_link = True


class BasketItemsInline(admin.TabularInline):
    model = BasketItem
    extra = 1
    field = ('basket', 'shop_product', 'quantity',  'price', 'total')
    show_change_link = True


class OrderItemsInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    field = ('order', 'shop_product', 'quantity',  'price', 'total')
    show_change_link = True


class OrderInline(admin.TabularInline):
    model = Order
    extra = 1
    field = ('user', 'created_at', 'updated_at', 'description', 'draft', 'total_price')
    show_change_link = True


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 1
    field = ('order', 'user', 'amount')
    show_change_link = True


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at', 'description', 'draft', 'total_price')
    search_fields = ('user',)
    list_filter = ('user',)
    inlines = [OrderItemsInline, PaymentInline]


class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ('order', 'shop_product', 'quantity', 'price')
    search_fields = ('order', 'shop_product')
    list_filter = ('order',)


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'user', 'amount')
    search_fields = ('order', 'user')
    list_filter = ('order',)


class BasketAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at', 'description', 'total_price')
    search_fields = ('user',)
    list_filter = ('user',)
    inlines = [BasketItemsInline]


class BasketItemsAdmin(admin.ModelAdmin):
    list_display = ('basket', 'shop_product', 'quantity', 'price', 'total')
    search_fields = ('basket', 'shop_product')
    list_filter = ('basket',)


admin.site.register(Basket, BasketAdmin)
admin.site.register(BasketItem, BasketItemsAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemsAdmin)
