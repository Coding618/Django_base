"""
首页，详情页面
通常是先查询数据库的数据
然后再进行HTML页面的渲染

不管是 数据库的数据缓存 还是 HTML页面的渲染（特别是分类渲染，比较慢），会影响用户的体验
最好的体验
    用户 直接 访问 经过数据库查询，已经渲染的HTML页面  ---- 静态化

    经过数据查询，已经渲染的HTML页面，写入到指定目录
"""
# 函数功能： 数据库查询， 渲染HTML页面，然后把渲染的HTML写入到指定页面
import time
from utils.goods import get_categories
from apps.contents.models import ContentCategory

def generic_meiduo_index():
    print('---------------- %s -----------------------' % time.ctime())
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
    # 1. 加载渲染的模板
    from django.template import loader
    index_template = loader.get_template('index.html')

    # 2. 把数据给模板
    index_html_data = index_template.render(context)
    from meiduo_mall import settings
    import os
    # base_dir 的上一级
    # os.path.join(os.path.dirname(settings.BASE_DIR), 'front_end_pc/index.html')

    # 3. 把渲染好的HTML，写入到指定文件中
    file_path = os.path.join(os.path.dirname(settings.BASE_DIR), 'front_end_pc/index.html')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(index_html_data)
