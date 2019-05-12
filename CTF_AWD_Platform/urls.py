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
from django.urls import path, re_path
import xadmin
from django.conf import settings
from django.conf.urls.static import static
# from apps.extra_apps.pydash import pydash
from rest_framework.documentation import include_docs_urls

# rest
from django.conf.urls import include
from rest_framework import routers
from users.views import UserViewset, SmsCodeViewset, UserLogViewSet
from teams.views import TeamViewSet
from competition.views import CompetitionViewSet
from notice.views import NoticeViewSet
from info.views import TeamCompetitionInfoViewSet, UserCompetitionInfoViewSet, IllegalityViewSet, \
    CtfCompetitionTableViewSet, CtfSubmitViewSet,CompetitionChoiceSubmitViewSet,UserChoiceInfoViewSet

#
router = routers.DefaultRouter()  # 路由
router.register('users', UserViewset, base_name='users')
router.register('codes', SmsCodeViewset, base_name='codes')
router.register('teams', TeamViewSet, base_name='teams')
router.register('competitions', CompetitionViewSet, base_name='competitions')
router.register('logs', UserLogViewSet, base_name='logs')

router.register('notices', NoticeViewSet, base_name='notices')
router.register('teamCompetitionInfos', TeamCompetitionInfoViewSet, base_name='teamCompetitionInfos')
router.register('userCompetitionInfos', UserCompetitionInfoViewSet, base_name='userCompetitionInfos')
router.register('illegalityInfos', IllegalityViewSet, base_name='illegalityInfos')
router.register('CtfCompetitionTables', CtfCompetitionTableViewSet, base_name='CtfCompetitionTables')
router.register('CtfSubmits', CtfSubmitViewSet, base_name='CtfSubmits')
router.register('CompetitionChoiceSubmits', CompetitionChoiceSubmitViewSet, base_name='UserChoiceInfos')
router.register('UserChoiceInfos', UserChoiceInfoViewSet, base_name='CompetitionChoiceSubmits')

# router.register('test',views.PermissionTestViewSet,base_name='test')


from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('x_admin/', xadmin.site.urls),
    # path('',include('apps.x_user.urls')),
    # rest
    re_path(r'^api/', include(router.urls)),  # 包含进路由配置的url
    re_path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),  # 浏览器测试的登录接口
    path('api-token-auth/', obtain_jwt_token),
    path('api-token-refresh/', refresh_jwt_token),  # 刷新token api  只有非过期token才有效
    path('api-token-verify/', verify_jwt_token),
    # API View that checks the veracity of a token, returning the token if it is valid
    path('docs/', include_docs_urls(title='SDUTCTF')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
