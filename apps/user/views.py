from django.shortcuts import render
import  re
from apps.user.models import *

# Create your views here.
def register(request):
    '''显示注册页面'''
    return render(request, 'register.html')

def register_handle(request):
    '''进行注册处理'''
    # 接受数据
    username = request.POST.get('user_name')
    password = request.POST.get('pwd')
    email = request.POST.get('email')
    allow = request.POST.get('allow')
    # 进行数据的校验
    if not all([username,password,email]):
        # 如果书库不完整的话
        return render(request, 'register.html', {'errmsg': '表单不完整'})

    if allow != 'on':
        return render(request, 'register.html', {'errmsg': '没有同意协议'})
    # 校验邮箱
    if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$',email):
        return render(request, 'register.html', {'errmsg': '邮箱格式错误'})
    # 进行业务处理:进行用户注册
    user = UserInfo.objects.create_()

    # 返回一个应答



