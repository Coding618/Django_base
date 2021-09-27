from django.shortcuts import render

# Create your views here.
"""
需求分析：根据页面的功能，哪些问题，需要后端交互实现;
如何确定  哪些功能需要 和 后端进行交互呢？
        1. 经验
        2. 关注类似网站的相似功能
"""
"""
判断用户是否重复的功能：
前端：     当用户输入用户名之后，失去焦点，发送一个 axios(ajax)请求

后端：     思路
    请求：         接收用户名
    业务逻辑：       根据用户名查询数据库，如果查询结果数量为0,则说明没有注册
                    如果查询结果数量大于1,说明注册了
    响应：         JSON
                    {code:0, count:0/1, errmsg:ok}
    路由：  GET    /usernames/<username>/count/
    步骤：
        1. 接收用户名
        2. 根据用户名查询数据库
        3. 返回响应
"""
from django.views import View
from apps.users.models import User
from django.http import JsonResponse

class UsernameCountView(View):

    def get(self, request, username):
        # 1. 接收用户名
        # 2. 根据用户名查询数据库
        count = User.objects.filter(username=username).count()
        # 3. 返回响应
        return JsonResponse({'code': 0, 'count': count, 'errmsg': 'OK'})