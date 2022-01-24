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
        response = JsonResponse({'code': 0, 'errmsg': 'ok'})
        # 为了首页显示用户信息
        response.set_cookie('username', username)
        return response

"""
前端：
    当用户点击退出按钮的时候，前端发送一个 axios delete请求
后端：
    请求
    业务逻辑        退出
    响应          返回JSON数据
"""
from django.contrib.auth import logout
class LogoutView(View):
    def delete(self, request):

        logout(request)

        response = JsonResponse({'code': 0, 'errmsg': "退出登录成功"})

        response.delete_cookie('username')
        return response

"""
用户中心，也必须是登录用户
LoginRequiredMixin 未登录的用户， 会返回 重定向，重定向并不是JSON数据

我们需要返回JSON数据
"""

from utils.views import LoginRequiredJSONMixin

class CenterView(LoginRequiredJSONMixin,View):

    def get(self, request):
        # request.user 就是 已经在登录的用户信息
        # request.user 是来源于 中间件
        # 系统会进行判断，如果我们确实是登录用户，则可以获取到，登录用户对应的 模型实例;
        # 如果我们确实不是登录用户，到 request.user = AnonymousUser() 匿名用户
        info_data = {
            'username': request.user.username,
            'email': request.user.email,
            'mobile': request.user.mobile,
            'email_active': request.user.email_active
        }
        return JsonResponse({'code': 0, 'errmsg': 'OK!', 'info_data': info_data})

"""
需求：     1. 保存邮箱 2. 发送一封激活邮件     3. 用户激活邮件

前端：     
        当用户输入邮箱之后，点击保存，然后发送一个 axios 请求
后端：
    请求：     接收请求，获取数据
    业务逻辑：   保存邮箱地址，发送一封激活邮件
    响应：        JSON code=0
    路由：     PUT
    步骤：
        1. 接收请求;
        2. 获取数据;
        3. 保存邮箱地址;
        4. 发送一封验证邮件;
        5. 返回响应
需求（需要实现的功能） --》 思路（请求，业务逻辑，响应） --》步骤  --》代码实现
"""
class EmailView(LoginRequiredJSONMixin, View):
    def put(self, request):
        # 1. 接收请求;
        # put, post ---- body
        data = json.loads(request.body)
        # 2. 获取数据;
        email = data.get('email')
        # 验证数据，正则

        # 3. 保存邮箱地址;
        # user / request.user 就是 登录用户的 实例对象
        # user ---》 User
        user = request.user
        user.email = email
        user.save()
        # 4. 发送一封验证邮件;
        from django.core.mail import send_mail
        # subject, message, from_email, recipient_list,
        # subject,          主题
        subject = '美多商城激活邮件'
        # message,          邮件内容
        message = ""
        # from_email,       发件人
        from_email = '美多商城<qi_rui_hua@163.com>'
        # recipient_list,    收件人列表
        recipient_list = ['windowsphonewang@163.com', 'sherlock0618@qq.com']
        # 4.1 对a标签的链接数据进行加密处理
        # user_id = 1
        from apps.users.utils import generic_emial_verify_token
        token = generic_emial_verify_token(request.user.id)

        verify_url = "http://www.meiduo.site:8080/success_verify_email.html?token=%s" % token
        html_message = '<p>尊敬的用户您好！</p>' \
                       '<p>感谢您使用美多商城。</p>' \
                       '<p>您的邮箱为：%s 。请点击此链接激活您的邮箱：</p>' \
                       '<p><a href="%s">%s<a></p>' % (email, verify_url, verify_url)

        # html_message = "test email，请点击链接，进行验证<a href='http:www.baidu.com/?token=%s'>激活</a> " % token

        # 邮件的内容如果是 html 这个时候，使用 html_message
        # html_message = "点击按钮"
        # send_mail(subject=subject,
        #           message=message,
        #           from_email=from_email,
        #           recipient_list=recipient_list,
        #           html_message=html_message)
        from celery_tasks.email.tasks import celery_send_email
        celery_send_email.delay(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            html_message=html_message
        )

        # 5. 返回响应
        return JsonResponse({'code': 0, 'errmsg': 'ok, 邮件发送成功'})

