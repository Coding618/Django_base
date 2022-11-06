import json

from django.shortcuts import render

# Create your views here.


"""
提交订单页面的展示
前端：
        发送一个axios 请求来获取，地址信息和购物车中选中的信息。
后端：
    请求:     必须是登陆用户才能访问;
    业务逻辑：   地址信息，购物车中选中商品的信息
    响应：     JSON
    路由：
        GET         orders/settlement/
    步骤：
        1. 获取用户信息
        2. 地址信息
            2.1 查询用户的地址信息（Address, Address, ...）
            2.2 将对象数据转换为字典数据
        3. 购物车中选中商品的信息
            3.1 链接 redis
            3.2 hash        {sku_id: count, sku_id:count}
            3.3 set         [1, 2, 3]
            3.4 (选做，优化)重新组织一个 选中的信息;
            3.5 根据商品的id，查询商品的具体信息（SKU, SKU, SKU, ...）
            3.6 需要将对象数据转换为字典数据。
"""
from django.views import View
from utils.views import LoginRequiredJSONMixin
from apps.users.models import Address
from django_redis import get_redis_connection
from django.http import JsonResponse
from apps.goods.models import SKU
from decimal import Decimal
class OrderSettlementView(LoginRequiredJSONMixin, View):
    def get(self, request):
        # 1. 获取用户信息
        user = request.user
        # 2. 地址信息
        #     2.1 查询用户的地址信息（Address, Address, ...）
        addresses = Address.objects.filter(user=user, is_deleted=False)
        #     2.2 将对象数据转换为列表数据
        address_list = []
        for address in addresses:
            address_list.append({
                'id': address.id,
                'province': address.province.name,
                'city': address.city.name,
                'district': address.district.name,
                'place': address.place,
                'receiver': address.receiver,
                'mobile': address.mobile
            })
        # 3. 购物车中选中商品的信息
        #     3.1 链接 redis
        redis_cli = get_redis_connection('carts')
        pipeline = redis_cli.pipeline()
        #     3.2 hash        {sku_id: count, sku_id:count}
        pipeline.hgetall('carts_%s' % user.id)
        #     3.3 set         [1, 2, 3]
        pipeline.smembers('selected_%s' % user.id)
        result = pipeline.execute()
        sku_id_counts = result[0]
        selected_id = result[1]
        #     3.4 (选做，优化)重新组织一个 选中的信息;
        selected_cart = {}
        for sku_id in selected_id:
            selected_cart[int(sku_id)] = int(sku_id_counts[sku_id])
        #     3.5 根据商品的id，查询商品的具体信息（SKU, SKU, SKU, ...）
        skus = SKU.objects.filter(id__in=selected_cart.keys())
        #     3.6 需要将对象数据转换为字典数据。
        sku_list = []
        for sku in skus:
            sku_list.append({
                'id': sku.id,
                'name': sku.name,
                'default_image_url': sku.default_image.url,
                'price': sku.price,
                'count': selected_cart[sku.id]
            })

        # 邮费
        freight = Decimal('10.00')
        context = {
            'skus': sku_list,
            'addresses': address_list,
            'freight': freight
        }
        return JsonResponse({
            'code': 200,
            'errmsg': 'ok~',
            'context': context})

"""
需求：     点击提交订单，生成订单
前端：     发送axiso请求，POST  携带数据    地址id， 支付方式，携带账户的session信息（cookie）
            不传 总金额，商品id 和 数量    （从后端获取） 
后端：     
    请求：     接收请求，验证数据
    业务逻辑：   数据入库
    响应：     返回响应
    
    路由：     POST    
    步骤：     
        一、接收请求     user, address_id, pay_method
        二、验证数据
            order_id    主键（自己生成）
            支付状态由支付方式决定
            总数量，总金额，运费
        三、数据入库     生成订单（订单基本信息表和订单商品信息表）
            1. 先保存订单基本信息
            2. 再保存订单商品信息
                2.1 连接redis
                2.2 获取 hash
                2.3 获取 set
                2.4 遍历选中商品的id。
                    最好重写组织一个数据，这个数据是选中的商品信息
                    {sku_id:count, sku_id:count}
                2.5 遍历 根据选中商品的id 进行查询
                2.6 判断库存是否充足。
                2.7 如果不充足，下单失败。
                2.8 如果充足，到库减少，销量增加。
                2.9 累加总数量和总金额。
                2.10 保存订单商品信息
            3. 更新订单的总金额和总数量
            4. 将redis中选中的商品信息移除出去。
        四、返回响应。         
                    
"""
from django.utils import timezone
from apps.orders.models import OrderInfo, OrderGoods
class OrderCommitView(LoginRequiredJSONMixin, View):
    def post(self, request):
        # 一、接收请求     user, address_id, pay_method
        user = request.user
        data = json.loads(request.body.deconde())
        address_id = data.get('address_id')
        pay_method = data.get('pay_method')
        if not all([address_id, pay_method]):
            return JsonResponse({'code': 400, 'errmsg': '缺少必要参数'})
        try:
            address = Address.objects.filter(id=address_id)
        except Exception:
            return JsonResponse({'code': 400, 'errmsg': '参数address_id错误'})
        # 二、验证数据
        #     order_id    主键（自己生成）
        order_id = timezone.localtime().strftime('%Y%m%d%H%M%S') + ('%09d' % user.id)
        # 先验证pay_method格式的合法性
        if pay_method not in [OrderInfo.PAY_METHODS_CHOICES['CASH'], OrderInfo.PAY_METHODS_CHOICES['ALIPAY']]:
            return JsonResponse({'code': 400, 'errmsg': '参数pay_method格式错误'})
        #     支付状态由支付方式决定
        if pay_method == OrderInfo.PAY_METHODS_ENUM['CASH']:
            pay_status = OrderInfo.ORDER_STATUS_ENUM['UNSEND']
        elif pay_method == OrderInfo.PAY_METHODS_ENUM['ALIPAY']:
            pay_menthod = OrderInfo.ORDER_STATUS_ENUM['UNPAID']
        #     总数量=0,
        total_count = 0
        # 总金额 = 0，
        total_amount = 0
        #     运费
        freight = Decimal('10.0')
        # 三、数据入库     生成订单（订单基本信息表和订单商品信息表）
        #     1. 先保存订单基本信息
        OrderInfo.objects.create(
            order_id=order_id,
            user=user,
            address=address,
            total_count=total_count,
            total_amount=total_amount,
            freight=freight,
            pay_method=pay_method,
            status=pay_status
        )
        #     2. 再保存订单商品信息
        #         2.1 连接redis
        #         2.2 获取 hash
        #         2.3 获取 set
        #         2.4 遍历选中商品的id。
        #             最好重写组织一个数据，这个数据是选中的商品信息
        #             {sku_id:count, sku_id:count}
        #         2.5 遍历 根据选中商品的id 进行查询
        #         2.6 判断库存是否充足。
        #         2.7 如果不充足，下单失败。
        #         2.8 如果充足，到库减少，销量增加。
        #         2.9 累加总数量和总金额。
        #         2.10 保存订单商品信息
        #     3. 更新订单的总金额和总数量
        #     4. 将redis中选中的商品信息移除出去。
        # 四、返回响应。,,
        pass
