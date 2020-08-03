import json
import re

from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse
from django_redis import get_redis_connection

from goods.models import SKU
from .models import User
from django.contrib.auth import login,logout,authenticate

from meiduo_mall.utils.views import login_required

from celery_tasks.email.tasks import send_verify_email


import logging
logger = logging.getLogger('django')


# Create your views here.
# Code is boring, have a fun!

# 验证用户名重复
class UsernameCountView(View):

    def get(self, request, username):

        try:
            # 1、统计用户数量
            count = User.objects.filter(
                username=username
            ).count()
        except Exception as e:
            print(e)
            # 写日记
            logger.error(e)

        # 2、构建相应返回
        else:
            return JsonResponse({
                'code': 0,
                'errmsg': 'ok',
                'count': count
            })

class MobileCountView(View):
    def get(self, request, mobile):
        count = 0
        # 1、根据手机号统计数量
        try:
            count = User.objects.filter(
                mobile=mobile
            ).count()
        except Exception as e:
            print(e)
            # 写日记
            logger.error(e)
        # 2.国建请求
        return JsonResponse({
            'code': 0,
            'errmsg': 'ok',
            'count': count,
        })


class RegisterView(View):

    def post(self, request):
        '''接收参数, 保存到数据库'''
        # 1.接收参数
        dict = json.loads(request.body.decode())
        username = dict.get('username')
        password = dict.get('password')
        password2 = dict.get('password2')
        mobile = dict.get('mobile')
        allow = dict.get('allow')
        sms_code_client = dict.get('sms_code')

        # 2.校验(整体)
        if not all([username, password, password2, mobile, allow, sms_code_client]):
            return JsonResponse({'code':400,
                                      'errmsg':'缺少必传参数'})

        # 3.username检验
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return JsonResponse({'code': 400,
                                      'errmsg': 'username格式有误'})

        # 4.password检验
        if not re.match(r'^[a-zA-Z0-9]{8,20}$', password):
            return JsonResponse({'code': 400,
                                      'errmsg': 'password格式有误'})

        # 5.password2 和 password
        if password != password2:
            return JsonResponse({'code': 400,
                                      'errmsg': '两次输入不对'})
        # 6.mobile检验
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return JsonResponse({'code': 400,
                                      'errmsg': 'mobile格式有误'})
        # 7.allow检验
        if allow != True:
            return JsonResponse({'code': 400,
                                      'errmsg': 'allow格式有误'})

        # 8.sms_code检验 (链接redis数据库)
        redis_conn = get_redis_connection('verify_code')

        # 9.从redis中取值
        sms_code_server = redis_conn.get('sms_%s' % mobile)

        # 10.判断该值是否存在
        if not sms_code_server:
            return JsonResponse({'code': 400,
                                      'errmsg': '短信验证码过期'})
        # 11.把redis中取得值和前端发的值对比
        if sms_code_client.lower() != sms_code_server.decode().lower():
            return JsonResponse({'code': 400,
                                      'errmsg': '验证码有误'})

        # 12.保存到数据库 (username password mobile)
        try:
            user =  User.objects.create_user(username=username,
                                             password=password,
                                             mobile=mobile)

        except Exception as e:
            return JsonResponse({'code': 400,
                                      'errmsg': '保存到数据库出错'})

        login(request, user)


        request.session.set_expiry(0)
        # 13.拼接json返回
        return JsonResponse({'code': 0,
                                 'errmsg': 'ok'})

class LoginView(View):

    # 1.提取参数
    def post(self,request):
        dict1 = json.loads(request.body.decode())
        username = dict1.get('username')
        password = dict1.get('password')
        remembered = dict1.get('remembered')
    # 2.校验参数
        if not all([username,password]):
            return JsonResponse({
                'code':400,
                'errmsg': '你的登基还缺少某个人的帮助'
            })
        if not re.match(r'^\w{5,20}$', username):
            return JsonResponse({
                'code':400,
                'errmsg': '你的英雄尚未到账',
            })
        if not re.match(r'^\w{8,20}$', password):
            return JsonResponse({
                'code':400,
                'errmsg': '请给你的英雄多充值',
            })
    # 3.认证状态
        user = authenticate(request,username=username,password=password)
        if not user:
            return JsonResponse({
                'code':400,
                'errmsg': '君生你未生，你生君以老'
            })
    # 4.状态保持
        login(request, user)
    # 5.判断是否记住用户
        if remembered != True:
    # 6.如果没有记住: 关闭立刻失效
            request.session.set_expiry(0)
        else:
    # 7.如果记住:  设置为两周有效
            request.session.set_expiry(None)
    # 8.返回响应
        response = JsonResponse({
            'code':0,
            'errmsg': '小垃圾的第一次登录尝试'
        })
        response.set_cookie('username',
                            username,
                            max_age= 3600*24*14)

        return response