"""
1. 夯实 django的基础
2. 需求分析
3. 学习新知识
4. 掌握分析问题，解决问题的能力（debug）
"""
"""
设置邮件服务器的步骤
1. 设置邮件服务器
    我们设置    163 邮箱服务器
    相当于 我们开启了 让163 帮助我们发送邮件; 同时设置了一些信息（特别是授权码）
2. 设置邮件发送的配置信息

3. 调用 send_mail 方法
"""
"""
需求：获取token信息，接收验证，更新状态，返回响应
前端：
    用户点击激活链接后，那个激活链接携带了 token
后端：
    请求：         接收请求，获取参数，验证参数，
    业务逻辑：       user_id, 根据用户id查询数据，修改数据
    响应：         返回响应 JSON
    
    路由：         PUT         emails/verification/    说明： token 并没有在 body 里
    步骤：
        1. 接收参数
        2. 获取参数
        3. 验证参数
        4. 获取 user_id
        5. 根据用户 id 查询数据
        6. 修改数据
        7. 返回响应 JSON
"""

class EmailVerifyView(View):

    def put(self, request):
        # 1. 接收参数
        params = request.GET
        # 2. 获取参数
        token = params.get('token')
        # 3. 验证参数
        if not token:
            return JsonResponse({'code': 400, 'errmsg': '参数缺失'})
        # 4. 获取 user_id
        from apps.users.utils import check_verify_token
        user_id = check_verify_token(token)
        if user_id is None:
            return JsonResponse({'code': 400, 'errmsg': '参数错误， 用户不存在'})
        # 5. 根据用户 id 查询数据
        user = User.objects.get(id=user_id)
        # 6. 修改数据
        user.email_active = True
        user.save()
        # 7. 返回响应 JSON
        return JsonResponse({'code': 0, 'errmsg': '邮件激活成功'})


"""
需求：
    新增地址
前端：
    当用户编写完成地址信息后，前端发送应该发送一个axios请求，会携带  相关的信息  （POST -- body）
后端：
    请求：         接收请求，获取参数，验证参数;
    业务逻辑：       数据入库
    响应：         返回响应

    路由：     POST    /addresses/create/
    步骤：
        1.接收请求
        2.获取参数，验证参数
        3.数据入库
        4.返回响应
"""
from apps.users.models import Address


class AddressCreateView(LoginRequiredJSONMixin, View):
    def post(self, request):
        # 1.接收请求
        data = json.loads(request.body.decode())
        # 2.获取参数，验证参数
        receiver = data.get('receiver')
        province_id = data.get('province_id')
        city_id = data.get('city_id')
        district_id = data.get('district_id')
        place = data.get('place')
        mobile = data.get('mobile')
        tel = data.get('tel')
        email = data.get('email')

        user = request.user
        # 验证参数(省略)
        # 2.1 验证必填参数
        # 2.2 省市区id， 是否正确
        # 2.3 详细地址的长度
        # 2.4 手机号
        # 2.5 固定电话
        # 2.6 邮箱
        # 3.数据入库
        address = Address.objects.create(
            user=user,
            title=receiver,
            receiver=receiver,
            province_id=province_id,
            city_id=city_id,
            district_id=district_id,
            place=place,
            mobile=mobile,
            tel=tel,
            email=email
        )
        address_dict = {
            "id": address.id,
            "title": address.title,
            "receiver": address.receiver,
            "province": address.province.name,
            "city": address.city.name,
            "district": address.district.name,
            "place": address.place,
            "mobile": address.mobile,
            "tel": address.tel,
            "email": address.email
        }
        # 4.返回响应
        return JsonResponse({'code': 0, 'errmsg': 'ok~', 'address': address_dict})

class AddressView(LoginRequiredJSONMixin, View):
    def get(self, request):
        # 1.查询指定数据
        user = request.user
        # addresses = user.addresses
        addressses = Address.objects.filter(user=user, is_deleted=False)
        # 2.将对象数据，转换为字典数据
        address_list = []
        for item in addressses:
            address_list.append({
                'id': item.id,
                'title': item.title,
                'receiver': item.receiver,
                'province': item.province.name,
                'city': item.city.name,
                'district': item.district.name,
                'place': item.place,
                'mobile': item.mobile,
                'tel': item.tel,
                'email': item.email
            })
        # 3.返回响应
        return JsonResponse({'code': 0, 'errmsg': 'ok~ 查询地址成功～', 'addresses': address_list})

