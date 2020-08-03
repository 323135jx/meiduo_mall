import os
from distutils import loader

from goods.models import GoodsCategory,GoodsChannel


def get_breadcrumb(category_id):
    ret_dict = {}
    category = GoodsCategory.objects.get(pk=category_id)
    if not category.parent:
        ret_dict['cat1'] = category.name
    elif not category.parent.parent:
        ret_dict['cat1'] = category.parent.name
        ret_dict['cat2'] = category.name
    elif not category.parent.parent.parent:
        ret_dict['cat1'] = category.parent.parent.name
        ret_dict['cat2'] = category.parent.name
        ret_dict['cat3'] = category.name

    return ret_dict


def get_categories():
    categories = {}
    channels = GoodsChannel.objects.order_by(
        'group_id',
        'sequence'
    )
    # 便利所有的分类频道，构建以组号作为key的键值对
    for channel in channels:
        if channel.group_id not in categories:
            categories[channel.group_id] = {
                'channels': [],
                'sub_cats': [],
            }
        # 填充当前组中的一级分类
        cat1 = channel.category
        categories[channel.group_id]['channels'].append({
            'id': cat1.id,
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
                'id': cat2.id,
                'name': cat2.name,
                'sub_cats': cat3_list
            })
    return categories

def get_goods_and_spec(sku_id):
    pass


def generate_static_sku_detail_html(sku_id):

    categories = get_categories()
    goods, sku, specs = get_goods_and_spec(sku_id)
    context = {
        'categories': categories,
        'goods':goods,
        'specs':sku,
        'sku':specs,
    }

    template = loader.get.template('detail.html')
    html_text = template.render(context)

    from django.conf import settings
    file_path = os.path.join(settings.GENERATED_STATIC_HTML_FILES_DIR, 'goods%s.html')
    with open(file_path, 'w') as f:
        f.write(html_text)

