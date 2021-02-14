from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _
from product.models import ShopProduct

User = get_user_model()  # give user as object not like setting.AUTH_USER_MODEL give string


class Order(models.Model):
    user = models.ForeignKey('account.User', on_delete=models.PROTECT, null=True, blank=True, related_name="order",
                             related_query_name="order")
    created_at = models.DateTimeField(_('Created at:'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)
    description = models.TextField(_('Description'), null=True, blank=True)
    draft = models.IntegerField(_('Draft'), default=True)

    def __str__(self):
        return self.user.first_name


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items",
                              related_query_name="order_items")
    shop_product = models.ForeignKey('product.ShopProduct', on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name="order_items",
                                     related_query_name="order_items")
    quantity = models.IntegerField(_('quantity'), null=True, blank=True)
    price = models.IntegerField(_('Price'), null=True, blank=True)
    total = models.IntegerField(_('Total'), null=True, blank=True)

    def __str__(self):
        return self.order.user.first_name


class Payment(models.Model):
    user = models.ForeignKey('account.User', on_delete=models.SET_NULL, null=True, blank=True, related_name="payment",
                             related_query_name="payment")  # query zadan ro asoon mikone
    order = models.ForeignKey(Order, on_delete=models.PROTECT, null=True, blank=True, related_name="payment",
                              related_query_name="payment")
    amount = models.IntegerField(_('Amount'), )

    def __str__(self):
        return self.user.first_name


class Basket(models.Model):
    user = models.OneToOneField('account.User', verbose_name=_('user'), on_delete=models.SET_NULL, null=True,
                                blank=True,
                                related_name="basket", related_query_name="basket")
    created_at = models.DateTimeField(_('Created at:'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)
    description = models.TextField(_('Description'), null=True, blank=True)
    total_price = models.IntegerField(_('TotalPrice'), default=0)

    def __str__(self):
        return str(self.user.first_name)


class BasketItem(models.Model):
    basket = models.ForeignKey(Basket, verbose_name=_('Basket'), on_delete=models.SET_NULL, related_name="basket_items",
                               related_query_name="basket_items", null=True, blank=True)
    shop_product = models.ForeignKey('product.ShopProduct', verbose_name=_('Shop Product'), on_delete=models.SET_NULL,
                                     null=True, blank=True)
    quantity = models.IntegerField(_('quantity'), null=True, blank=True)
    price = models.IntegerField(_('Price'), null=True, blank=True)
    total = models.IntegerField(_('Total'), null=True, blank=True)
    def __str__(self):
        return self.basket.user.first_name
