from django.urls import path

from .views import CategoryDetailView, ProductDetailView, SubCategoryDetailView, create_comment, like_comment, \
    SearchView, LowToHighPriceView, HighToLowPriceView, like_product

urlpatterns = [
    path('sub_category/<slug:slug>/', SubCategoryDetailView.as_view(), name='sub_category'),
    path('category/<slug:slug>/', CategoryDetailView.as_view(), name='category'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('comment/', create_comment, name='create_comment'),
    path('like_comment/', like_comment, name='like_comment'),
    path('like_product/', like_product, name='like_product'),
    path('search/<slug:slug>/', SearchView.as_view(), name='search'),
    path('low_to_high_price/<slug:slug>/', LowToHighPriceView.as_view(), name='low_to_high_price'),
    path('high_to_low_price/<slug:slug>/', HighToLowPriceView.as_view(), name='high_to_low_price'),
]
