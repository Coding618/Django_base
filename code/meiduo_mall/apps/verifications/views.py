from django.http import HttpResponse
from django.shortcuts import render
"""
前端：
    拼接一个 url， 然后给 img， img会发起请求
    url=http://mp-meiduo-python.itheima.net/image_codes/269c7e6a-ef90-4a2c-acbe-b9e8b58c75bf/
    
    url=http://ip:port/image_code/uuid/
后端：
    请求          接收路由中的 uuid
    业务逻辑        生成图片验证码和图片二进制，通过 redis 把图片验证码保存起来;
    响应          返回图片二进制
    
    路由：         GET     image_code/uuid/
    步骤：
            1.接收路由中的 uuid
            2.生成图片验证码和图片二进制
            3.通过 redis 把图片验证码保存起来
            4.返回图片二进制
        
"""
# Create your views here.
from django.views import View
from libs.captcha.captcha import captcha
from django_redis import get_redis_connection
class ImageCodeView(View):

    def get(self, request, uuid):
        # 1. 接收路由中的 uuid
        # 2. 生成图片验证码和图片二进制
        # text: 图片验证码的内容    例如：XYZZ
        # image: 图片二进制
        text, image = captcha.generate_captcha()
        # 3. 通过 redis 把图片验证码保存起来
        # 3.1 进行redis的链接
        redis_cli = get_redis_connection('code')
        # 3.2 设置过期时间
        redis_cli.setex(uuid, 60*2, text)
        # 4. 返回图片二进制,不能返回二进制
        # content_type 的语法形式，大类/小类
        # content_type  (MIME 类型)
        # 图片： image/jpge,   image/gif, image/png
        return HttpResponse(image, content_type='image/ipeg')