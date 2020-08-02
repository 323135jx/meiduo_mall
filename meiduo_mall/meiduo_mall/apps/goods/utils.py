from goods.models import GoodsCategory


def get_breadcrumb(category_id):
    ret_dict = {}
    category = GoodsCategory.objects.get(pk=category_id)
    if not category.parent:
        ret_dict['cat1'] = category.name
    elif not category.parent.parent:
        ret_dict['cat1'] = category.parent.name
        ret_dict['cat2'] = category.name
    elif not category.parent.parent:
        ret_dict['cat1'] = category.parent.parent.name
        ret_dict['cat2'] = category.parent.name
        ret_dict['cat3'] = category.name
