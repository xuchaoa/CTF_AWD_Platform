from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class TeamProfile(models.Model):
    team_name = models.CharField(max_length=50,default='',verbose_name='队伍名称')


    class Meta:
        db_table = 'TeamProfile'
        verbose_name = '队伍管理'

    def __str__(self):
        return self.team_name