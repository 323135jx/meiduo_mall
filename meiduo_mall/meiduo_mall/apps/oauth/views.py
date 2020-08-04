from django.contrib.auth import login
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from QQLoginTool.QQtool import OAuthQQ
from django.conf import settings
from django_redis import get_redis_connection
from carts.utills import merge_cart_cookie_to_redis

from itsdangerous import TimedJSONWebSignatureSerializer

from users.models import User
from .models import OAuthQQUser

import re
import json
import logging
logger = logging.getLogger('django')

# Create your views here.



#
# def check_access_token(token):
#     # 功能：解密openid
#     # 参数：token值
#     # 返回值：openid
#     serializer = TimedJSONWebSignatureSerializer(
#         secret_key=settings.SECRET_KEY
#     )
#     data = serializer.loads(token)
#
#     openid = data.get("openid")
#
#     return openid
#
#
#
# def generate_access_token(openid):
#     # 功能：加密openid
#     # 参数：openid用户的qq标示
#     # 返回值：token值
#     serializer = TimedJSONWebSignatureSerializer(
#         secret_key=settings.SECRET_KEY,
#         expires_in=3600 # 定义当前生成的token的有效期为3600秒
#
#     )
#
#     # 加密的数据为一个字典
#     data = {"openid":openid}
#
#     access_token = serializer.dumps(data)
#
#     return access_token.decode()
#
# class QQFirstView(View):
#     """提供QQ登录网页界面网址"""
#
#     def get(self,request):
#
#         # 1. 获取数据
#         next_url = request.GET.get('next')
#
#
#         # 2. 处理数据
#         # 获取qq登录界面
#         oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
#                            client_secret=settings.QQ_CLIENT_SECRET,
#                            redirect_uri=settings.QQ_REDIRECT_URI,
#                            state=next_url
#                            )
#
#         login_url = oauth.get_qq_url()
#
#         # 3. 构造返回响应
#         return JsonResponse({
#             'code':0,
#             'errmsg':'ok',
#             'login_url':login_url
#         })
#
# class QQUserView(View):
#     """用户扫码登录的回调处理"""
#
#     def get(self, request):
#         """获取从前端发送过来的code参数"""
#         code = request.GET.get('code')
#
#         if not code:
#             return({
#                 'code':400,
#                 'errmsg':'缺少code参数'
#             })
#
#         # 调用我们安装的QQLoginTool工具类
#         # 创建工具对象
#         oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
#                         client_secret=settings.QQ_CLIENT_SECRET,
#                         redirect_uri=settings.QQ_REDIRECT_URI,
#                         )
#
#         try:
#             # 携带code向qq服务器请求acces_token
#             token = oauth.get_access_token(code)
#             openid = oauth.get_open_id(token)
#
#         except Exception as e:
#             # 如果上面获取openid出错，则验证失败
#             logger.error(e)
#             # 返回结果
#             return JsonResponse({
#                 'code':400,
#                 'errmsg':'oauth2.0认证失败，即获取qq信息失败'
#             })
#
#         try:
#             oauth_qq = OAuthQQUser.objects.get(openid=openid)
#         except OAuthQQUser.DoesNotExist as e:
#             logger.info(e)
#             access_token = generate_access_token(openid)
#             return JsonResponse({
#                 'access_token':access_token
#             })
#
#         # 用户已经绑定过qq--登录成功！！
#         user =oauth_qq.user
#         login(request, user)    # 状态保持
#         response = JsonResponse({
#             "code":0,
#             "errmsg":'ok'
#         })
#         response.set_cookie("username", user.username, max_age=3600*24*14)
#         return response
#
#     def post(self, request):
#         """根据用户传进来的手机号，判断用户是否注册美多商城号"""
#         # 1.获取数据
#         user_info = json.loads(request.body.decode())
#         mobile = user_info.get('mobile')
#         password = user_info.get('password')
#         sms_code = user_info.get('sms_code')
#         access_token = user_info.get('access_token')
#
#         if not all([mobile,password,sms_code,access_token]):
#             return JsonResponse({
#                 "code":400,
#                 "errmsg":"缺少必要的参数"
#             })
#
#         # 2.校验数据
#         # 判断手机是否合法
#         if not re.match(r'^1[3-9]\d{9}$', mobile):
#             return JsonResponse({
#                 "code":400,
#                 "errmsg":"请输入正确的手机号码"
#             })
#
#         # 判断密码是否合法
#         if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
#             return JsonResponse({
#                 "code": 400,
#                 "errmsg": "请输入8-20位的密码"
#             })
#
#         conn = get_redis_connection('sms_code')
#         sms_code_from_redis = conn.get("sms_%s"%mobile)
#         if not sms_code_from_redis:
#             return JsonResponse({
#                 "code":400,
#                 "errmsg":"验证码过期"
#             })
#         if sms_code_from_redis.decode() != sms_code:
#             return JsonResponse({
#                 "code":400,
#                 "errmsg":"你弄啥？连个密码都输错"
#             })
#
#         # 3.处理数据
#         # 把openid从access_token参数中解密出来
#         openid = check_access_token(access_token)
#
#         try:
#             user = User.objects.get("mobile")
#         except User.DoesNotExist as e:
#             logger.info(e)
#             # 3.1 没有注册，新建在绑定
#             user = User.objects.create_user(
#                 username=mobile,
#                 mobile=mobile,
#                 password=password,
#             )
#             # 绑定openid
#             OAuthQQUser.objects.create(
#                 openid = openid,
#                 user=user
#             )
#             login(request, user)
#             response = JsonResponse({'code':0,'errmsg':'ok'})
#             response.set_cookie('username', user.username, max_age=3600*24*14)
#             response = merge_cart_cookie_to_redis(request=request, user=user, response=response)
#             return response
#         # 3.2 已经注册，直接绑定
#         # 绑定openid
#         OAuthQQUser.objects.create(
#             openid = openid,
#             user=user
#         )
#         login(request, user)
#
#         # 4.返回响应
#         response = JsonResponse({
#             "code":0,
#             "errmsg":"ok"
#         })
#         response.set_cookie("username", user.username, max_age=3600*24*14)
#
#         # 合并购物车
#         response = merge_cart_cookie_to_redis(request=request, user=user, response=response)
#         return response

