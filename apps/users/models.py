from django.db import models
from django.contrib.auth.models import AbstractUser
# from teams.models import TeamProfile
from django.utils import timezone
import datetime
from django.utils import timezone

# Create your models here.


class UserProfile(AbstractUser):
    '''
    自定义的 User Model，权衡之后决定继承自AbstractUser，如果功能拓展限制后续考虑继承自AbstractBaseUser
    可以只先填写user_name
    任何字段不能传空字符
    blank 表示后端是不是必须填写
    添加verbose_name用于xadmin，help_text用于drf
    '''
    gender_choices = (
        (0,'男'),
        (1,'女'),
        (2,'未知')
    )
    # user_name = models.CharField(max_length=30, null=False, blank=True, verbose_name="姓名",help_text='姓名')
    # user_password = models.CharField(max_length=50, null=False, blank=True, verbose_name="密码")
    user_school = models.CharField(max_length=30, null=True, blank=True, verbose_name="学校",help_text='学校')
    user_major = models.CharField(max_length=30, null=True, blank=True, verbose_name="专业班级",help_text='专业班级')
    user_phone = models.CharField(max_length=11, null=True, blank=True,unique=True, verbose_name="手机")
    user_number = models.CharField(max_length=11,null=True,blank=True,unique=True,verbose_name='学号',help_text='学号')
    # user_email = models.CharField(max_length=30,null=True,blank=True,unique=True,verbose_name='邮箱')
    user_image = models.ImageField(upload_to='avatar/%Y/%m/%d',verbose_name='头像',blank=True)
    user_url = models.CharField(max_length=36, null=True, blank=True, verbose_name='个人网址')
    user_gender = models.SmallIntegerField(choices=gender_choices,default=2)
    user_ip = models.CharField(max_length=15,null=True,blank=True,verbose_name='ip')
    # user_team = models.ForeignKey(TeamProfile,null=True,blank=True,on_delete=models.SET_NULL,related_name='user_team')
    user_str = models.CharField(max_length=36,null=False, blank=True,verbose_name='随机字符串')
    user_registertime = models.DateTimeField(default=timezone.now,verbose_name='注册时间')

    class Meta:
        db_table = 'UserProfile'
        verbose_name = '用户管理'  #后台显示的字段信息
        verbose_name_plural = verbose_name
        ordering = ['id']  # fix #20
        # abstract = True

    def __str__(self):
        return self.username



class VerifyCode(models.Model):
    """
    验证码
    """
    code = models.CharField(max_length=10, verbose_name="验证码")
    mobile = models.CharField(max_length=30, verbose_name="电话或邮箱")
    type = models.CharField(default='mobile',max_length=25,verbose_name='类型')
    add_time = models.DateTimeField(default=timezone.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "短信验证"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code


class UserLoginLog(models.Model):
    user = models.ForeignKey(UserProfile,null=True,blank=True,on_delete=models.CASCADE,verbose_name='用户',related_name='user_log')
    user_login_time = models.DateTimeField(default=timezone.now,verbose_name='登陆时间')
    user_login_ip = models.CharField(max_length=15,verbose_name='登陆ip')
    user_login_agent = models.CharField(max_length=200,verbose_name='UA')
    user_login_os = models.CharField(max_length=100,verbose_name='OS')

    class Meta:
        verbose_name = '登录日志'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{}.{}'.format(self.user.username,self.user_login_ip)
