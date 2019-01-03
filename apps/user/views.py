
from django.shortcuts import render,redirect # redirect 重定向
from django.core.urlresolvers import reverse
from apps.user.models import User,Address
from apps.goods.models import GoodsSKU
from django.views.generic import View
from django.conf import settings
from django.http import HttpResponse
from django.core.mail import send_mail
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired #这是一个异常
from django.contrib.auth import authenticate,login,logout# 这是django对用户登录验证和保持用户登录的模块
from utils.mixin import LoginRequiredMixin
from celery_tasks.tasks import send_register_active_email
from django_redis import get_redis_connection
import  re

# Create your views here.
def register(request):
    if request.method == 'GET':

        '''显示注册页面'''
        return render(request, 'register.html')
    else:
        '''进行注册处理'''
        # 接受数据
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')
        # 进行数据的校验
        if not all([username, password, email]):
            # 如果书库不完整的话
            return render(request, 'register.html', {'errmsg': '表单不完整'})

        if allow != 'on':
            return render(request, 'register.html', {'errmsg': '没有同意协议'})
        # 校验邮箱
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg': '邮箱格式错误'})
        # 校验用户名是否重复
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # 用户名不存在
            user = None

        if user:
            # 用户名已经存在
            return render(request, 'register.html', {'errmsg': '用户名已存在'})

        # 进行业务处理:进行用户注册
        user = User.objects.create_user(username, email, password)
        user.is_active = 0
        user.save()
        # 返回一个应答 跳转到首页
        return redirect(reverse('goods:index'))

# 关于类视图的使用:
class RegisterView(View):
    '''注册'''
    def get(self,request):
        '''显示注册页面'''
        return render(request, 'register.html')

    def post(self,request):
        '''进行注册处理'''
        # 接受数据
        username = request.POST.get('user_name')
        password1 = request.POST.get('pwd')
        password2 = request.POST.get('cpwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')
        # 进行数据的校验
        if not all([username, password1, password2, email]):
            # 如果书库不完整的话
            return render(request, 'register.html', {'errmsg': '表单不完整'})
        # 进行密码两次是否一致的验证
        if password2 != password1:
            return render(request, 'register.html', {'errmsg': '两次密码不一致'})
        if allow != 'on':
            return render(request, 'register.html', {'errmsg': '没有同意协议'})
        # 校验邮箱
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg': '邮箱格式错误'})
        # 校验用户名是否重复
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # 用户名不存在
            user = None

        if user:
            # 用户名已经存在
            return render(request, 'register.html', {'errmsg': '用户名已存在'})

        # 进行业务处理:进行用户注册
        user = User.objects.create_user(username, email, password1)
        user.is_active = 0
        user.save()

        # 发送激活邮件,包含激活链接
        # 激活链接中需要包含用户的身份信息

        #加密用户的身份信息,
        serializer = Serializer(settings.SECRET_KEY,3600)
        info = {'confirm':user.id}
        token =serializer.dumps(info) # bytes
        # !!!!大坑 返回的加密数据多加了一个'b' http://127.0.0.1:8000/user/active/b'eyJh*****
        # 这里代表是字节流,可是我们想要的是一个字符串 我们需要一个解码
        token = token.decode('utf8') #默认就是utf8 括号里也可以不写


        # # 发邮件
        # subject = '天天生鲜用户激活'
        # message = ""
        # sender = settings.EMAIL_FROM
        # receiver = [email]
        # html_mesg = "<h1>%s,欢迎您注册天天生鲜</h1>请点击以下链接激活您的账户</br><a href='http://127.0.0.1:8000/user/active/%s'>http://127.0.0.1:8000/user/active/%s</a>"%(username,token,token)
        # send_status = send_mail(subject,message,sender,receiver,html_message=html_mesg)
        # print(send_status)
        # # 返回一个应答 跳转到首页


        # 如何使用异步celery处理延时任务的话 就调用这个函数
        send_register_active_email.delay(email,username,token)

        return redirect(reverse('goods:index'))


# 用户激活的视图
class ActiveView(View):
    '''用户激活'''
    def get(self,request,token):
        # 进行解密,获取要激活的用户信息
        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
            # 获取待激活用户的id
            info = serializer.loads(token)
            user_id = info['confirm']

            # 根据id获取用户信息
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()

            # 直接跳转到登录页面
            return redirect(reverse('user:login'))
        except SignatureExpired as e:
            # 激活链接已过期
            return HttpResponse('激活链接已过期')
