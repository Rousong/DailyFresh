# -*- coding:utf-8 -*-
from django.contrib import admin
from apps.goods.models import GoodsType,IndexGoodsBanner,GoodsSKU,Goods
# Register your models here.

class IndexPromotionBannerAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        '''新增或者更新表中的数据时调用'''
        super(IndexPromotionBannerAdmin,self).save_model(request, obj, form, change)

        # 发出任务,让celery worker重新生成首页静态页
        from celery_tasks.tasks import generate_static_index
        generate_static_index.delay()

    def delete_model(self, request, obj):
        """删除数据的时候调用"""
        # 调用父类的方法来实现数据的删除
        super(IndexPromotionBannerAdmin,self).delete_model(request, obj)

        # 附加的操作：重新生成首页的静态文件
        from celery_tasks.tasks import generate_static_index
        generate_static_index.delay()


admin.site.register(GoodsType)
admin.site.register(GoodsSKU)
admin.site.register(Goods)
admin.site.register(IndexGoodsBanner,IndexPromotionBannerAdmin)