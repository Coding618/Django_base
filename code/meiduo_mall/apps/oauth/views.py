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