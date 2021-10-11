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

