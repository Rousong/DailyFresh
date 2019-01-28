from django.core.mail import send_mail
from django.conf import settings
# 使用celery
from celery import Celery
import time

# 在worker 任务处理者一端加这么几句 初始化环境变量
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dailyfresh.settings")
django.setup()

# 导入商品模块的模型
from apps.goods.models import GoodsType, IndexGoodsBanner, IndexPromotionBanner, IndexTypeGoodsBanner
# 导入模板对应的包
from django.template import loader, RequestContext
# 导入项目的配置文件
from django.conf import settings

# 创建一个Celery类的实例对象
# broker 是一个中间人 这里写redis的数据地址
app = Celery('celery_tasks.tasks', broker='redis://redis:6379/1')


# 定义任务函数
@app.task
def send_register_active_email(to_email, username, token):
    '''发送激活邮件'''
    # 组织邮件信息
    subject = '天天生鲜用户激活'
    message = ""
    sender = settings.EMAIL_FROM
    receiver = [to_email]
    html_mesg = "<h1>%s,欢迎您注册天天生鲜</h1>请点击以下链接激活您的账户</br><a href='http://127.0.0.1:8000/user/active/%s'>http://127.0.0.1:8000/user/active/%s</a>" % (
        username, token, token)
    send_status = send_mail(subject, message, sender, receiver, html_message=html_mesg)
    print(send_status)
    time.sleep(20)


@app.task
def generate_static_index():
    """生成静态的首页"""
    # 查询商品的分类信息
    types = GoodsType.objects.all()
    # 获取首页轮播的商品的信息
    index_banner = IndexGoodsBanner.objects.all().order_by('index')
    # 获取首页促销的活动信息
    promotion_banner = IndexPromotionBanner.objects.all().order_by('index')

    # 获取首页分类商品信息展示
    for type in types:
        # 查询首页显示的type类型的文字商品信息
        title_banner = IndexTypeGoodsBanner.objects.filter(type=type, display_type=0).order_by('index')
        # 查询首页显示的图片商品信息
        image_banner = IndexTypeGoodsBanner.objects.filter(type=type, display_type=1).order_by('index')
        # 动态给type对象添加两个属性保存数据
        type.title_banner = title_banner
        type.image_banner = image_banner

    # 获取登录用户的额购物车中的商品的数量
    cart_count = 0

    # 组织上下文
    context = {
        'types': types,
        'index_banner': index_banner,
        'promotion_banner': promotion_banner,
        'cart_count': cart_count
    }

    # 生成静态首页的内容 render 》 HttpResponse对象
    # 1. 加载模板文件
    template = loader.get_template('static_index.html')
    # 2. 渲染模板,生成HTML
    static_index_html = template.render(context)
    # 3.保存生成的静态页面,保存在static文件夹下面
    static_path = os.path.join(settings.BASE_DIR, 'static/index.html')

    # 开始保存数据
    with open(static_path, 'w') as file:
        file.write(static_index_html)
