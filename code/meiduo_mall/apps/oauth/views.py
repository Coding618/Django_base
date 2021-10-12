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
        # 4. 根据 openid 进行判断
        # 5. 如果用户已经绑定用户信息， 直接登录
        # 6. 如果用户未绑定用户信息，需进行绑定用户信息，再进行登录

        pass

