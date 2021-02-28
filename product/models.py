from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _

import account
from account.models import Shop

User = get_user_model()  # give user as object not like setting.AUTH_USER_MODEL give string


class Brand(models.Model):
    name = models.CharField(_('Name'), max_length=150)
    image = models.ImageField(_('Image'), unique=True)
    slug = models.CharField(_('Slug'), max_length=100)
    detail = models.TextField(_('Detail'))

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(_('Name'), max_length=150)
    image = models.ImageField(_('Image'), unique=True)
    slug = models.SlugField(_('Slug'))
    detail = models.TextField(_('Detail'), blank=True, null=True)
    parent = models.ForeignKey('self', verbose_name=_("Parent"), on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='children', related_query_name='children')

    def __str__(self):
        return self.name


class Product(models.Model):
    brand = models.ForeignKey('Brand', on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='product',
                              related_query_name='product')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, related_name='products',
                                 related_query_name='products', null=True)
    name = models.CharField(_('Name'), max_length=150)
    image = models.ImageField(_('Image'), unique=True)
    slug = models.SlugField(_('Slug'))
    detail = models.TextField(_('Detail'))
    date_created = models.DateTimeField(_("Create at"), auto_now_add=True)

    @property
    def like_count(self):
        q = ProductLike.objects.filter(product=self, condition=True)
        return q.count()

    @property
    def dislike_count(self):
        q = ProductLike.objects.filter(product=self, condition=False)
        return q.count()

    def __str__(self):
        return self.name


class ProductMeta(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name='productMeta',
                                related_query_name='productMeta')
    label = models.CharField(_('Label'), max_length=250)
    value = models.CharField(_('value'), max_length=250)

    def __str__(self):
        return self.label


class ShopProduct(models.Model):
    shop = models.ForeignKey('account.Shop', on_delete=models.CASCADE, null=True, blank=True,
                             related_name='shop_product',
                             related_query_name='shop_product')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, related_name='shop_product',
                                related_query_name='shop_product')
    price = models.IntegerField(_('Price'))
    quantity = models.IntegerField(_('Quantity'))

    def __str__(self):
        return str(self.product.name) + ' ' + str(self.shop.name)


class ProductImage(models.Model):
    product = models.ForeignKey('Product', verbose_name=_(
        "Products"), on_delete=models.CASCADE, related_name="images", related_query_name="images")
    image = models.ImageField(_('Image'), blank=True)

    def __str__(self):
        return self.image.url


# class Off(models.Model):
#     code = models.IntegerField(_('Off code'), unique=True)
#     start = models.DateTimeField(_('Start at'))
#     end = models.DateTimeField(_('End at'))
#     percentage = models.FloatField(_('Percentage'))


class ProductSingleSetting(models.Model):
    product = models.OneToOneField(Product, verbose_name=_("product"), on_delete=models.CASCADE, related_name=
    'product_single_setting', related_query_name='product_single_setting')
    author = models.BooleanField(_("author"))
    comment = models.BooleanField(_("comment"))
    allow_discussion = models.BooleanField(_("allow discussion"), default=True)

    class Meta:
        verbose_name = _("ProductSingleSetting")
        verbose_name_plural = _("ProductSingleSettings")


class Comment(models.Model):
    author = models.ForeignKey('account.User', verbose_name=_(
        "Author"), on_delete=models.SET_NULL, related_name='comment', related_query_name='comment', null=True,
                               blank=True)
    product = models.ForeignKey('Product', verbose_name=_(
        "Products"), on_delete=models.CASCADE, related_name="comment", related_query_name="comment")
    content = models.TextField(_("Content"))
    create_at = models.DateTimeField(_("Create at"), auto_now_add=True)
    update_at = models.DateTimeField(_("Update at"), auto_now=True)
    is_confirmed = models.BooleanField(_("confirm"), default=True)

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        ordering = ['-create_at']

    @property
    def like_count(self):
        q = CommentLike.objects.filter(comment=self, condition=True)
        return q.count()

    @property
    def dislike_count(self):
        q = CommentLike.objects.filter(comment=self, condition=False)
        return q.count()

    def __str__(self):
        return self.product.name


class CommentLike(models.Model):
    author = models.ForeignKey('account.User', verbose_name=_(
        "Author"), on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, verbose_name=_(
        'Comment'), on_delete=models.CASCADE)
    condition = models.BooleanField(_("Condition"))
    create_at = models.DateTimeField(_("Create at"), auto_now_add=True)
    update_at = models.DateTimeField(_("Update at"), auto_now=True)

    class Meta:
        verbose_name = _("CommentLike")
        verbose_name_plural = _("CommentLikes")
        unique_together = ('author', 'comment',)

    def __str__(self):
        return str(self.condition)


class ProductLike(models.Model):
    user = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name="product_like", related_query_name="product_like")
    product = models.ForeignKey('Product', verbose_name=_(
        "Products"), on_delete=models.CASCADE, related_name="product_like", related_query_name="product_like")
    condition = models.BooleanField(_("Condition"), default=True)
    create_at = models.DateTimeField(_("Create at"), auto_now_add=True)
    update_at = models.DateTimeField(_("Update at"), auto_now=True)

    class Meta:
        verbose_name = _("CommentLike")
        verbose_name_plural = _("CommentLikes")
        unique_together = ('user', 'product',)

    def __str__(self):
        return self.product.name
