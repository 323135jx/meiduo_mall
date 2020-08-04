"""
封装工具函数
"""


# Cookie数据的编码
import base64
import pickle

from django_redis import *


def carts_cookie_encode(cart_dict):
    """
    把购物车字典数据，经过pickle和base64编码成可视化字符
    :param cart_dict: 购物车字典
    :return: 可视化字符串
    """
    # 1.使用pickl
    return base64.b64encode(pickle.dumps(cart_dict)).decode()

def carts_cookie_decode(cart_str):
    return pickle.loads(base64.b64decode(cart_str.encode()))

def merge_cart_cookie_to_redis(request, user, response):
    """
    登录后合并cookie购物车数据到Redis
    :param request: 本次请求对象,获取cookie中的数据
    :param user: 登录用户信息,获取user_id
    :param response: 本次响应对象,清除cookie中的数据
    :return: response
    """
    # 获取cookie中的购物车数据
    cookie_cart = request.COOKIES.get('carts')
    if not cookie_cart:
        return response
    cart_dict = carts_cookie_decode(cookie_cart)

    new_dict = {}
    new_add = []
    new_remove = []

    #　同步cookie中购物车数据
    for sku_id, item in cart_dict.items():
        new_dict[sku_id]=item['count']
        if item['selected']:
            new_add.append(sku_id)
        else:
            new_remove.append(sku_id)

    # 将new_cart_dict写入到Redis数据库
    conn = get_redis_connection('carts')
    # pl = conn.pipeline()
    conn.hmset('carts_%s'%user.id, new_dict)
    # 将勾选状态同步到Redis数据库
    if new_add:
        conn.sadd('selected_%s'%user.id, *new_add)
    if new_remove:
        conn.srem('selected_%s'%user.id, *new_remove)

    response.delete_cookie('carts')

    return response