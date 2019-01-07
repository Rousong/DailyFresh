from django.shortcuts import render, redirect
from django.views.generic import View
from apps.order.models import OrderGoods
from apps.goods.models import GoodsSKU, GoodsType, IndexGoodsBanner,IndexPromotionBanner,IndexTypeGoodsBanner
from django.urls import reverse # django2.0 把原来的 django.core.urlresolvers 包 更改为了 django.urls包
from django_redis import get_redis_connection

from django.core.paginator import Paginator
# 使用缓存导入相关的包
from django.core.cache import cache

class IndexView(View):
    """首页"""
    def get(self, request):
        """显示"""
        # 先判断缓存中是否有数据,没有数据不会报错返回NONE
        context = cache.get('index_page_data')

        if context is None:

            # 查询商品的分类信息
            types = GoodsType.objects.all()
            # 获取首页轮播的商品的信息
            index_banner = IndexGoodsBanner.objects.all().order_by('index')
            # 获取首页促销的活动信息
            promotion_banner = IndexPromotionBanner.objects.all().order_by('index')

            # 获取首页分类商品信息展示
            for type in types:
                # 查询首页显示的type类型的文字商品信息
                title_banner = IndexTypeGoodsBanner.objects.filter(type=type, display_type = 0).order_by('index')
                # 查询首页显示的图片商品信息
                image_banner = IndexTypeGoodsBanner.objects.filter(type= type, display_type = 1).order_by('index')
                # 动态给type对象添加两个属性保存数据
                type.title_banner = title_banner
                type.image_banner = image_banner



            # 组织上下文
            context = {
                'types': types,
                'index_banner': index_banner,
                'promotion_banner': promotion_banner,
            }
            # 设置缓存数据,缓存的名字，内容，过期的时间
            cache.set('index_page_data', context, 3600)

        # 获取user
        user = request.user
        # 获取登录用户的额购物车中的商品的数量
        cart_count = 0

        # is_authenticated这个是个属性而不是一个方法 之前写成 is_authenticated()会
        # 报'bool' object is not callable的错误
        if user.is_authenticated:
            # 用户已经登录
            conn = get_redis_connection('default')
            cart_key = 'cart_%d' % user.id

            # 获取用户购物车中国的商品条目数
            cart_count = conn.hlen(cart_key)

            context.update(cart_count = cart_count)

        return render(request, 'index.html', context)