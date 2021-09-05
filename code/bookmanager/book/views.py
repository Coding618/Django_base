from django.shortcuts import render

# Create your views here.
from django.http import HttpRequest
from django.http import HttpResponse

def index(request):

    # render(request, template_name, context=None) 渲染模板
    # request           请求
    # tempfile_name     模板名字
    # context=None
    context={
        'name':'马上爽十一，点他'
    }
    return render(request,"book/index.html",context=context)