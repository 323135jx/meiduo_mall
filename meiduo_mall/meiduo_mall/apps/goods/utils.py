import os
from distutils import loader

from goods.models import GoodsCategory, GoodsChannel, SKU, SKUSpecification, SPUSpecification, SpecificationOption

from copy import deepcopy

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
    # 当前SKU商品
    sku = SKU.objects.get(pk=sku_id)
    sku.default_image_url = sku.default_image_url.url

    # 记录当前sku的选项组合
    cur_sku_spec_options = SKUSpecification.objects.filter(sku=sku).order_by('spec_id')
    cur_sku_options = [] # [1,4,7]
    for temp in cur_sku_spec_options:
        # temp是SKUSpecofocation中间表对象
        cur_sku_spec_options.append(temp.option_id)

    # spu对象(spu商品)
    goods = sku.spu
    # 罗列出和当前sku同类的所有商品的选项和商品id的映射关系
    # {(1,4,7):1, (1,3,7):2}
    sku_options_mapping = {}
    skus = SKU.objects.filter(spu=goods)
    for temp_sku in skus:
        #  temp_sku:每一个sku商品对象
        sku_spec_options = SKUSpecification.objects.filter(sku=temp_sku).order_by('spec_id')
        sku_options = []
        for temp in sku_spec_options:
            sku_options.append(temp.option_id)  # [1,4,7]
        sku_options_mapping[tuple(sku_options)] = temp_sku.id   #{(1,4,7):1}

        # specs当前页面需要渲染的所有规格
        specs = SPUSpecification.objects.filter(spu=goods).order_by('id')
        for index, spec in enumerate(specs):
            # spec每一个规格对象
            options = SpecificationOption.objects.filter(spec=spec)
            # 每一次选项规格的时候，准备一个当前sku的选项组合列表，便于后续使用
            temp_list = deepcopy(cur_sku_options)   # [1,4,7]
            for option in options:
                # 每一个选项,动态添加一个sku_id值,来确定这个选项是否属于当前sku商品
                temp_list[index] = option.id    # [1,3,7] ---> sku_id?
                option.sku_id = sku_options_mapping.get(tuple(temp_list))   # 找到对应选项组合的sku_id

            # 在每一个规格对象中动态添加一个属性spec_options来记录当前规格有哪些选项
            spec.spec_options = options

        return goods, sku, specs



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


#