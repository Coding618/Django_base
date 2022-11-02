"""
需求：
    在登录的时候，将cookie上的数据，合并到redis中;
前端：
后端：
    请求：         登录的时候，获取cookie数据
    业务逻辑：       合并到redis中
    响应：

1. 读取cookie数据
2. 初始化一个字典，用于保存 sku_id:count
    初始化一个列表，用于保存选中的商品id
    初始化一个列表，用于保存未选中 的商品id
3. 遍历 cookie 数据
4. 将字典数据，列表数据分别添加到redis中
2. 删除cookie数据

################################
redis           hash
                        1:10
                        3:10
                set
                        1
cookie
        {
            1: {count:666, selected:True},      # sku_id: count
            2: {count:999, selected:True},
        }

hash
1:666
2:99
1. 当 cookie 数据和redis数据，不一致，有相同的商品id的时候，数量怎么办？？？（可能有多种情况）我们暂时以  cookie 为主
2. 当 cookie 数据有，但是redis数据没有的，全部以 cookie为主。
3, 当 redis中有数据，而 cookie 没有。则，不修改。
"""
import base64
import pickle

from django_redis import get_redis_connection


def merge_carts_cookie_to_redis(request, response):
    # 1. 读取cookie数据
    carts_str = request.COOKIES.get('carts')
    # if carts_str is not None:
    #     carts = pickle.loads(base64.b64decode(carts_str.encode()))
    if not carts_str:
        return response
    carts = pickle.loads(base64.b64decode(carts_str.encode()))
    # 2. 初始化一个字典，用于保存 sku_id:count
    new_cookie_dict = {}
    #     初始化一个列表，用于保存选中的商品id
    select_ids = []
    #     初始化一个列表，用于保存未选中 的商品id
    unselect_ids = []
    # 3. 遍历 cookie 数据
    for sku_id, count_select_dict in carts.items():
        new_cookie_dict[sku_id] = count_select_dict['count']
        if count_select_dict['selected']:
            select_ids.append(sku_id)
        else:
            unselect_ids.append(sku_id)
    # 4. 将字典数据，列表数据分别添加到redis中
    # {sku_id: count, sku_id: count, ...}
    # selected_ids [1, 2, 3]
    # unselected_ids [4, 5, 6]
    redis_cli = get_redis_connection('carts')
    pipeline = redis_cli.pipeline()
    pipeline.hmset('carts_%s' % request.user.id, new_cookie_dict)
    if len(select_ids):
        pipeline.sadd('selected_%s' % request.user.id, *select_ids)
    if len(unselect_ids):
        pipeline.sadd('unselected_%s' % request.user.id, *unselect_ids)
    pipeline.execute()
    # 5. 删除cookie数据
    response.delete_cookie('carts')
    return response

