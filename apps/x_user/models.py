from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.x_team.models import Team_Profile
from django.utils import timezone

# Create your models here.


class User_Profile(AbstractUser):
    '''
    自定义的 User Model
    可以只先填写user_name
    任何字段不能传空字符
    blank 表示后端是不是必须填写
    '''
    gender_choices = (
        (0,'男'),
        (1,'女'),
        (2,'未知')
    )
    user_name = models.CharField(max_length=30, null=False, blank=False, verbose_name="姓名")
    user_password = models.CharField(max_length=50, null=False, blank=False, verbose_name="密码")
    user_school = models.CharField(max_length=30, null=True, blank=False, verbose_name="学校")
    user_major = models.CharField(max_length=30, null=True, blank=False, verbose_name="专业班级")
    user_phone = models.CharField(max_length=11, null=True, blank=False, verbose_name="手机")
    user_number = models.CharField(max_length=11,null=True,blank=False,verbose_name='学号')
    user_email = models.CharField(max_length=30,null=True,blank=False,verbose_name='邮箱')
    user_image = models.ImageField(upload_to='avatar/%Y/%m/%d',verbose_name='头像',default='')
    user_url = models.CharField(max_length=36, null=True, blank=False, verbose_name='个人网址')
    user_gender = models.SmallIntegerField(choices=gender_choices,default=2)
    user_ip = models.CharField(max_length=15,null=True,blank=False,verbose_name='ip')
    user_team_id = models.ForeignKey(Team_Profile,null=True,blank=True,on_delete=models.SET_NULL,related_name='user_team121')
    user_str = models.CharField(max_length=36,null=False, blank=False,verbose_name='随机字符串')
    user_registertime = models.DateTimeField(default=timezone.now,verbose_name='注册时间')

    class Meta:
        db_table = 'User_Profile'
        verbose_name = '用户'  #后台显示的字段信息
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user_name