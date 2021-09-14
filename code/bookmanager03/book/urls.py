from django.urls import path
from book.views import create_book, shop, register, json, method, response
from django.urls import converters
from django.urls.converters import register_converter

class MoblieConverter:
    regex = '1[3-9]\d{9}'

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value
# converter 转换器类
# type_name 转换器名字
register_converter(MoblieConverter, 'phone')
urlpatterns = [
    path('create/', create_book),
    path('<int:city_id>/<phone:mobil    e>/', shop),
    path('register', register),
    path('json/', json),
    path('method/', method),
    path('res/', response)
]