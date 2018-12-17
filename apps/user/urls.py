from django.conf.urls import url
from apps.user import views

urlpatterns = [
    url(r'^register$', views.register, name='register'), #注册
    url(r'^register_handle$', views.register_handle, name='register_handle'), #注册

]