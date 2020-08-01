from oauth.views import *
from django.urls import re_path

urlpatterns = [
        # 获取QQ扫码登录链接
        re_path(r'^qq/authorization/$', QQFirstView.as_view()),
        # QQ用户部分接口
        re_path(r'^oauth_callback/$', QQUserView.as_view()),

]