from django.urls import re_path

from orders.views import *

urlpatterns = [
    # 订单确认
    re_path(r'^orders/settlement/$', OrderSettlementView.as_view()),
    # 订单提交
    re_path(r'^orders/commit/$', OrderCommitView.as_view()),
]