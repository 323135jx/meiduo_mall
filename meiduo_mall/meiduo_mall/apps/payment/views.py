from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from alipay import AliPay
import os
from orders.models import OrderInfo
from django.conf import settings
import logging

from payment.models import Payment

logger = logging.getLogger('django')

# Create your views here.

class PaymentView(View):
    """订单支付功能"""

    def get(self, request, order_id):
        # 查询要支付的订单
        user = request.user

        try:
            order = OrderInfo.objects.get(order_id=order_id,user=user,status=OrderInfo.ORDER_STATUS_ENUM['UNPAID'])
        except OrderInfo.DoesNotExist as e:
            logger.error(e)
            return JsonResponse({'code':400,'errmsg':'order_id有误'}, status=400)


        # 创建支付宝支付对象
        alipay = AliPay(
            appid = settings.ALIPAY_APPID,
            app_notify_url = None,  # 默认回调url,异步回调，支付成功之后，阿里后台主动请求美多
            app_private_key_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "keys/app_private_key.pem"),
            alipay_public_key_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "keys/alipay_public_key.pem"),
            sign_type = "RSA2",
            debug = settings.ALIPAY_DEBUG
        )

        # 生成登录支付宝功能
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no = order_id,
            total_amount = str(order.total_amount),
            subject = "美多商城%s"%order_id,
            return_url = settings.ALIPAY_RETURN_URL
        )

        # 响应
        alipay_url = settings.ALIPAY_URL + "?" + order_string
        return JsonResponse({'code':0,'errmsg':'ok','alipay_url':alipay_url})

class PaymentStatusView(View):
    """保存订单支付效果"""

    def put(self, request):
        # 1.获取参数
        # 获取前端传入的请求参数

        data = request.GET.dict()

        # 获取并从请求参数中剔除signature
        signature = data.pop('sign')


        # 2.处理参数
        # 创建支付宝支付对象
        alipay = AliPay(
            appid=settings.ALIPAY_APPID,
            app_notify_url=None,
            app_private_key_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "keys/app_private_key.pem"),
            alipay_public_key_path=os.path.join(os.path.dirname(os.path.abspath(__file__)),"keys/alipay_public_key.pem"),
            sign_type="RSA2",
            debug=settings.ALIPAY_DEBUG
        )

        # 校验这个重定向是否是alipay重定向过来的
        success = alipay.verify(data=data, signature=signature)

        if success:
            # 读取order_id
            order_id = data.get('out_trade_no')
            # 读取支付宝流水号
            trade_id = data.get('trade_no')
            # 保存Payment模型类数据
            Payment.objects.create(
                order_id=order_id,
                trade_id=trade_id
            )

            OrderInfo.objects.filter(order_id = order_id,status = OrderInfo.ORDER_STATUS_ENUM['UNPAID']).update(status=OrderInfo.ORDER_STATUS_ENUM['UNRECEIVED'])

            return JsonResponse({'code':0,'errmsg':'ok','trade_id':trade_id})
        else:
            # 订单支付失败，重定向回我的订单
            return JsonResponse({'code':400,'errmsg':'支付失败'})


        #　3.返回响应