class LogoutView(View):
    # 实现退出功能
    def delete(self,request):
        # 清除seesion
        logout(request=request)

        # 构造响应
        response = JsonResponse({
            'code':0,
            'errmsg':"对面卧底已经干掉",
        })

        # 返回响应
        response.delete_cookie('username')
        return response

class UserInfoView(View):

    @method_decorator(login_required)
    def get(self, request):

        # 1.获取对象
        user = request.user

        # 2.构建响应
        return JsonResponse({
            'user': 0,
            'errmsg': 'ok',
            'info_data':{
                'username':user.username,
                'mobile': user.mobile,
                # 个性签名
                'email': user.email,
                'email_active': user.email_active

            }
        })

# 更新邮箱接口
class EmailView(View):

    @method_decorator(login_required)
    def put(self, request):
        # 1.提取参数
        data = json.loads(request.body.decode())
        email = data.get('email')

        # 2.校验参数
        if not email:
            return JsonResponse({'code':400,'errmsg':'没有传出机密文件的工具'})
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return JsonResponse({'code':0,'errmsg':'你是在使用打狗棒通信吗？！'})

        # 3.数据处理
        user = request.user
        try:
            user.email = email
            user.email_active = False
            user.save()
        except Exception as e:
            logger.error(e)
            return JsonResponse({
                'code':400,
                'errmsg':'添加卧底同僚失败'
            })

        # 发送邮箱验证邮件
        verify_url = user.generate_verify_email_url()
        send_verify_email.delay(email,verify_url)

        # 数据响应
        return JsonResponse({
            'code':0,
            'errmsg':'ok'
        })


# 确认邮箱接口
class VerifyEmailView(View):

    def put(self,request):
        # 1.提取查询字符串中token
        token = request.GET.get('token')

        # 2.校验token
        user = User.check_verify_email_token(token)
        if not user:
            return JsonResponse({
                'code':400,
                'errmsg':'你不是我们线人'
            })

        # 3.如果token有效，把邮箱的激活状态设置为True
        user.email_active = True
        user.save()

        return JsonResponse({'code':0, 'errmsg':'又联系到一个同僚！'})

from .models import Address
# 新增用户地址
class CreateAddressView(View):

    def post(self, request):
        # 1.提取参数
        data = json.loads(request.body.decode())
        receiver = data.get('receiver')
        province_id = data.get('province_id')
        city_id = data.get('city_id')
        district_id = data.get('district_id')
        place = data.get('place')
        mobile = data.get('mobile')
        tel = data.get('tel')
        email = data.get('email')

        # 判断用户地址数量是否超过20个
        user = request.user
        count = Address.objects.filter(user=user).count()
        if count>20:
            return JsonResponse({
                'code':400,
                'errmsg':'数量超限'
            })

        # 2.校验参数
        if not all([receiver, province_id, district_id, place, mobile]):
            return JsonResponse({
                'code':400,
                'errmsg':'缺少参数！'
            })

        if not all([receiver, province_id, city_id, district_id, place, mobile]):
            return JsonResponse({"code": 400, 'errmsg': '缺少参数！'})

        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return JsonResponse({'code': 400,
                                 'errmsg': '参数mobile有误'})
        if tel:
            if not re.match(r'^(0[0-9]{2,3}-)?([2-9][0-9]{6,7})+(-[0-9]{1,4})?$', tel):
                return JsonResponse({'code': 400,
                                     'errmsg': '参数tel有误'})
        if email:
            if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
                return JsonResponse({'code': 400,
                                     'errmsg': '参数email有误'})

        # 3.新建用户地址
        try:
            address = Address.objects.create(
                user=user,
                province_id=province_id,
                city_id=city_id,
                district_id=district_id,
                title=receiver,  # 当前地址的标题，默认收货人名称就作为地址标题
                receiver=receiver,
                place=place,
                mobile=mobile,
                tel=tel
            )

            # 如果当前新增地址的时候，用户没有设置默认地址，那么
            # 我们把当前新增的地址设置为用户的默认地址
            if not user.default_address:
                user.default_address = address
                user.save()

        except Exception as e:
            print(e)
            return JsonResponse({'code': 400, 'errmsg': '新增地址失败！'})

        address_info = {
            "id": address.id,
            "title": address.title,
            "receiver": address.receiver,

            "province": address.province.name,
            "city": address.city.name,
            "district": address.district.name,

            "place": address.place,
            "mobile": address.mobile,
            "tel": address.tel,
            "email": address.email
        }

        # 4、返回响应
        return JsonResponse({
            'code': 0,
            'errmsg': 'ok',
            'address': address_info
        })