def generate_access_token(openid):
    # 功能：加密openid
    # 参数：openid用户的qq标示
    # 返回token值
    serializer = TimedJSONWebSignatureSerializer(
        secret_key=settings.SECRET_KEY,
        expires_in=3600 # 定义当前生成的token的有效期为3600秒
    )

    # 加密的数据是一个字典
    data = {"openid": openid}

    access_token = serializer.dumps(data)

    return access_token.decode()


def check_access_token(token):
    # 功能：解密出openid
    # 参数：token值
    # 返回值，返回openid
    serializer = TimedJSONWebSignatureSerializer(
        secret_key=settings.SECRET_KEY
    )

    data = serializer.loads(token)

    openid = data.get('openid')

    return openid



class QQUserView(View):

    def get(self, request):

        # 1、提取查询字符串参数code
        code = request.GET.get('code')
        # 2、验证code获取token
        try:
            oauth_qq = OAuthQQ(
                client_id=settings.QQ_CLIENT_ID,
                client_secret=settings.QQ_CLIENT_SECRET,
                redirect_uri=settings.QQ_REDIRECT_URI
            )
            token = oauth_qq.get_access_token(code)
            # 3、根据token获取openid
            openid = oauth_qq.get_open_id(access_token=token)
        except Exception as e:
            print(e)
            return JsonResponse({'code': 400, 'errmsg': 'qq登陆失败！'})


        try:
            oauth_qq = OAuthQQUser.objects.get(openid=openid)
        except OAuthQQUser.DoesNotExist as e:
            # 4、用户没有绑定过qq：我们需要返回加密的openid
            access_token = generate_access_token(openid)
            return JsonResponse({
                'access_token': access_token
            })


        # 5、用户已经绑定过qq——登陆成功！！
        user = oauth_qq.user
        login(request, user) # 状态保持
        response = JsonResponse({'code':0, 'errmsg': 'ok'})
        response.set_cookie('username', user.username, max_age=3600*24*14)
        return response


    def post(self, request):
        # 根据用户传递来的手机号，判断用户是否注册美多商城账号
        user_info = json.loads(request.body.decode())
        mobile = user_info.get('mobile')
        password = user_info.get('password')
        sms_code = user_info.get('sms_code')
        access_token = user_info.get("access_token")

        if not all([mobile, password, sms_code, access_token]):
            return JsonResponse({'code': 400, 'errmsg': '缺少参数'})

        # 判断手机号是否合法
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return JsonResponse({'code': 400,
                                 'errmsg': '请输入正确的手机号码'})

        # 判断密码是否合格
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return JsonResponse({'code': 400,
                                 'errmsg': '请输入8-20位的密码'})


        conn = get_redis_connection('sms_code')
        sms_code_fron_redis = conn.get('sms_%s'%mobile)
        if not sms_code_fron_redis:
            return JsonResponse({'code': 400, 'errmsg': '验证码过期'})
        if sms_code_fron_redis.decode() != sms_code:
            return JsonResponse({'code': 400, 'errmsg': '您输入的短信验证码有误！'})


        # 把openid从access_token参数中解密出来
        openid = check_access_token(access_token)

        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist as e:
            print(e)
            # 1、没有注册，新建再绑定
            user = User.objects.create_user(
                username=mobile,
                mobile=mobile,
                password=password
            )
            # 绑定openid
            OAuthQQUser.objects.create(
                openid=openid,
                user=user
            )

            login(request, user)
            response = JsonResponse({'code': 0, 'errmsg': 'ok'})
            response.set_cookie('username', user.username, max_age=3600*24*14)
            return response


        # 2、已经注册，直接绑定
        # 绑定openid
        OAuthQQUser.objects.create(
            openid=openid,
            user=user
        )
        login(request, user)
        response = JsonResponse({'code': 0, 'errmsg': 'ok'})
        response.set_cookie('username', user.username, max_age=3600 * 24 * 14)
        return response


class QQFirstView(View):

    # 接口1
    def get(self, request):

        # 获取携带的next查询字符串参数
        # 该参数表面qq登陆之后返回的页面
        next_url = request.GET.get('next')

        # 1、获取qq登陆扫码页面链接
        oauth_qq = OAuthQQ(
            client_id=settings.QQ_CLIENT_ID,
            client_secret=settings.QQ_CLIENT_SECRET,
            redirect_uri=settings.QQ_REDIRECT_URI,
            state=next_url
        )
        login_url = oauth_qq.get_qq_url()

        # 2、构建响应返回
        return JsonResponse({
            'code': 0,
            'errmsg': 'ok',
            'login_url': login_url
        })
