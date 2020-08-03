
from django.urls import re_path


# 路由映射表
from users.views import *

urlpatterns=[
    # 用户名是否重复检查接口
    # GET + usersnames/<用户名>/count = self.get
    re_path(r'^usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/count/$', UsernameCountView.as_view()),
    # 手机号是否重复
    re_path(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', MobileCountView.as_view()),
    # 注册
    re_path(r'^register/$', RegisterView.as_view()),
    # 用户登录的子路由
    re_path(r'^login/$', LoginView.as_view()),
    # 用户退出
    re_path(r'^logout/$', LogoutView.as_view()),
    # 用户中心
    re_path(r'^info/$', UserInfoView.as_view()),
    # 更新邮箱
    re_path(r'^emails/$', EmailView.as_view()),
    # 验证并激活邮箱借口
    re_path(r'^emails/verification/$', VerifyEmailView.as_view()),
    # 新增收货地址
    re_path(r'^addresses/create/$', CreateAddressView.as_view()),
    # 展示地址
    re_path(r'^addresses/$', AddressView.as_view()),
    # 修改地址
    re_path(r'^addresses/(?P<address_id>\d+)/$', UpdateDestroyAddressView.as_view()),
    # 设置默认地址
    re_path(r'^addresses/(?P<address_id>\d+)/default/$', DefaultAddressView.as_view()),
    # 更新地址标题
    re_path(r'^addresses/(?P<address_id>\d+)/title/$', UpdateTitleAddressView.as_view()),
    # 修改密码
    re_path(r'^password/$', ChangePasswordView.as_view()),
    # 用户浏览记录
    re_path(r'^browse_histories/$', UserBrowseHistory.as_view()),
]

