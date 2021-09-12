from django.http import HttpResponse
from django.shortcuts import render
from book.models import BookInfo
# Create your views here.

def index(request):

    book = BookInfo.objects.all()
    print(book)
    return HttpResponse('index')

#########  insert 数据 ################
from book.models import BookInfo

book = BookInfo(
    name='Django',
    pub_date='2000-01-01',
    readcount=10
)
book.save()

# 方式2
# objects  -- 实现增删改查
BookInfo.objects.create(
    name='测试开发入门',
    pub_date='2020-2-1',
    readcount=100
)

########## 修改参数  #########

## 方式一
# select * from book_bookinfo where id=6;
book = BookInfo.objects.get(id=6)
book.name='爬虫入门'
book.save()   # 执行保存操作，才会将修改的结果，保存到数据库中欧你
## 方式二   使用 filter 方法去执行
book = BookInfo.objects.filter(id=5).update(name='大数据开发入门',commentcount=999)


########### 删除数据 ####################
book=BookInfo.objects.get(id=6)
book.delete()

book=BookInfo.objects.get(id=5).delete()
book=BookInfo.objects.filter(id=5).delete()


############## 查询 ##################
# get  单一结果
try:
    booK=BookInfo.objects.get(id=6)
except BookInfo.DoesNotExist:
    print("查询结果不存在")
# all  列表
book=BookInfo.objects.all()
from book.models import PeopleInfo
PeopleInfo.objects.all()
# count 查询结果数量

BookInfo.objects.all().count()
BookInfo.objects.count()

############### 过滤查询 #############################

# filter   过滤出多个结果
# exclude  排查符合条件下的多个结果
# get      过滤单一结果
# 模型类名.objects.filter(属性名__运算符=参数值)     获取 n 个结果， n=1,2,3,...
# 模型类名.objects.exclude(属性名__运算符=参数值)    获取 n 个结果， n=1,2,3,...
# 模型类名.objects.get(属性名__运算符=参数值)        获取 1 个结果， 或者 异常


# 查询编号为1的图书
BookInfo.objects.get(id=1)          # 简写形式  (属性名=值)
BookInfo.objects.get(id__exact=1)   # 完整形式
BookInfo.objects.get(pk=1)

BookInfo.objects.get(id=1)
BookInfo.objects.filter(id=1)
# 查询书名包含'湖'的图书
BookInfo.objects.filter(name__contains='湖')

# 查询书名以'部'结尾的图书
BookInfo.objects.filter(name__endswith='部')

# 查询书名为空的图书
BookInfo.objects.filter(name__isnull=True)
# 查询编号为1或3或5的图书
BookInfo.objects.filter(id__in=[1,3,5])
# 查询编号大于3的图书
# 大于    gt    great
# 大于等于 gte      equal
# 小于    lt      little  less then
# 小于等于 lte
BookInfo.objects.filter(id__gt=3)

# 查询编号不等于3的图书
BookInfo.objects.exclude(id=3)

# 查询1980年发表的图书
BookInfo.objects.filter(pub_date__year='1980')
# 查询1990年1月1日后发表的图书
BookInfo.objects.filter(pub_date__gt='1990-01-01')
BookInfo.objects.filter(id__gt=3)
# 查询阅读量大于评论量的书籍
from django.db.models import F
BookInfo.objects.filter(readcount__gt=F('commentcount'))
# 查询阅读量大于2倍评论量的图书
BookInfo.objects.filter(readcount__gte=F('commentcount')*2)
# 并且查询
# 查询阅读量大于20, 并且编号小于=3的图书
BookInfo.objects.filter(readcount__gte=20)
BookInfo.objects.filter(readcount__gte=20).filter(id__lte=3)
# 或者
BookInfo.objects.filter(readcount__gte=20, id__lte=3)
# 或者查询
# 查询阅读量大于20, 或者编号小于=3的图书
BookInfo.objects.filter(readcount__gte=20)
from django.db.models import Q
BookInfo.objects.filter(Q(readcount__gte=20) | Q(id__lte=3))

#############  聚合函数 #########################
from django.db.models import Sum, Max, Min, Avg, Count
# 聚合函数 模型名.objects.aggregate(XXX('字段名'))
BookInfo.objects.aggregate(Sum('readcount'))

BookInfo.objects.order_by('readcount')

# 查询书籍为1的所有人物信息
# book=BookInfo.objects.filter(id=1)
people = PeopleInfo.objects.get(id=1)
people.book.name
people.book.readcount


############# 关联过滤查询 ###############
# 查询图书，要求图书人物为"郭靖"
BookInfo.objects.filter(peopleinfo__name__exact='郭靖')
BookInfo.objects.filter(peopleinfo__name='郭靖')
# 查询图书，要求图书中人物的描述包含"八"
BookInfo.objects.filter(peopleinfo__description__contains='八')

# 查询图书，要求图书人物为"郭靖"
BookInfo.objects.filter(peopleinfo__name__exact='郭靖')

# 查询书名为“天龙八部”的所有人物
PeopleInfo.objects.filter(book__name='天龙八部')

# 查询图书阅读量大于30的所有人物
PeopleInfo.objects.filter(book__readcount__gt=30)

# 将硬盘的数据放到内存中，称作缓存  例如 redis