# 网页地址展示接口
# 本质：把当前用户所有地址信息返回
class AddressView(View):

    def get(self, request):

        # 1、根据用户，过滤出当前用户的所有地址
        user = request.user
        addresses = Address.objects.filter(
            user=user,
            is_deleted = False # 没有逻辑删除的地址
        )

        # 2、把地址转化成字典
        address_list = []
        for address in addresses:
            if address.id != user.default_address_id:
                # address：每一个地址对象
                address_list.append({
                    'id': address.id,
                    'title': address.title,
                    'receiver': address.receiver,
                    'province': address.province.name,
                    'city': address.city.name,
                    'district': address.district.name,
                    'place': address.place,
                    'mobile': address.mobile,
                    'tel': address.tel,
                    'email': address.email
                })
            else:
                address_list.insert(0, {
                    'id': address.id,
                    'title': address.title,
                    'receiver': address.receiver,
                    'province': address.province.name,
                    'city': address.city.name,
                    'district': address.district.name,
                    'place': address.place,
                    'mobile': address.mobile,
                    'tel': address.tel,
                    'email': address.email
                })

        # 3、构建响应返回
        return JsonResponse({
            'code': 0,
            'errmsg': 'ok',
            'default_address_id': user.default_address_id,
            'addresses': address_list
        })




# 相同的请求路径+不同的请求方法 = 统一类视图中
# 更新地址接口
class UpdateDestroyAddressView(View):

    def put(self, request, address_id):

        # 1、获取被更新的地址
        try:
            address = Address.objects.get(pk=address_id)
        except Address.DoesNotExist as e:
            print(e)
            return JsonResponse({'code': 400, 'errmsg': '资源未找到！'})

        # 2、提取参数
        data = json.loads(request.body.decode())
        receiver = data.get('receiver')
        province_id = data.get('province_id')
        city_id = data.get('city_id')
        district_id = data.get('district_id')
        place = data.get('place')  # 详细地址
        mobile = data.get('mobile')
        tel = data.get('tel')
        email = data.get('email')

        # 3、校验参数
        if not all([receiver, province_id, city_id, district_id, place, mobile]):
            return JsonResponse({"code": 400, 'errmsg': '缺少参数！'})

        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return JsonResponse({'code': 400,
                                 'errmsg': '参数mobile有误'})
        if tel:
            if not re.match(r'^(0[0-9]{2,3}-)?([2-9][0-9]{6,7})+(-[0-9]{1,4})?$', tel):
                return JsonResponse({'code': 400,
                                     'errmsg': '参数tel有误'})
        if email:
            if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
                return JsonResponse({'code': 400,
                                     'errmsg': '参数email有误'})


        address.receiver = receiver
        address.province_id = province_id
        address.city_id = city_id
        address.district_id = district_id
        address.place = place
        address.mobile = mobile
        address.tel = tel
        address.email = email
        address.save()

        # data.pop('province')
        # data.pop('city')
        # data.pop('district')
        # Address.objects.filter(pk=address_id).update(**data)
        # address = Address.objects.get(pk=address_id)

        address_info = {
            "id": address.id,
            "title": address.title,
            "receiver": address.receiver,

            "province": address.province.name,
            "city": address.city.name,
            "district": address.district.name,

            "place": address.place,
            "mobile": address.mobile,
            "tel": address.tel,
            "email": address.email
        }

        return JsonResponse({
            'code': 0,
            'errmsg': 'ok',
            'address': address_info
        })

    def delete(self, request, address_id):
        """删除地址"""
        try:
            # 1.获取参数
            address = Address.objects.get(id=address_id)

            # 2.处理参数(逻辑删除)
            address.is_deleted = True
            address.save()
        except Address.DoesNotExist as e:
            logger.error(e)
            return JsonResponse({
                'code':400,
                'errmsg':'删除地址失败'
            })

        # 3.返回响应
        return  JsonResponse({
            'code':0,
            'errmsg':'删除地址成功'
        })

