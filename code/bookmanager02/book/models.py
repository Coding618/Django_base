from django.db import models

# Create your models here.

class BookInfo(models.Model):
    name = models.CharField(max_length=10, unique=True, verbose_name='名称')
    pub_date = models.DateField(null=True, verbose_name='发布日期')
    readcount = models.IntegerField(default=0, verbose_name='阅读量')
    commentcount = models.IntegerField(default=0, verbose_name='评论量')
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除')

    # 一对多的关系模型， 系统添加一个 关联模型类名小写_set
    # peopleinfo_set = [PeopleInfo, PeopleInfo, ...]
    class Mate:
        db_table = 'bookinfo' # 修改表的名字
        verbose_name = '书籍管理' # admin站点的使用

    def __str__(self):
        return self.name

class PeopleInfo(models.Model):
    GENDER_CHOICES = {
        (1, 'male'),
        (2, 'female')
    }
    name = models.CharField(max_length=10, unique=True, verbose_name='名称')
    gender = models.SmallIntegerField(choices=GENDER_CHOICES, default=1, verbose_name='性别')
    description = models.CharField(max_length=100, null=100, verbose_name='描述信息')
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除')
    # 主表  和  从表
    #  1   对   多
    # 书籍      人物
    book = models.ForeignKey(BookInfo, models.CASCADE, verbose_name='图书')
    # book=BookInfo()
    class Meta:
        db_table = 'peopleinfo'
        verbose_name = '人物信息'
    def __str__(self):
        return self.name
