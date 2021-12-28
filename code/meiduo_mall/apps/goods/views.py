from django.shortcuts import render

# Create your views here.
"""
关于模型的分析
1. 根据页面效果，尽量多的分析字段
2. 去分析是保存在一个表中，还是多个表中（多举例说明）

分析表的关系的时候，最多不要超过3个表
多对多 （一般是3个表）

学生 和 老师

学生表
stu_id      stu_name
100             张三
200             李四

老师表
teacher_id  teacher_name
666             牛老师
999             齐老师

第三张表
stu_id      teacher_id
100             666
100             999
200             666
200             999
商品day01     模型的分析 --》   Fastdfs（用于保存图片，视频等文件 ） --》为了部署Fdfs

"""
############### 上传图片的代码 ##########################
# from fdfs_client.client import Fdfs_client
#
# # 1.创建客户端
# # 修改加载配置文件的路径
# client = Fdfs_client('utils/fastdfs/client.conf')
#
# # 2.上传图片
# # 图片的绝对路径
# client.upload_by_filename('/home/sherlock/Pictures/插件截图.png')

"""
{'Group name': 'group1', 'Remote file_id': 'group1/M00/00/00/wKgfg2GbC9-ASAhtAAEr3bICYZQ204.png', 
'Status': 'Upload successed.', 'Local file name': '/home/sherlock/Pictures/插件截图.png', 
'Uploaded size': '74.00KB', 'Storage IP': '192.168.31.131'}
"""
# 3.获取file_id, upload_by_filename 上传成功会返回字典数据
# 字典数据中，有 file_id

from django.views import View
from utils.goods import get_categories
from apps.contents.models import ContentCategory
class IndexView(View):

    def get(self, request):
        """
        首页数据分为2部分
        1部分是 商品分类数据
        2部分是 广告数据
        :param request:
        :return:
        """
        # 1.商品分类数据
        categories = get_categories()
        # 2.广告数据
        contents = {}
        content_categories = ContentCategory.objects.all()
        for cat in content_categories:
            contents[cat.key] = cat.content_set.filter(status=True).order_by('sequence')

        context = {
            'categories': categories,
            'contents': contents,
        }
        return render(request, 'index.html', context)
