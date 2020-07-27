
from django.urls import re_path


# 路由映射表
from users.views import *

urlpatterns=[
    # 用户名是否重复检查接口
    # GET + usersnames/<用户名>/count = self.get
    re_path(r'^usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/count/$', UsernameCountView.as_view()),
    # 手机号是否重复
    re_path(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', MobileCountView.as_view()),
]

