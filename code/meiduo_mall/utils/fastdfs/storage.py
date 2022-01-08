"""
https://docs.djangoproject.com/en/1.11/howto/custom-file-storage/

1. 您的自定义存储系统必须是 的子类django.core.files.storage.Storage
2. Django 必须能够在没有任何参数的情况下实例化您的存储系统。这意味着任何设置都应该取自 django.conf.settings：
3. 您的存储类必须实现_open()和_save()方法, 以及适合您的存储类的任何其他方法
    url
"""
from django.core.files.storage import Storage
class MyStorage(Storage):
    def _open(self, name, mode='rb'):
        """Retrieve the specified file from storage."""
        pass

    def _save(self, name, content, max_length=None):
        pass

    def url(self, name):
        return 'http://192.168.31.132:8888/' + name  # ccw
        # return "http://192.168.1.102:8888/" + name     # my