class DefaultAddressView(View):
    """设置默认地址"""
    def put(self, request, address_id):
        # 修改当前登录用户对象的default_address只想address_id的地址
        try:
            user = request.user
            # user.default_address = <Address对象>
            user.default_address_id = address_id
            # user.default_address = Address.objects.get(pk=address_id)
            user.save()
        except Address.DoesNotExist as e:
            logger.error(e)
            return JsonResponse({
                'code':400,
                'errmsg':'设置默认地址失败'
            })


        return JsonResponse({
            'code': 0,
            'errmsg':'ok'
        })


class UpdateTitleAddressView(View):
    """设置地址标题"""

    def put(self, request, address_id):

        try:
            # 1.获取更新数据
            data = json.loads(request.body.decode())
            title = data.get('title')
            # 2.获取被修改的地址对象
            address = Address.objects.get(pk=address_id)
            # 3.修改并返回响应
            address_title = title
            address.save()
        except Address.DoesNotExist as e:
            logger.error(e)
            return JsonResponse({
                'code':400,
                'errmsg':'修改地址名称失败'
            })

        return JsonResponse({
            'code':0,
            'errmsg':'ok'
        })

class ChangePasswordView(View):

    def put(self,request):
        # 1.提取参数
        data = json.loads(request.body.decode())
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        new_password2 = data.get('new_password2')

        # 2.校验参数
        if not all([old_password, new_password, new_password2]):
            return JsonResponse({
                'code': 400,
                'errmsg': '缺少必要参数'
            })

        if not re.match(r'^[a-zA-Z0-9]{8,20}$', new_password):
            return JsonResponse({'code': 400,
                                      'errmsg': 'password格式有误'})
        if new_password != new_password2:
            return JsonResponse({
                'code':400,
                'errmsg': '两次输入密码不一致'
            })
        user = request.user
        if not user.check_password(old_password):
            return JsonResponse({
                'code':400,
                'errmsg':'输入的原密码错误'
            }, status = 400)

        # 3.更新数据
        user.set_password(new_password)
        user.save()
        logout(request)

        # 4.返回响应
        response = JsonResponse({
            'code':0,
            'errmsg':'修改成功'
        })
        response.delete_cookie('username')
        return response


class UserBrowseHistory(View):

    @method_decorator(login_required)
    def post(self, request):
        # 记录用户历史
        # 1.获取请求参数
        data = json.loads(request.body.decode())
        sku_id =data.get('sku_id')

        user = request.user
        # 2.加入用户炉石记录redis列表中
        conn = get_redis_connection('history')

        p = conn.pipeline()
        # 2.1 去重
        p.lrem('history_%s'%user.id,0,sku_id)
        # 2.2 左侧插入
        p.lpush('history_%s'%user.id, sku_id)
        # 2.3 截断
        p.ltrim('history_%s'%user.id, 0, 4)
        p.excute()

        return JsonResponse({
            'code':0,
            'errmsg':'ok'
        })

    @method_decorator(login_required)
    def get(self,request):
        user = request.user

        # 1.读取redis游览历史
        conn = get_redis_connection('history')
        sku_ids = conn.lrange('history_%s'%user.id, 0, -1)

        # 2.获取sku商品信息
        # sku_ids = [int(x) for x in sku_ids]
        skus = SKU.objects.filter(id__in=sku_ids)
        sku_list = []
        for sku in skus:
            sku_list.append({
                'id': sku.id,
                'name': sku.name,
                'price': sku.price,
                'default_image_url':sku.default_image_url.url
            })

        # 3.返回响应
        return JsonResponse({
            'code':0,
            'errmsg':'ok',
            'skus':sku_list
        })