##############################################
"""
一、根据页面效果，分析需求
    1. 最近浏览记录   只有登录用户才可以访问。我们只记录登录用户的浏览记录
    2. 浏览记录应该有顺序
    3. 没有分页
二、功能：
    1. 在用户访问商品详情的时候，添加浏览记录
    2. 在个人中心，展示浏览记录
三、分析：
    问题1：    保存哪些数据？     用户id、商品id、顺序（时间）
    问题2：    保存在哪里？      一般要保存在数据库中  （缺点：慢; 频繁操作数据库）
                            最好是redis中
                            服务器内存较大，可以选择： MySQL + Redis
user_id, sku_id, 顺序
key: value          key(user_id)
redis:
    string:     X
    list:       V
    hash:       X(无顺序)
    set:        X(无顺序)
    zset:       V(无重复)
                权重：值
"""
"""
添加浏览记录：
    前端：
            当登录用户，访问一个具体的SKU页面的时候，发送一个axios请求;  请求携带    sku_id
    后端：
        请求：             接收请求，获取请求参数，验证参数
        业务逻辑：          连接Redis，先去重，再保存到Redis中，只保存5条记录;
        响应：             返回JSON
        路由：            POST     browse_histories
        步骤：
            1. 接收请求
            2. 获取参数
            3. 验证参数
            4. 连接 Redis，   list
            5. 去重
            6. 保存到Redis中;
            7. 只保存5条记录
            8. 返回JSON
展示浏览记录：
    前端：
            用户在访问浏览记录的时候，发送axios请求。请求会携带session信息
    后端：
        请求：              
        业务逻辑：       连接redis， 获取redis数据([1, 2, 3]). 根据商品id，进行数据查询，将对象转换为字典          
        响应：           JSON
        路由：           GET
        步骤： 
            1. 连接redis
            2. 获取redis数据 ([1, 2, 3])
            3. 根据商品id进行数据查询
            4. 将对象转换为字典
            5. 返回JSON
            
"""
from apps.goods.models import SKU
from django_redis import get_redis_connection
class UserHistoryView(LoginRequiredJSONMixin, View):
    def post(self, request):
        user = request.user
        # 1. 接收请求
        data = json.loads(request.body.decode())
        # 2. 获取参数
        sku_id = data.get('sku_id')
        # 3. 验证参数
        try:
            sku = SKU.objects.get(id=sku_id)
        except SKU.DoesNotExist:
            return JsonResponse({'code': 400, 'errmsg': '没有此商品'})
            # 4. 连接 Redis，   list
        redis_cli = get_redis_connection('history')
            # 5. 去重(先删除 这个商品id的数据，再添加就可以)
        redis_cli.lrem('history_%s' % user.id, 0, sku_id)
            # 6. 保存到Redis中;
        redis_cli.lpush('history_%s' % user.id, sku_id)
            # 7. 只保存5条记录
        redis_cli.ltrim('history_%s' % user.id, 0, 4)
            # 8. 返回JSON
        return JsonResponse({'code': 0, 'errmsg': 'OK!!!'})

    def get(self, request):
        # 1. 连接redis
        redis_cli = get_redis_connection('history')
        # 2. 获取redis数据 ([1, 2, 3])
        ids = redis_cli.lrange('history_%s' % request.user.id, 0, 4)    # 0, -1
        # 3. 根据商品id进行数据查询
        history_list = []
        for sku_id in ids:
            sku = SKU.objects.get(id=sku_id)
            # 4. 将对象转换为字典
            history_list.append({
                "id": sku.id,
                "name": sku.name,
                "default_image_url": sku.default_image.url,
                "price": sku.price
            })
        # 5. 返回JSON
        return JsonResponse({'code': 0, 'errmsg': 'ok~', 'skus': history_list})