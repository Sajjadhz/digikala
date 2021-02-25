from django.urls import path

from .views import CategoryDetailView, ProductDetailView, SubCategoryDetailView, create_comment, like_comment, \
    ShopProductView, SearchView, LowToHighPriceView, HighToLowPriceView

urlpatterns = [
    path('sub_category/<slug:slug>/', SubCategoryDetailView.as_view(), name='sub_category'),
    path('category/<slug:slug>/', CategoryDetailView.as_view(), name='category'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('shop_product/<slug:slug>/', ShopProductView.as_view(), name='shop_product'),
    path('comment/', create_comment, name='create_comment'),
    path('like_comment/', like_comment, name='like_comment'),
    path('search/<slug:slug>/', SearchView.as_view(), name='search'),
    path('low_to_high_price/<slug:slug>/', LowToHighPriceView.as_view(), name='low_to_high_price'),
    path('high_to_low_price/<slug:slug>/', HighToLowPriceView.as_view(), name='high_to_low_price'),
]
