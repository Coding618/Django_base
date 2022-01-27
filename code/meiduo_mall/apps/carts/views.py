import json

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from django_redis import get_redis_connection

"""
1. 京东的网站，登录的用户可以实现购物车，未登录用户可以实现购物车       V 
   淘宝的网站，必须是登录用户才可以实现购物车
2. 登录用户数据保存在哪里？         服务器里    mysql/redis
                                            redis           学习，购物车频繁增删改查
                                            mysql + redis
   未登录用户数据保存在哪里？        客户端     
                                            cookie
3. 保存哪些数据？？？
            redis:  
                    user_id, sku_id(商品id), count(数量)， selected(选中状态)
            
            cookis: 
                    sku_id, count, selected

4. 数据的组织：
    redis:
            user_id, sku_id(商品id), count(数量), selected(选中状态)
            hash
            user_id:
                    sku_id:count,
                    xxx_sku_id: selected
            
            1:
                1:10
                xxx_1: True
                2:20
                xxx_2: True
                3:30
                xxx_3: True
            总共13个空间
            进一步优化？！！！
            优化：因为redis的数据是保存在内存中，我们应该尽量少的占用redis的空间
            user_id:
                    sku_id: count
            selected:
            
            user_1:         id : 数量
                            1  : 10
                            2  : 20
                            3  : 30
            记录选中的商品：
            1,3
            
            user_1:
                    1:10
                    2:20
                    3:30
            selected_1: {1, 3}
            总共10个空间
            
            user_1:             (通过正负来记录是否被选中)
                    1 : 10
                    2 : -20
                    3 : 30
            7个空间
    cookie:
        {
            sku_id: {count: xxx, selected: xxxx},
            sku_id: {count: xxx, selected: xxxx},
            sku_id: {count: xxx, selected: xxxx},
            sku_id: {count: xxx, selected: xxxx},
        }
5. 
    cookie字典转换为字符串保存起来，数据没有加密
    
    base64
    
    1G = 1024MB
    1MB = 1024 KB
    1KB = 1024 B
    1B  = 8 byte
    
    ASCII
    base64：由8位 --> 6位
    aaa ---> XYZN
    
    base64模块使用：
        base64.b64encode()将bytes类型数据进行base64编码，返回编码后的bytes类型数据;
        base64.b64decode()将base64编码后的bytes类型数据进行解码，返回解码后的bytes类型数据。
    
    字典 -------》pickle ----- 二进制----------》Base64编码（6位）
    pickle 模块使用：
        pickle.dumps()将Python数据序列化为bytes类型的数据;
        pickle.loads()将bytes类型数据烦序列化为Python数据
######################### 编码数据 ###########################        
# 字典
carts = {
    '1': {'count':10, 'selected': True},
    '2': {'count':20, 'selected': False},
}

# 字典 转换为 bytes类型
import pickle
b = pickle.dumps(carts)

# bytes类型的数据 进行base64编码
import base64
encode = base64.b64encode(b)

###################### 解码数据 ########################
# base64编码的数据 进行解码
decode_bytes = base64.b64decode(encode)

# 对解码后的数据 转换为 字典
pickle.loads(decode_bytes)

6.
请求：
业务逻辑：
响应

增（注册）
    1. 接收数据
    2. 验证数据
    3. 数据入库
    4. 返回响应
删
    1.查询到指定记录
    2.删除数据（物理删除，逻辑删除）
    3.返回响应
改（个人的邮箱）
    1.查询指定的记录
    2.接收数据
    3.验证数据
    4.数据更新
    5.返回响应
查（个人中心的数据展示，省市区）
    1.查询指定数据
    2.将对象数据转换为字典数据
    3.返回响应
"""
from apps.goods.models import SKU
import pickle
import base64
class CartsView(View):
    """
    前端：
        用户点击添加购物车之后，前端将 商品id 发送给后端
    后端：
        请求：             接收参数，验证参数
        业务逻辑：           根据商品id，查询数据库，检查商品id， 数量是否有效
                            数据入库
                                登录用户入 redis
                                    链接redis
                                    获取用户id
                                    hash
                                    set
                                未登录用户 入cookie
                                    先有cookie字典
                                    字典转为bytes
                                    bytes类型数据 转为 base64编码
                                    设置cookie
                                    返回响应
        响应：             返回 JSON
        路由：         POST    /carts/
        步骤：
                    1. 接收数据
                    2. 验证数据
                    3. 判断用户的登录状态
                    4. 登录用户保存redis
                        4.1 链接redis
                        4.2 操作hash
                        4.3 操作set
                        4.4 返回响应
                    5. 未登录用户保存cookie
                        5.1 先有cookie字典
                        5.2 字典转为bytes
                        5.3 bytes类型数据 转为 base64编码
                        5.4 设置cookie
                        5.5 返回响应
    """
    def post(self, request):
        # 1. 接收数据
        data = json.loads(request.body.decode())
        sku_id = data.get("sku_id")
        count = data.get("count")
        # 2. 验证数据
        try:
            sku = SKU.objects.get(id=sku_id)
        except SKU.DoesNotExist:
            return JsonResponse({'code': 400, 'errmsg': '查无此商品'})
        # 类型强制转换
        try:
            count = int(count)
        except Exception:
            count = 1
        # 3. 判断用户的登录状态
        user = request.user
        if user.is_authenticated:
            # 4. 登录用户保存redis
            #     4.1 链接redis
            redis_cli = get_redis_connection('carts')
            #     4.2 操作hash
            redis_cli.hset('carts_%s' % user.id, sku_id, count)
            #     4.3 操作set
            redis_cli.sadd('selected_%s' % user.id, sku_id)
            #     4.4 返回响应
            return JsonResponse({'code': 0, 'errmsg': 'OK!添加购物车成功'})
        else:
            # 5. 未登录用户保存cookie
            # 5.0 先读取cookie数据
            cookie_carts = request.COOKIES.get("carts")
            if cookie_carts:
                carts = pickle.loads(base64.b64decode(cookie_carts))
            else:
                #     5.1 先有cookie字典
                carts = {}
            # 判断商品id 是否在购物车cookie中
            if sku_id in carts:
                # 该商品存在 购物车的cookie中
                origin_count = carts[sku_id]['count']
                count += origin_count

            carts[sku_id] = {
                'count': count,
                'selected': True
            }

            #     5.2 字典转为bytes

            carts_bytes = pickle.dumps(carts)
            #     5.3 bytes类型数据 转为 base64编码

            base64encode = base64.b64encode(carts_bytes)
            #     5.4 设置cookie
            response = JsonResponse({'code': 0, 'errmsg': 'OK! 购物车加入cookie成功'})
            response.set_cookie('carts', base64encode.decode(), max_age=3600*24*12)
            #     5.5 返回响应
            return response
