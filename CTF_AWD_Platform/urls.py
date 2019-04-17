"""CTF_AWD_Platform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
import xadmin
from django.conf import settings
from django.conf.urls.static import static
# from apps.extra_apps.pydash import pydash


#rest
from django.conf.urls import url, include
from rest_framework import routers
from apps.x_user import views
#
router = routers.DefaultRouter() #路由
router.register('user',views.UserListView,base_name='user')
# router.register('test',views.TestView,base_name='test')
from rest_framework_jwt.views import obtain_jwt_token,refresh_jwt_token,verify_jwt_token



urlpatterns = [
    # path('admin/', admin.site.urls),
    path('x_admin/',xadmin.site.urls),
    # path('',include('apps.x_user.urls')),
    #rest
    re_path(r'^api/', include(router.urls)), #包含进路由配置的url
    re_path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')), #浏览器测试接口配置
    path('api-token-auth/',obtain_jwt_token),
    path('api-token-refresh/',refresh_jwt_token),  #刷新token api  只有非过期token才有效
    path('api-token-verify/',verify_jwt_token),  # API View that checks the veracity of a token, returning the token if it is valid
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)