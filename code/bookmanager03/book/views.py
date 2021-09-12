from django.http import HttpResponse
from django.shortcuts import render
from book.models import BookInfo
# Create your views here.
def create_book(request):
    book=BookInfo.objects.create(
        name='abc',
        pub_date='2000-01-01',
        readcount=10
    )

    return HttpResponse('craete')

def shop(request, city_id, shop_id):
    query_params = request.GET
    print(query_params)
    # < QueryDict: {'order': ['readcount']} >
    # order = query_params.get('order')
    # order = query_params['order']
    # print(order)
    # <QueryDict: {'order': ['readcount', 'commentcount'], 'page': ['1']}>
    order = query_params.getlist('order')
    print(order)
    return HttpResponse("光哥的的小世界")

"""
查询字符串 
"""

def register(request):

    data = request.POST
    print(data)
    # <QueryDict: {'username': ['meiduo'], 'password': ['123456']}>
    return HttpResponse("okk")

def json(request):
    body = request.body
    print(body)
    # b'{\n    "name": "meiduo",\n    "age": 10\n}'
    body_str = body.decode()
    print(body_str)
    # {
    #     "name": "meiduo",
    #     "age": 10
    # }
    print(type(body_str))

    import json
    body_dict = json.loads(body_str)
    print(body_dict)

    ############# META  ######
    print(request.META['SERVER_PORT'])

    return HttpResponse("json")

def method(request):
    print(request.method)
    return HttpResponse('method')