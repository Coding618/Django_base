from django.http import HttpResponse
from django.shortcuts import render, redirect
from book.models import BookInfo
# Create your views here.
def create_book(request):
    book=BookInfo.objects.create(
        name='abc',
        pub_date='2000-01-01',
        readcount=10
    )

    return HttpResponse('craete')

def shop(request, city_id, mobile):
    print(city_id, mobile)
    query_params = request.GET
    print(query_params)
    # < QueryDict: {'order': ['readcount']} >###
    # order = query_params.get('order')
    # order = query_params['order']
    # print(order)
    # <QueryDict: {'order': ['readcount', 'commentcount'], 'page': ['1']}>
    # order = query_params.getlist('order')
    # print(order)
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
from django.http import JsonResponse
def response(request):
    # response = HttpResponse('res', status=598)
    # response['name'] = 'Sherlock'
    #
    # return response
    info={
        'name':'Sherlock',
        'address':'school'
    }
    girls = [
        {
            'name': 'excel',
            'address': 'guangzhou'
        },
        {
            'name': 'youzi',
            'address': 'nanjing'
        }
    ]
    """
    safe=True 表 将dict转换成 json数据
    """
    # response = JsonResponse(data=girls, safe=False)
    import json
    data = json.dumps(girls)
    # return HttpResponse(data)
    return redirect('https://www.baidu.com')

def set_cookie(request):

    username = request.GET.get('username')
    password = request.GET.get('password')
    response = HttpResponse('set_coookie')

    response.set_cookie('username', username, max_age=60*60)
    response.set_cookie('password', password)
    # response.delete_cookie('name')
    return response
def get_cookie(request):
    print(request.COOKIES)
    return HttpResponse('get_cookie')

def set_session(request):
    username = request.GET.get('username')
    user_id = 1
    request.session['user_id'] = 1
    request.session['username'] = username

    # request.session.clear()
    # request.session.flush()
    request.session.set_expiry(3600)
    return HttpResponse('set_session')

def get_session(request):
    # 获取字典的时候，用get
    user_id = request.session.get('user_id')
    username = request.session.get('username')

    # '%s'%username
    content = '{}, {}'.format(user_id, username)
    return HttpResponse(content)


####################
def login(request):
    if request.method == 'GET':
        return HttpResponse('GET 请求')
    else:
        return HttpResponse('POST 逻辑')



from  django.views import View

class LoginView(View):
    def get(self, request):
        return HttpResponse('get get geting')

    def post(self, request):
        return HttpResponse('post post posting')


class Person(object):
     def play(self):
         pass

     @classmethod
     def say(cls):
         pass
     @staticmethod
     def eat():
         pass

# Person.say()

from django.contrib.auth.mixins import LoginRequiredMixin

class OrderView(LoginRequiredMixin, View):
    def get(self, request):
        return HttpResponse("GET 我的订单里面必须登录")
    def post(self, request):
        return HttpResponse("POST 我的订单页面，这个页面必须登录")