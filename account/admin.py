from django.contrib import admin
from django.contrib.admin.forms import AdminPasswordChangeForm
from django.contrib.admin.options import InlineModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _

from order.admin import OrderInline, PaymentInline, BasketInline
from product.admin import ShopProductInline, CommentInline, ProductLikeInline
from .models import User, Address, Shop, Email


# Register your models here.

class AddressInline(admin.TabularInline):
    model = Address
    extra = 1
    field = ('user', 'city', 'street', 'alley', 'zip_code')
    show_change_link = True


class ShopInline(admin.TabularInline):
    model = Shop
    extra = 1
    field = ('user', 'name', 'slug')
    show_change_link = True


class EmailInline(admin.TabularInline):
    model = Email
    extra = 1
    field = ('user', 'subject')
    show_change_link = True


class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'password']
    change_password_form = AdminPasswordChangeForm
    # initial register
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )
    # can add/change data after registeration
    fieldsets = (
        (_('hi data'), {
            'fields': ('email', 'password')
        }),
        (_('Personal info'), {
            'fields': ('first_name', 'last_name', 'image')
        }),
        (_('Permissions'), {
            'fields': ('is_staff', 'is_active', 'is_superuser')
        }),
        (_('Important dates'), {
            'fields': ('last_login', 'date_joined')
        }),
    )
    ordering = ['email', ]
    inlines = [AddressInline, ShopInline, OrderInline, PaymentInline, BasketInline, EmailInline, CommentInline,
               ProductLikeInline]


class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'street', 'alley', 'zip_code')
    search_fields = ('user', 'city')
    list_filter = ('user',)


class ShopAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'description', 'image', 'slug')
    search_fields = ('user', 'name', 'slug')
    list_filter = ('user',)
    inlines = [ShopProductInline]




class EmailAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject', 'body')
    search_fields = ('user', 'subject')
    list_filter = ('user',)


admin.site.register(User, UserAdmin)
admin.site.register(Shop, ShopAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Email, EmailAdmin)
