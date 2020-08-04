from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
import json
from goods.models import SKU
from django_redis import get_redis_connection

from .utills import carts_cookie_decode,carts_cookie_encode
# Create your views here.



class CartSelectAllView(View):
    """全选购物车"""

    def put(self, request):
        #　1.接收参数
        json_dict = json.loads(request.body.decode())
        selected = json_dict.get('selected', True)

        #　2.检验参数
        if selected:
            if not isinstance(selected, bool):
                return JsonResponse({'code':400,'errmsg':'参数selected有误'})

        #　3.是否登录
        user = request.user
        if user.is_authenticated:
            # 用户已登录,操作redis购物车
            redis_conn = get_redis_connection('carts')
            item_dict = redis_conn.hgetall('carts_%s'%user.id)
            sku_ids = item_dict.keys()

            if selected:
                # 全选
                redis_conn.sadd('selected_%s'%user.id, *sku_ids)
            else:
                # 取消全选
                redis_conn.srem('selected_%s'%user.id, *sku_ids)
            return JsonResponse({'code':0,'errmsg':'全选购物车成功！'})
        else:
            cookie_cart = request.COOKIES.get('carts')
            response = JsonResponse({'code':0,'errmsg':'全选购物车成功'})

            if cookie_cart:
                cart_dict =carts_cookie_decode(cookie_cart)

                for sku_id in cart_dict.keys():
                    cart_dict[sku_id]['selected'] = selected

                cart_data = carts_cookie_encode('carts')

                response.set_cookie('carts', cart_data)

            return response
        #　4.返回响应

class CartsView(View):


    def delete(self, request):
        """
        接收和检验参数
        :param request:
        :return:
        """
        data = json.loads(request.body.decode())
        sku_id = data.get('sku_id')
        # count =data.get('count')
        # selected = data.get('selected')

        user = request.user
        if user.is_authenticated:
            conn = get_redis_connection('carts')
            conn.hdel('carts_%s'%user.id, sku_id)
            return JsonResponse({'code':0,'errmsg':'删除购物车成功'})
        else:
            cookie_cart = request.COOKIES.get('carts')
            if cookie_cart:
                cart_dict = carts_cookie_decode(cookie_cart)
            else:
                cart_dict = {}
            response = JsonResponse({'code':0,'errmsg':'删除购物车成功'})

            if sku_id in cart_dict:
                del cart_dict[sku_id]
                cart_data = carts_cookie_encode(cart_dict)
                response.set_cookie('carts', cart_data)
            return response

    def put(self, request):

        data = json.loads(request.body.decode())
        sku_id =data.get('sku_id')
        count =data.get('count')
        selected =data.get('selected', True)

        user = request.user
        if user.is_authenticated:
            conn = get_redis_connection('carts')
            conn.hmset('carts_%s'%user.id, {sku_id:count})
            if selected:
                conn.sadd('selected_%s'%user.id, sku_id)
            else:
                conn.srem('selected_%s'%user.id, sku_id)
            return JsonResponse({
                'code':0,
                'errmsg':'ok',
                'cart_sku':{
                    'id':sku_id,
                    'count':count,
                    'selected':selected
                }
            })

        else:
            cart_dict = {}
            cart_str = request.COOKIES.get('carts')
            if cart_str:
                cart_dict = carts_cookie_decode(cart_str)
            if not cart_dict:
                return JsonResponse({'code':0,'errmsg':'ok'})
            if sku_id in cart_dict:
                cart_dict[sku_id]['count'] = count
                cart_dict[sku_id]['selected'] = selected

            cart_str = carts_cookie_encode(cart_dict)

            response = JsonResponse({
                'code':0,
                'errmsg':'ok',
                'cart_sku':{
                    'id':sku_id,
                    'count':count,
                    'selected':selected
                }
            })

            response.set_cookie(
                'carts',
                cart_str
            )

            return response

    def get(self, request):
        cart_dict = {}
        user = request.user
        if user.is_authenticated:
            conn = get_redis_connection('carts')
            cart_redis_dict = conn.hgetall('carts_%s'%user.id)
            cart_redis_selected = conn.smembers('selected_%s'%user.id)
            for k,v in cart_redis_dict.items():
                cart_dict[int(k)] = {
                    'count':int(v),
                    'selected': k in cart_redis_selected
                }


        else:
            cart_str = request.COOKIES.get('carts')
            if cart_str:
                cart_dict = carts_cookie_decode(cart_str)

        cart_skus = []
        for k,v in cart_dict.items():
            # k: sku_id; v:{count:xx, selected:xx}
            sku = SKU.objects.get(pk=k)
            cart_skus.append({
                'id':sku.id,
                'name':sku.name,
                'count':v['count'],
                'selected':v['selected'],
                'price':sku.price,
                'default_image_url':sku.default_image_url.url,
                'amount':v['count']*sku.price
            })
        return JsonResponse({
            'code':0,
            'errmsg':'ok',
            'cart_skus':cart_skus
        })

    def post(self, request):
        # 1.提取参数
        data = json.loads(request.body.decode())
        sku_id = data.get('sku_id')
        count = data.get('count')
        selected = data.get('selected', True)

        # 2.检验参数
        if not all([sku_id, count]):
            return JsonResponse({
                'code':400,
                'errmsg':'缺少参数！'
            })

        if not isinstance(selected, bool):
            return JsonResponse({
                'code':400,
                'errmsg':'参数有误！'
            })


        # 3.判断是否登录
        user = request.user
        if user.is_authenticated:
            # 4.登录写入redis
            conn = get_redis_connection('carts')
            conn.hincrby('carts_%s'%user.id, sku_id, amount = count)    # 不存在则新增
            if selected == True:
                conn.sadd('selected_%s'%user.id, sku_id)
            return JsonResponse({'code': 0,'errmsg': 'ok'})

        else:
            # 5.未登录写入cookie
            cart_dict = {}
            cart_str =request.COOKIES.get('carts')
            if cart_str:
                cart_dict = carts_cookie_decode(cart_str)
            if sku_id in cart_dict:
                cart_dict[sku_id]['count'] += count
            else:
                cart_dict[sku_id] = {
                    'count':count,
                    'selected':selected
                }

            cart_dict[sku_id]['selected'] = selected

            cart_str = carts_cookie_encode(cart_dict)

            response = JsonResponse({
            'code':0,
            'errmsg':'ok'
        })
            response.set_cookie(
                'carts',
                cart_str
            )
            return response






