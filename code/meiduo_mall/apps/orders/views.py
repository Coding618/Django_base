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
