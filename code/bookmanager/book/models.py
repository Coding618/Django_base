from django.db import models

# Create your models here.
class BookInfo(models.Model):
    # 默认创建id
    name = models.CharField(max_length=10)


class PeopleInfo(models.Model):
    name = models.CharField(max_length=10)
    gender = models.BooleanField()
    # 外键： 人物属于哪本书
    book = models.ForeignKey(BookInfo, on_delete=models.CASCADE)


