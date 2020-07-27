from django.shortcuts import render
from django.views import View
from django.http import JsonResponse

from .models import User

import logging
logger = logging.getLogger('django')

# Create your views here.

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

