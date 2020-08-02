from haystack import indexes

# 被搜索的数据模型类
from .models import  SKU

# 针对ＥＳ搜索引擎库定义一个索引模型类
class SKUIndex(indexes.SearchIndex,indexes.Indexable):


    # text固定的字段
    # document = True表示text字段用户被检索字段
    # use_template = True使用模板来制定text字段中包含被检索的数据有哪些
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        # 获取被检索数据的模型类
        return SKU

    def index_queryset(self, using=None):
        # 返回被检索的查询集
        return self.get_model().objects.filter(is_launched=True)
