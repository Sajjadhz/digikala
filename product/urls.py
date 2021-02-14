from django.urls import path

from .views import CategoryDetailView, ProductDetailView, SubCategoryDetailView, create_comment, like_comment, \
    ShopProductView

urlpatterns = [
    path('sub_category/<slug:slug>/', SubCategoryDetailView.as_view(), name='sub_category'),
    path('category/<slug:slug>/', CategoryDetailView.as_view(), name='category'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('shop_product/<slug:slug>/', ShopProductView.as_view(), name='shop_product'),
    path('comment/', create_comment, name='create_comment'),
    path('like_comment/', like_comment, name='like_comment'),
]
