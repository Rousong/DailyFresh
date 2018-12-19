from django.conf.urls import url
from apps.user import views
from apps.user.views import RegisterView,ActiveView,LoginView
urlpatterns = [
    #url(r'^register$', views.register, name='register'), #注册
    #url(r'^register_handle$', views.register_handle, name='register_handle'), #注册
    url(r'^register$',RegisterView.as_view(), name='register'),#注册
    url(r'^active/(?P<token>.*)$',ActiveView.as_view(),name='active'),#用户激活
    url(r'^login$',LoginView.as_view(),name='login'), # 登录
]