
from django.urls import re_path
from .views import *

urlpatterns = [
    re_path(r'^carts/$', CartsView.as_view()),
    # 购物车全选
    re_path(r'^carts/selection/$', CartSelectAllView.as_view()),
    # 提供商品页面右上角购物车数据
    re_path(r'^carts/simple/$', CartsSimpleView.as_view()),
]