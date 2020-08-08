from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from users.models import Address
from goods.models import SKU
from django_redis import get_redis_connection

# Create your views here.
from decimal import Decimal
from django.utils import timezone

from meiduo_mall.utils.views import login_required
from .models import *

import json
import logging
logger = logging.getLogger('django')


class OrderSettlementView(View):
    """结算清单"""
    # 获取登录用户

    @method_decorator(login_required)
    def get(self,request):

        # 1.获取数据
        user = request.user
        # 1.1 查询地址
        try:
            addresses = Address.objects.filter(user=user,is_deleted=False)
        except Exception as e:
            # 如果地址为空,渲染时会调转到地址编辑页面
            addresses = None

        # 查询购物车
        conn = get_redis_connection('carts')

        cart_str = conn.hgetall('carts_%s'%user.id)
        cart_selected = conn.smembers('selected_%s'%user.id)
        cart = {}
        for sku_id in cart_selected:
            cart[int(sku_id)] = int(cart_str[sku_id])

        # 构建商品信息数据
        sku_list = []
        skus = SKU.objects.filter(id__in=cart.keys())
        for sku in skus:
            sku_list.append({
                'id':sku.id,
                'name':sku.name,
                'default_image_url':sku.default_image_url.url,
                'count':cart[sku.id],
                'price':sku.price,
            })

        # 补充运费
        freight = Decimal('10.00')

        # 其他信息构建
        addresses_list = []
        for address in addresses:
            addresses_list.append({
                "id":address.id,
                "province":address.province.name,
                "city":address.city.name,
                "district":address.district.name,
                "place":address.place,
                "mobile":address.mobile,
                "receiver":address.receiver,
            })

        # 渲染界面
        context ={
            'addresses': addresses_list,
            'skus':sku_list,
            'freight':freight
        }
        # 2.处理数据
        # 3.构建响应
        return JsonResponse({
            'code':0,
            'errmsg':'ok',
            'context':context
        })

from django.utils import timezone
class OrderCommitView(View):
    """提交订单"""

    @method_decorator(login_required)
    def post(self, request):
        """提交订单"""
        # 1.获取数据
        # 获取当前需要的订单数据
        user = request.user
        json_dict = json.loads(request.body.decode())
        address_id = json_dict.get('address_id')
        pay_method = json_dict.get('pay_method')

        # 2.验证数据
        if not all([address_id,pay_method]):
            return JsonResponse({'code':400,'errmsg':'您的任务还差些！'})

        # 判断address_id是否合法
        try:
            address = Address.objects.get(pk=address_id)
        except Address.DoesNotExist as e:
            logger.error(e)
            return JsonResponse({'code':400,'errmsg':'小爬虫你被抓住了'})
        if pay_method not in [OrderInfo.PAY_METHODS_ENUM['CASH'],OrderInfo.PAY_METHODS_ENUM['ALIPAY']]:
            return JsonResponse({'code':400,'errmsg':'休想骗过我,爬虫生来就是被践踏'})

        # 3.处理数据
        # 生成订单编号
        order_id = timezone.localtime().strftime('%Y%m%d%H%M%S') + ('%09d'%user.id)
        # 保存订单基本信息　OrderInfo
        # 从redis读取购物车中被勾选的商品信息
        conn = get_redis_connection('carts')
        cart_dict = conn.hgetall('carts_%s'%user.id)
        cart_selected = conn.smembers('selected_%s'%user.id)
        carts = {}

        for sku_id in cart_selected:
            carts[int(sku_id)] = int(cart_dict[sku_id])

        # 遍历购物车中被勾选的商品信息
        sku_ids = carts.keys()

        with transaction.atomic():
            # 关键的时间阶段－order订单新建节点

            save_id = transaction.savepoint()   #　事务执行保存点
            order = OrderInfo.objects.create(
                order_id=order_id,
                user=user,
                address=address,
                total_count=0,
                total_amount=Decimal('0'),
                freight=Decimal('10.00'),
                pay_method=pay_method,
                status=OrderInfo.ORDER_STATUS_ENUM['UNPAID']
                if pay_method == OrderInfo.PAY_METHODS_ENUM['ALIPAY']
                else OrderInfo.ORDER_STATUS_ENUM['UNSEND'])

            # 遍历购物车中被勾选的商品信息
            for sku_id in sku_ids:

                    # 增加一个乐观锁
                while True:

                    sku = SKU.objects.get(id=sku_id)
                    # 读取原始库存
                    origin_stock = sku.stock
                    origin_sales = sku.sales

                    sku_count = carts[sku.id]
                    if sku_count > sku.stock:
                        # 由于库存不足,整个事务会回滚到订单新建之前的节点
                        transaction.savepoint_rollback(save_id)
                        return JsonResponse({'code':400,'errmsg':'库存不足'})

                    # # SKU减少库存,增加销量
                    # sku.stock -= sku_count
                    # sku.sales += sku_count
                    # sku.save()

                    # 增加的代码：乐观锁更新库存和销量
                    # 计算差值
                    new_stock = origin_stock - sku_count
                    new_sales = origin_sales + sku_count
                    result = SKU.objects.filter(id=sku_id,stock=origin_stock).update(stock=new_stock,sales=new_sales)
                    # 如果下单失败，但是库存足够是，
                    # 继续下单,知道下单成功或者库存不足为止
                    if result == 0:
                        continue

                    # 修改SPU销量
                    sku.spu.sales += sku_count
                    sku.spu.save()

                    # 保存订单商品信息
                    OrderGoods.objects.create(
                        order = order,
                        sku = sku,
                        count = sku_count,
                        price = sku.price
                    )

                    # 保存商品订单中总数量和总价
                    order.total_count += sku_count
                    order.total_amount += (sku_count * sku.price)
                    break

            # 添加邮费和保存订单信息
            order.total_amount += order.freight
            order.save()
            transaction.savepoint_commit(save_id)

        # 清楚购物车中已结算的商品
        conn.hdel('carts_%s'%user.id, *cart_selected)
        conn.srem('selected_%s'%user.id, *cart_selected)


        # 4.返回响应

        return JsonResponse({
            'code':0,
            'errmsg':'下单成功',
            'order_id':order.order_id
        })


