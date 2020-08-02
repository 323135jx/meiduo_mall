"""
该模块中实现首页静态化
"""
# loder: 读取或者加载模板文件
import os

from django.template import loader
from django.conf import settings

from contents.models import ContentCategory, Content
from goods.models import GoodsChannel,GoodsCategory

# 测试
def render_template_demo():

    # 1.get_template函数加载模板，传入一个模板文件名
    template = loader.get_template('demo.html')

    # 模板支持python基础类型，还支持传入模型对象
    context = {
        'name':'sophy',
        'age':18
    }

    # 2.填充动态数据--页面渲染
    html_text = template.render(context)

    # 3.把渲染完成的页面数据保存为静态文件
    with open('demo.html','w') as f:
        f.write(html_text)


def generate_static_index_html():

    # 频道分类数据
    categories = {}
    channels = GoodsChannel.objects.order_by(
        'group_id',
        'sequence'
    )
    # 便利所有的分类频道，构建以组号作为key的键值对
    for channel in channels:
        if channel.group_id not in categories:
            categories[channel.group_id]={
                'channels':[],
                'sub_cats':[],
            }
        # 填充当前组中的一级分类
        cat1 = channel.category
        categories[channel.group_id]['channels'].append({
            'id':cat1.id,
            'name': cat1.name,
            'url': channel.url
        })
        # 填充当前组中的二级分类信息
        cat2s = GoodsCategory.objects.filter(parent=cat1)

        for cat2 in cat2s:

            cat3_list = []

            cat3s = GoodsCategory.objects.filter(parent=cat2)
            for cat3 in cat3s:
                cat3_list.append({
                    'id': cat3.id,
                    'name': cat3.name
                })
            categories[channel.group_id]['sub_cats'].append({
                'id':cat2.id,
                'name':cat2.name,
                'sub_cats': cat3_list
            })
        # 填充当前组中的三级分类

    # 获取首页所有的信息
    # 页面广告数据
    contents = {}
    content_cats = ContentCategory.objects.all()
    for content_cat in content_cats:
        contents[content_cat.key] = Content.objects.filter(
            category=content_cat,
            status=True
        ).order_by('sequence')

    # context={
    #     'categories':categories,
    #     'contents':contents
    #
    # }
    context = {
        'categories': categories,
        'contents': contents
    }
    # =======广告实现渲染
    # 获取模板对象
    template = loader.get_template('index.html')

    # 2.传入模板参数
    html_text = template.render(context)

    filename = os.path.join(settings.GENERATED_STATIC_HTML_FILES_DIR, 'index.html')
    # 3.写入font_end_pc文件夹下的index.html静态文件
    with open(filename, 'w') as f:
        f.write(html_text)

