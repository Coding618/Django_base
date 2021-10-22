from django.db import DatabaseError
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
"""
第三方登录的步骤：
1. QQ互联开发平台申请成为开发者（可不做）
2. QQ互联创建应用（可不做）
3. 按照文档开发（看稳定）

3.1 准备工作
    # QQ登录参数
    # 我们申请的客户端 id
    QQ_CLIENT_ID = '101474184'  appid
    # 我们申请的 客户密钥
    QQ_CLIENT_SECRET = ''   appkey
    # 我们申请时添加的：登录成功后，回调的路径
    QQ_REDIRECT_URI = 'http:wwww.meiduo.site:8080/oauth_callback.html'
3.2 设置 QQ登录的图标  目的：让我们点击QQ图标，来实现第三方登录       --前端已经实现了
3.3 根据auth2.0 来获取code 和 token                           --- 待实现
    对于应用而言，需要进行两步：
    1. 获取 Authorizaiton code
    2. 通过 Authorization Code 获取 Access Token
3.4 根据 token 换取 openid                                     ---- 待实现
    openid 是此网站上，唯一应用身份的标识，网站可将此 ID 进行存储，便于用户下次登录时，辨识身份，
    或者将其与用户在网站上的原有账户进行绑定;
把openid和用户信息进行 绑定

生成用户绑定链接 ---》 获取code ---》 获取token ---》 获取openid ---》 保存openid
"""

"""
生成用户绑定链接
前端： 当用户点击QQ登录图标的时候，前端发送一个 axios（Ajax）请求
后端:
    请求
    业务逻辑        调用QQLoginTool   生成跳转链接
    响应              返回跳转链接   {"code": 0, "qq_login_url":"http://XXX"}
    路由              GET     qq/authorization/
    步骤  
        # 1. 生成QQLoginTool    实例对象
        # 2. 调用对象方法生成跳转链接
        # 3. 返回响应
"""
from django.views import View
from QQLoginTool.QQtool import OAuthQQ
from meiduo_mall.settings import QQ_CLIENT_ID, QQ_CLIENT_SECRET, QQ_REDIRECT_URI
class QQLoginURLView(View):
    def get(self, request):
        # 1. 生成QQLoginTool    实例对象
        # client_id = None,         appid
        # client_secret = None,      appsecret
        # redirect_uri = None,      用户同意后，跳转的链接
        # state = None
        qq = OAuthQQ(client_id=QQ_CLIENT_ID,
                     client_secret=QQ_CLIENT_SECRET,
                     redirect_uri=QQ_REDIRECT_URI,
                     state=None)
        # 2. 调用对象方法生成跳转链接
        qq_login_url = qq.get_qq_url()
        # 3. 返回响应
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'login_url': qq_login_url})

