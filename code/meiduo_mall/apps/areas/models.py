from django.db import models

# Create your models here.

class Area(models.Model):
    """
    省市区
    """
    name = models.CharField(max_length=20, verbose_name='名称')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL,
                               related_name='subs',
                               null=True, blank=True, verbose_name='上级行政区划')
    # related_name  关联模型的名字
    # 默认是   关联模型类名小写  _set  area_set
    # 我们可以通过， related_name  修改默认的名字， 现在修改为 sebs;
    class Meta:
        db_table = 'tb_areas'
        verbose_name = "省市区"
        verbose_name_plural = "省市区"

    def __str__(self):
        return self.name


"""
一张表 省市区
  id            name            parent_id
100000         广东省              null
100100          广州市             100000
100200          深圳市             100000
100101          南沙区             100100
100102          番禺区             100100
"""

