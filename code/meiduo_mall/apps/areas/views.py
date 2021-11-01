from django.shortcuts import render

# Create your views here.
from django.views import View

"""
需求：
    获取省份信息
前端：
    当页面加载的时候，会发送axios请求，来获取，省份信息
后端：
    请求：             不需要请求参数
    业务逻辑：           查询省份信息
    响应：             JSON
    路由：             areas/ 
    步骤：
        1. 查询省份信息
        将对象转换为字典数据
        2. 返回响应

"""
from apps.areas.models import Area
from django.http import JsonResponse
from django.core.cache import cache
class AreaView(View):
    def get(self, request):
        # 先查缓存数据
        province_list = cache.get('province')
        if province_list is None:
            # 1. 查询省份信息
            provinces = Area.objects.filter(parent=None)

            # 2. 将对象转换为字典数据
            province_list = []
            for province in provinces:
                province_list.append({
                    'id': province.id,
                    'name': province.name
                })
            # cache.set(key, value, expire)
            cache.set('province', province_list, 24*3600)
        # 3. 返回响应
        return JsonResponse({'code': 0, 'errmsg': 'OK!', 'province_list': province_list})

"""
需求：
    获取市、区县级信息
前端：
    当页面加载的时候，会发送axios请求，来获取，下一级的信息
后端：
    请求：             需要传递省份id、市的id
    业务逻辑：           根据id，查询信息，将查询结果转换为字典列表
    响应：             JSON
    路由：             areas/id
    步骤：
        1. 获取省份id、市id，查询信息
        2. 将对象转换为字典数据
        3. 返回响应
"""
class SubAreaView(View):
    def get(self, request, id):
        # 1. 获取省份id、市id，查询信息
        # Area.objects.filter(parent_id=id)
        # Area.objects.filter(parent=id)
        # 先获取缓存
        data_list = cache.get('city:%s' % id)
        if data_list is None:
            up_level = Area.objects.get(id=id)
            down_level = up_level.subs.all()
            # 2. 将对象转换为字典数据
            data_list = []
            for item in down_level:
                data_list.append({
                    'id': item.id,
                    'name': item.name
                     })
            # 缓存
            cache.set('city:%s' % id, data_list, 24*3600)
        # 3. 返回响应
        return JsonResponse({'code': 0, 'errmsg': 'ok~', 'sub_data': {'subs': data_list}})
"""
日活
注册用户        1亿
日活用户        1%      1百万
下单比例        1%      1W  10000
新增地址的概率   1%      100W  300次    2次
不经常变化的数据    我们最好缓存到redis（内容）中，减少数据库的查询 
"""