"""
需求： 获取code， 通过code，获取token，通过token 再获取openid
前端：
    应该获取 用户同意之后，生成的code， 把code发送给后端
后端：
    请求：             获取code
    业务逻辑：           通过code 去获取 token，再通过token获取openid
                    根据 openid 进行判断
                    如果用户已经绑定用户信息， 直接登录
                    如果用户未绑定用户信息，需进行绑定用户信息，再进行登录
    响应：     
    路由：       GET       oauth_callback/?code=XXXXX
    步骤：
        1. 获取code
        2. 通过code 去获取 token，
        3. 再通过token获取openid
        4. 根据 openid 进行判断
        5. 如果用户已经绑定用户信息， 直接登录
        6. 如果用户未绑定用户信息，需进行绑定用户信息，再进行登录
"""
from apps.oauth.models import OAuthQQUser
from django.contrib.auth import login
import json
from apps.users.models import User
from apps.oauth.utils import check_access_token, generic_openid
class OauthQQView(View):

    def get(self, request):
        # 1. 获取code
        code = request.GET.get('code')
        if code is None:
            return JsonResponse({'code': 400, 'errmsg': '参数不全！！！'})
        # 2. 通过code 去获取 token，
        qq = OAuthQQ(client_id=QQ_CLIENT_ID,
                     client_secret=QQ_CLIENT_SECRET,
                     redirect_uri=QQ_REDIRECT_URI,
                     state=None)
        token = qq.get_access_token(code)
        # 3. 再通过token获取openid
        openid = qq.get_open_id(token)
        # 4. 根据 openid 进行查询判断
        try:
            qquser = OAuthQQUser.objects.get(openid=openid)
        except OAuthQQUser.DoesNotExist:
            # 不存在
            # 5. 如果没有绑定，则需要绑定
            """
            封装的思想：
                所谓的封装的思想其实就是把   一些实现了特定功能的代码， 封装成为一个函数（方法）
            封装的目的：
                解耦          当需求发生改变的时候，对代码的修改比较小，比较方便
            封装的步骤：
                1. 把要封装的代码，定义到一个函数（方法）中欧你
                2. 优化封装的代码
                3. 验证封装的代码
            """
            access_token = generic_openid(openid)
            response = JsonResponse({'code': 400, 'errmsg': 'ok', 'access_token': access_token})
            return response
        else:
            # 存在
            # 6. 如果绑定过，则直接登录
            # 6.1 设置 session
            login(request, qquser.user)
            # 6.2 设置 cookie
            response = JsonResponse({'code': 0, 'errmsg': 'ok'})
            response.set_cookie('username', qquser.user.username)

            return response
        # 5. 如果用户已经绑定用户信息， 直接登录
        # 6. 如果用户未绑定用户信息，需进行绑定用户信息，再进行登录

    def post(self, request):
        # 1. 接受请求
        data = json.loads(request.body.decode())
        # 2. 获取请求的参数      openid
        mobile = data.get('mobile')
        sms_code = data.get('sms_code')
        password = data.get('password')
        access_token = data.get('access_token')

        # 验证请求参数   省略详细步骤
        if not all([mobile, sms_code, password]):
            return JsonResponse({'code': 400, 'errmsg': '参数缺失！'})

        # 添加 access_token 解密
        openid = check_access_token(access_token)
        if openid is None:
            return JsonResponse({'code': 400, 'errmsg': '参数缺失'})
        # 3. 根据手机号进行用户信息的查询;
        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            # 不存在
            # 5. 查询到用户的手机号没有注册;   我们创建一个user信息，然后再绑定;
            user = User.objects.create_user(username=mobile,
                                            password=password,
                                            mobile=mobile)
            # response = JsonResponse({'code': 400, 'access_token': openid})
            # return response
        else:
            # 存在
            # 4. 查询到用户的手机号已经被注册了，判断密码是否正确;密码正确就可以直接保存（绑定） 用户和 openid 的信息
            if not user.check_password(password):
                return JsonResponse({'code': 400, 'errmsg': '密码错误或者帐号错误'})
        try:
            OAuthQQUser.objects.create(user=user, openid=openid)
        except DatabaseError:
            return JsonResponse({'code': 400, 'errmsg': '往数据库添加数据出错了'})

        # 6. 完成状态保持
        login(request, user)
        # 7. 返回响应
        response = JsonResponse({'code': 0, 'errmsg': 'ok'})

        response.set_cookie('username', user.username)

        return response

"""
需求：
    绑定帐号信息，点击保存的时候，需要做什么？
    QQ（openid）和 美多的帐号信息
    绑定时， 需要提交 手机、密码、验证码、openid
前端： 当用户输入，手机号、密码、短信验证码之后，就发送axios请求；  请求时，需要携带 mobile、password、sms_code、access_token(openid) 
后端：
    请求：         接受参数，获取请求参数
    业务逻辑：       绑定，完成状态保持
    响应：         返回，code = 0, 跳转到首页
    路由：         POST       oauth_callback/
    步骤:
        # 1. 接受请求
        # 2. 获取请求的参数      openid
        # 3. 根据手机号进行用户信息的查询;
        # 4. 查询到用户的手机号已经被注册了，判断密码是否正确;密码正确就可以直接保存（绑定） 用户和 openid 的信息
        # 5. 查询到用户的手机号没有注册;   我们创建一个user信息，然后再绑定;
        # 6. 完成状态保持
        # 7. 返回响应
"""

############### itsdangerous 的基本使用 #########################
# itsdangerous 就是为了数据加密的
## 加密
# 1. 导入 itsdangerous 的类
from meiduo_mall import settings
from  itsdangerous import TimedJSONWebSignatureSerializer as Serializer
# 2. 创建类的实例对象
# secret_key,       密钥
# expires_in=None   过期时间
s = Serializer(secret_key=settings.SECRET_KEY, expires_in=3600)
# 3. 加密数据
token = s.dumps({'openid':'1234567890'})
# b'eyJhbGciOiJIUzUxMiIsImlhdCI6MTYzNDcwNzcxMiwiZXhwIjoxNjM0NzExMzEyfQ.eyJvcGVuaWQiOiIxMjM0NTY3ODkwIn0.X3FYZCj-xJz7NnuyYtWxm2R2pgDu2X4mMtP1S4uTnE7zYHttfPlsenMQn9Lq14N7dhkl-Iv-YOrPgP3cjkicGQ'

## 解密
from meiduo_mall import settings
from  itsdangerous import TimedJSONWebSignatureSerializer as Serializer
s = Serializer(secret_key=settings.SECRET_KEY, expires_in=3600)
s.loads(token)
# {'openid': '1234567890'}