# /user/login
class LoginView(View):
    '''登录'''
    def get(self,request):
        '''显示登录页面'''
        # 判断是否记住了用户名
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
            checked = 'checked'
        else:
            username = ''
            checked = ''
        return render(request,'login.html',{'username':username,'checked':checked})

    def post(self,request):
        '''登录校验'''
        # 接收数据
        username = request.POST.get('username')
        password = request.POST.get('pwd')

        # 校验数据
        if not all([username,password]):
            return render(request,'login.html',{'errmsg':'数据不完整'})
        # 业务处理:登录校验

        user = authenticate(username=username, password=password)
        if user is not None:
            # 用户名密码正确
            if user.is_active:
                # 用户已激活
                # 记录用户的登录状态
                login(request,user)

                # 获取登录后所要跳转到的地址
                next_url = request.GET.get('next',reverse('goods:index'))

                # 跳转到首页
                response = redirect(next_url)
                # 判断是否需要记住用户名
                remember = request.POST.get('remember')

                if remember == 'on':
                    # 记住用户名
                    response.set_cookie('username',username,max_age=7*24*3600)
                    print("ceshi")
                else:
                    response.delete_cookie('username')
                # 返回response
                return response

            else:
                # 用户未激活
                return render(request, 'login.html', {'errmsg': '账户未激活'})
        else:
            # 用户名或者密码错误
            print("cuowu")
            return  render(request,'login.html',{'errmsg':'用户名或sss者密码错误'})

        # 返回应答

# /user/logout
class LogoutView(View):
    '''退出登录'''
    def get(self,request):
        '''退出登录'''
        # 清除用户的session信息
        logout(request)

        # 跳转到首页
        return  redirect(reverse('goods:index'))

# /user/
class UserInfoView(LoginRequiredMixin,View):
    '''用户中心-信息页'''
    def get(self,request):
        '''显示'''
        # django框架会给request对象添加一个属性user
        # 如果用户已登录，user的类型User
        # 如果用户没登录，user的类型AnonymousUser


        # 获取用户的个人信息
        user = request.user

        # # 获取用户的默认收货地址
        # try:
        #     address = Address.objects.get(user=user, is_default=True)
        # except Address.DoesNotExist:
        #     address = None

        address = Address.object.get_default_address(user)

        # 获取用户的历史浏览记录
        # from redis import StrictRedis
        # conn = StrictRedis(host='172.16.179.142', db=10)
        # 上面这两句可以用下面这一句封装(利用了django-redis)
        con = get_redis_connection('default') # 这里的default就是settings里面的redis的default设置
        # 这个con就是 上面的StrictRedis的实例对象

        history_key = 'history_%d' % user.id
        # 获取用户最新浏览的5个商品的id
        sku_ids = con.lrange(history_key, 0, 4)  # [4, 2, 1, 3]

        # 从数据库中查询用户浏览商品的具体信息,直接使用范围查询
        skus = GoodsSKU.objects.filter(id__in=sku_ids)
        # skus_li = []
        # for sku_id in sku_ids:
        #     for sku in skus:
        #         if sku.id == sku_id:
        #             skus_li.append(sku)

        # 便利获取用户浏览的商品历史信息
        goods_li = []
        for id in sku_ids:
            # 根据id查询商品的信息
            goods = GoodsSKU.objects.get(id=id)
        #     # 追加到列表中
            goods_li.append(goods)

        # 组织模板上下文
        context = {
            'skus': skus,
            'address': address,
            'page': 'user'}

        # 除了我们给django传递的模板变量，django还会把user传递给模板文件
        return  render(request,'user_center_info.html',context)

# /user/order
class UserOrderView(LoginRequiredMixin,View):
    '''用户中心-订单页'''
    def get(self, request):
        '''显示'''
        # 获取用户的订单信息
        page = 'order'

        # 使用模板
        return render(request, 'user_center_order.html',{'page':page})

# /user/address
class AddressView(LoginRequiredMixin,View):
    '''用户中心-地址页'''
    def get(self, request):
        '''显示'''
        user = request.user  # 获取对应的用户对象

        # # 获取用户的默认收货地址
        # try:
        #     address = Address.objects.get(user=user, is_default=True)
        # except Address.DoesNotExist:
        #     address = None

        address = Address.object.get_default_address(user)

        page = 'addr'
        return render(request, 'user_center_site.html',{'page':page,'address':address})

    def post(self,request):
        # 接收数据
        receiver = request.POST.get('receiver')
        addr = request.POST.get('addr')
        zip_code = request.POST.get('zip_code')
        phone = request.POST.get('phone')
        # 校验数据
        if not all([receiver,addr,phone]):
            return render(request,'user_center_site.html',{'errmsg':'数据不完整'})

        # 校验手机号
        if not re.match(r'1[3|4|5|7|8][0-9]{9}$',phone):
            return render(request, 'user_center_site.html', {'errmsg': '手机号码格式错误'})
        # 业务处理:地址添加
        # 如果用户已经存在默认收货地址 添加的地址不作为默认收货地址 否则作为默认收货地址
        user = request.user # 获取对应的用户对象
        # try:
        #     address = Address.objects.get(user=user,is_default=True)
        # except Address.DoesNotExist:
        #     address = None

        address = Address.object.get_default_address(user)

        if address:
            is_default = False
        else:
            is_default = True

        # 添加地址
        Address.object.create(user=user,
                               receiver=receiver,
                               addr=addr,
                               zip_code=zip_code,
                               phone=phone,
                               is_default=is_default)

        # 返回应答
        return redirect(reverse('user:address'))