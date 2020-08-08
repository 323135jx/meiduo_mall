from django.urls import re_path
from .views import *

urlpatterns=[
    # 订单支付
    re_path(r'^payment/(?P<order_id>\d+)/$', PaymentView.as_view()),
    # 订单支付状态
    re_path(r'^payment/status/$', PaymentStatusView.as_view()),
]