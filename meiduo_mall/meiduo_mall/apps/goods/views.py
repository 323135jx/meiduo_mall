from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from .models import SKU, GoodsCategory
from django.core.paginator import Paginator,EmptyPage
from .utils import get_breadcrumb

# Create your views here.

# sku商品列表数据返回(分页)
from goods.models import SKU


# def get_breadcrumb(category_id):
#     ret_dict = {}
#     category = GoodsCategory.objects.get(pk=category_id)
#     if not category.parent:
#         ret_dict['cat1'] = category.name
#     elif not category.parent.parent:
#         ret_dict['cat1'] = category.parent.name
#         ret_dict['cat2'] = category.name
#     elif not category.parent.parent:
#         ret_dict['cat1'] = category.parent.parent.name
#         ret_dict['cat2'] = category.parent.name
#         ret_dict['cat3'] = category.name


class ListView(View):

    def get(self, request, category_id):
        page = request.GET.get('page')
        page_size = request.GET.get('page_size')
        ordering = request.GET.get('ordering')
        # １.获取ｓｋｕ商品数据－－排序
        skus = SKU.objects.filter(
            category_id=category_id,
            is_launched=True
        ).order_by(ordering)
        # 2.分页　－－　根据page和page-size分页
        try:
            paginator = Paginator(skus,page_size)

            cur_page = paginator.page(page)
        except EmptyPage as e:
            print(e)
            return JsonResponse({
                'code':400,
                'errmsg':'空页！'
            })
        ret_list = []
        for sku in cur_page:
            ret_list.append({
                'id':sku.id,
                'default_image_url':sku.default_image_url.url,
                'name':sku.name,
                'price':sku.price
            })

        # 返回响应

        return JsonResponse({
            'code':0,
            'errmsg':'ok',
            'breadcrumb':get_breadcrumb(category_id),
            'list':ret_list,
            'count':paginator.num_pages # 总页数
        })

# 热销商品
class HotGoodsView(View):
    def get(self, request, category_id):
        # １、获取热销商品(取销量最高的２个)
        skus = SKU.objects.filter(
            category_id=category_id,
            is_launched=True
        ).order_by('-sales')[:2]

        # ２、构建响应返回
        ret_list = []
        for sku in skus:
            ret_list.append({
                'id':sku.id,
                'name':sku.name,
                'price':sku.price,
                'default_image_url':sku.default_image_url.url
            })

        return JsonResponse({
            'code':0,
            'errmsg':'ok',
            'hot_skus':ret_list
        })

# 使用Haystack提供的搜索视图，实现搜索
# SerachView搜索视图基类，
# 请求方式:GET
# 请求路径: search/
# 请求参数: ?q=华为&page=1&page_size=3
# 响应数据：默认返回的是完整的html页面；不符合我们的借口需求，调整返回值
from haystack.views import SearchView
class MySerachView(SearchView):
    # 精确搜索

    def create_response(self):
        # 默认SearchView搜索视图逻辑

        context = self.get_context()

        sku_list = []
        for search_result in context['page'].object_list:
            sku = search_result.object
            sku_list.append({
                'id': sku.id,
                'name': sku.name,
                'price':sku.price,
                'default_image_url': sku.default_image_url.url,
                'searchkey':context['query'],
                'page_size':context['paginator'].per_page,
                'count':context['paginator'].count,
            })



        return JsonResponse(sku_list, safe=False)
