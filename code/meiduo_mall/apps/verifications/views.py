import logging

from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
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
        redis_cli.setex('img_%s' % uuid, 60*2, text)
        # 4. 返回图片二进制,不能返回二进制
        # content_type 的语法形式，大类/小类
        # content_type  (MIME 类型)
        # 图片： image/jpge,   image/gif, image/png
        return HttpResponse(image, content_type='image/ipge')
"""
1.注册 
我们提供免费开发测试，【免费开发测试前，请先 注册 成为平台用户】。

2.绑定测试号
免费开发测试需要在"控制台—管理—号码管理—测试号码"绑定 测试号码 。

3. 开发测试
开发测试过程请参考 短信业务接口 及 Demo示例 / sdk参考（新版）示例。Java环境安装请参考"新版sdk"。
4.免费开发测试注意事项
    4.1.免费开发测试需要使用到"控制台首页"，开发者主账户相关信息，如主账号、应用ID等。
    
    4.2.免费开发测试使用的模板ID为1，具体内容：【云通讯】您的验证码是{1}，请于{2}分钟内正确输入。其中{1}和{2}为短信模板参数。
    
    4.3.测试成功后，即可申请短信模板并 正式使用 。
"""
"""
前端
    当用户输入 手机号， 图片验证码之后，前端发送一个 AXIOS 请求
	sms_codes/13672680885/?image_code=9MPY&image_code_id=acda37bd-7c4e-41c0-992c-f610f5db6a92
后端：
    请求： 
        请求：     接收请求，获取请求参数（路由有手机号， 用户的图片验证码和UUID在查询字符串中）
        业务逻辑：   验证参数，验证图片验证码， 生成短信验证码，保存验证码，发送短信验证码
        响应：     返回响应，
                {'code': 0, 'errmsg': 'ok'}
        路由：     GET     sms_codes/13672680885/?image_code=9MPY&image_code_id=acda37bd-7c4e-41c0-992c-f610f5db6a92
        步骤：     
            1.  获取参数
            2.  验证参数
            3.  验证图片验证码
            4.  生成短信验证码
            5.  保存短信验证码
            6.  发送短信验证码
            7.  返回响应
"""
from random import randint
import logging
logger = logging.getLogger('django')
class SmsCodeViwe(View):
    def get(self, request, mobile):
        # 1.  获取参数
        image_code = request.GET.get('image_code')
        uuid = request.GET.get('image_code_id')
        # 2.  验证参数
        if not all([image_code, uuid]):
            return JsonResponse({'code': 400, 'errmsg': '参数不全'})
        # 3.  验证图片验证码
        # 3.1 链接 redis
        redis_cli = get_redis_connection('code')
        # 3.2 获取 redis 数据
        redis_image_code = redis_cli.get('img_%s' % uuid)
        if redis_image_code is None:
            return JsonResponse({'code': 400, 'errmsg': '图片验证码失效'})
        # 删除图形验证码，防止恶意测试图形验证码
        try:
            redis_cli.delete('img_%s' % uuid)
        except Exception as e:
            logger.error(e)

        # 3.3 对比
        if redis_image_code.decode().lower() != image_code.lower():
            return JsonResponse({'code': 400, 'errmsg': '图片验证码错误'})
        # 提取发送短信的标记，看看有没有
        sned_flag = redis_cli.get('send_flag_%s' % mobile)
        if sned_flag is not None:
            return JsonResponse({'code': 400, 'errmsg': '请勿重复发送短信'})
        # 4.  生成短信验证码
        sms_code = '%06d' % randint(0, 999999)
        # 5.  保存短信验证码
        redis_cli.setex('sms_%s' % mobile, 300, sms_code)
        # 添加一个发送标记，防止频繁发送手机验证码
        redis_cli.setex('send_flag_%s' % mobile, 120, 1)
        # 6.  发送短信验证码
        from libs.yuntongxun.sms import CCP
        CCP().send_template_sms(mobile, [sms_code, 5], 1)
        # 7.  返回响应
        return JsonResponse({'code': 0, 'errmsg': 'ok'})