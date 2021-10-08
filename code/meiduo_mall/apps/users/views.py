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
import re
# 验证用户名是否重复
class UsernameCountView(View):

    def get(self, request, username):
        # 1. 接收用户名,判断一下
        # if not re.match('[a-zA-Z0-9_-]{5,20}',username):
        #     return JsonResponse({'code': 200, 'errmsg': '用户名不满足需求'})
        # 2. 根据用户名查询数据库
        count = User.objects.filter(username=username).count()
        # 3. 返回响应
        return JsonResponse({'code': 0, 'count': count, 'errmsg': 'OK'})
# 验证手机号码是否重复
class MobileCountView(View):
    def get(self, request, mobile):
        count = User.objects.filter(mobile=mobile).count()
        return JsonResponse({'code': 0, 'count': count, 'errmsg': 'OK'})
"""
需求分析：
前端：         当用户输入用户名、密码、确认密码，手机号，是否同意协议等信息后，会点击注册按钮
                前端后发送axios请求
后端：
    请求：          接收请求
    业务逻辑：       验证数据 ->  数据入库
    响应：           JSON {'code':0, 'errmsg': 'ok'}
                    0: 成功，  400：失败
    路由：     POST    register/
    步骤：
        1. 接收请求（POST ---- JSON）
        2. 获取数据 
        3. 验证数据
            3.1 用户名、密码、确认密码，手机号，是否同意协议，是否都有
            3.2 用户名满足规则，用户名不能重复
            3.3 密码满足规则
            3.4 确认密码和密码要一致
            3.5 手机号满足规则，手机号也不能重复
            3.6 需要同意协议
        4. 数据入库
        5. 返回响应
"""
import json
from django.contrib.auth import login
from django_redis import get_redis_connection
class RegisterView(View):

    def post(self, request):
        # 1. 接收请求（POST - --- JSON）
            # 接收短信验证码的参数

        body_bytes = request.body
        body_bytes.decode()
        body_dict = json.loads(body_bytes)
        # 2. 获取数据
        username = body_dict.get('username')
        password = body_dict.get('password')
        password2 = body_dict.get('password2')
        mobile = body_dict.get('mobile')
        sms_code = body_dict.get('sms_code')
        allow = body_dict.get('allow')

        sms_code_client = request.POST.get('sms_code')
        # 3. 验证数据
            # 3.1 用户名、密码、确认密码，手机号，是否同意协议，是否都有
        if not all([username, password, password2, mobile, allow]):
            return JsonResponse({'code':400, 'errmsg': '参数不全'})
            # 3.2 用户名满足规则，用户名不能重复
        if not re.match('[a-zA-Z0-9_-]{5,20}', username):
            return JsonResponse({'code': 400, 'errmsg': '用户名不满足规则'})            # 3.3 密码满足规则
            # if not re.match('[a-zA-Z0-9_-]{5,20}', password):
            #     return JsonResponse({'code': 400, 'errmsg': '密码不满足规则'})
            # # 3.4 确认密码和密码要一致
            # if password2 != password:
            #     return JsonResponse({'code': 400, 'errmsg': '确认密码不满足规则'})
            # # 3.5 手机号满足规则，手机号也不能重复
            # if not re.match('1[345789]\d{9}', mobile):
            #     return JsonResponse({'code': 400, 'errmsg': '手机号不满足规则'})
            # # 3.6 需要同意协议
            # if not re.match('[a-zA-Z0-9_-]{5,20}', allow):
            #     return JsonResponse({'code': 400, 'errmsg': '用户协议不满足规则'})
        # # 链接验证码redis
        # image_code = request.GET.get('image_code')
        # uuid = request.GET.get('image_code_id')
        # # 2.  验证参数
        # if not all([image_code, uuid]):
        #     return JsonResponse({'code': 400, 'errmsg': '参数不全'})

        redis_conn = get_redis_connection('code')
        # redis_image_code = redis_conn.get('img_%s' % uuid)
        # if redis_image_code is None:
        #     return JsonResponse({'code': 400, 'errmsg': '图片验证码失效'})
            # 删除图形验证码，防止恶意测试图形验证码
            # 删除图形验证码，防止恶意测试图形验证码
        # try:
        #     redis_cli.delete('img_%s' % uuid)
        # except Exception as e:
        #     logger.error(e)
        # 3.3 对比 验证码
        # if redis_image_code.decode().lower() != image_code.lower():
        #     return JsonResponse({'code': 400, 'errmsg': '图片验证码错误'})
        sms_code_server = redis_conn.get('sms_%s' % mobile)
        # 判断短信验证码是否过期
        if not sms_code_server:
            return JsonResponse({'code': 400, 'errmsg': '短信验证码失效'})
        # 对比输入的和服务端存储的短信验证码是否一致
        # if sms_code_client != sms_code_server.decode():
        if sms_code != sms_code_server.decode():
            return JsonResponse({'code': 400, 'errmsg': '短信验证码有误'})
        # 4. 数据入库
        try:
            # User.objects.create(username=username, password=password, mobile=mobile)
            user = User.objects.create_user(username=username, password=password, mobile=mobile)
            # 如何设置session信息
            # request.session['user_id']=user.id
            # Django提供了状态保持的方法
            login(request, user)
        except Exception as e:
            return JsonResponse({'code': 400, 'errmsg': '注册地区'})
        return JsonResponse({'code': 0, 'errmsg': '注册成功！！！'})
        # 5. 返回响应
"""
如果需求是注册成功后表示用户认证通过，那么此时可以在注册成功后实现状态保持！！（注册成功，即登录）
（注册成功，单独登录）
状态保持两种方式：
    在客户端信息使用cookie 
    在服务端信息使用session
"""

"""
登录
前端：
    当用户把用户名和密码输入完成之后，会点击登录按钮; 这个时候，前端应该发送一个axios请求

后端：
    请求    ： 接收数据，验证数据;
    业务逻辑 ：  验证用户名和密码是否正确，session
    响应     ：    返回 JSON 数据 0 成功；400 失败
    
    POST        /login/
步骤：
    1. 接受参数
    2. 验证参数
    3. 验证用户名和密码是否正确;
    4. session
    5. 判断是否记住登录
    6. 返回响应
"""
from django.contrib.auth import authenticate
from django.contrib.auth import login

class LoginView(View):

    def post(self, request):
        # 1. 接受参数
        data = json.loads(request.body.decode())
        username = data.get('username')
        password = data.get('password')
        remembered = data.get('remembered')
        # 2. 验证参数
        if not all([username, password]):
            return JsonResponse({'code': 400, 'errmsg': '参数不全'})
        if re.match('1[3-9]\d{9}', username):
            User.USERNAME_FIELD = 'mobile'
        else:
            User.USERNAME_FIELD = 'username'

        # 3. 验证用户名和密码是否正确;
        # User.objects.filter(username=username)
        # 方式2：
        # 如果用户名和密码正确，则返回 User 信息
        # 如果用户名和密码不正确， 则返回 None
        user = authenticate(username=username, password=password)
        if user is None:
            return JsonResponse({'code': 400, 'errmsg': '帐号或密码错误'})

        # 4. session
        login(request, user)
        # 5. 判断是否记住登录
        if remembered:
            # 记住登录 --2周
            request.session.set_expiry(None)
        else:
            # 不记住登录，浏览器关闭，session 过期
            request.session.set_expiry(0)
        # 6. 返回响应
        return JsonResponse({'code': 0, 'errmsg': 'ok'})
