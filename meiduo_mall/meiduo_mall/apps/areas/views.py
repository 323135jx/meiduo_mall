from django.shortcuts import render
from .models import Area
from django.views import View
from django.core.cache import cache
from django.http import JsonResponse
# Create your views here.

class ProvinceAreasView(View):
    """省级地区"""

    def get(self, request):

        # 有限判断缓存中有没有数据
        p_list = cache.get('province_list')

        if not p_list:
            # 把省信息按照格式返回
            # 1.读取模型类查询集
            provinces = Area.objects.filter(
                parent=None
            )
            # 2.把所有的模型类对象，转换成字典{id, name}
            p_list = []
            for province in provinces:
                p_list.append({
                    'id':province.id,
                    'name':province.name
                })

            # 读取mysql省数据之后，写入缓存
            # cache模块写入缓存是key-value形式
            cache.set('province_list', p_list, 3600)


        # 3. 构造返回响应
        return JsonResponse({
            'code':0,
            'errmsg':'ok',
            'province_list':p_list
        })


# 获取可选市区信息
class SubAreasView(View):

    def get(self, request, pk):
        # 路径中传入的pk
        # 1.pk是省的逐渐，请求所有市信息
        # 2.pk是市的逐渐，请求所有区信息

        sub_data = cache.get('sub_area_%s'%pk)

        if not sub_data:
            # 当前pk滤出的父级行政区对象
            p_area = Area.objects.get(
                pk = pk
            )

            # 当前父级行政对象关联的多个子级行政区
            subs = Area.objects.filter(
                parent_id = pk
            )

            sub_list = []
            for sub in subs:
                # sub是子级行政区对象
                sub_list.append({
                    'id':sub.id,
                    'name':sub.name,
                })

            sub_data = {
                'id': p_area.id,
                'name':p_area.name,
                'subs':sub_list
            }

            cache.set('sub_area_%s'%pk, sub_data, 3600)

        return JsonResponse({
            'code': 0,
            'errmsg': 'ok',
            'sub_data': sub_data
        })

