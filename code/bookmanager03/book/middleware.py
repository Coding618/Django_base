from django.utils.deprecation import MiddlewareMixin

class TestMiddleWare(MiddlewareMixin):

    def process_request(self, request):
        print("每次请求前需要调用该方法")

        username = request.COOKIES.get('username')
        if username is None:
            print('没有用户信息')
        else:
            print("有用户信息")

    def process_response(self, request, response):
        print("每次响应，都会调用执行")

        return response