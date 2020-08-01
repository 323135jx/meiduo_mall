

from django.core.files.storage import Storage
from django.conf import settings


class FastDFSStorage(Storage):

    def open(self, name, mode='rb'):
        return None

    def save(self, name, content, max_length=None):
        pass

    def url(self, name):
        # 该函数返回到结果就是， ImageField.url属性的出的结果

        return settings.FDFS_URL + name
