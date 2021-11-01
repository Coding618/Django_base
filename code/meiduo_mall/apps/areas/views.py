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
class AreaView(View):
    def get(self, request):
        # 1. 查询省份信息
        provinces = Area.objects.filter(parent=None)

        # 2. 将对象转换为字典数据
        parernt_list = []
        for province in provinces:
            parernt_list.append({
                'id': province.id,
                'name': province.name
            })
        # 3. 返回响应
        return JsonResponse({'code': 0, 'errmsg': 'OK!', 'province_list': parernt_list})

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

        up_level = Area.objects.get(id=id)
        down_level = up_level.subs.all()
        # 2. 将对象转换为字典数据
        data_list = []
        for item in down_level:
            data_list.append({
                'id': item.id,
                'name': item.name
                 })
        # 3. 返回响应
        return JsonResponse({'code': 0, 'errmsg': 'ok~', 'sub_data': {'subs': data_list}})
