from django.db import models
from django.contrib.auth.models import AbstractUser
from competition.models import CompetitionProfile
# Create your models here.


class TeamProfile(models.Model):
    team_name = models.CharField(max_length=50,default='',verbose_name='队伍名称')
    team_captain = models.CharField(max_length=50,default='',verbose_name='队长')
    team_member1 = models.CharField(max_length=50,default='',verbose_name='队员1')
    team_member2 = models.CharField(max_length=50,default='',verbose_name='队员2')
    team_member3 = models.CharField(max_length=50,default='',verbose_name='队员3')
    competition_id = models.ForeignKey(CompetitionProfile,null=True,blank=True,on_delete=models.SET_NULL,related_name='team_competition')


    class Meta:
        db_table = 'TeamProfile'
        verbose_name = '团队管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.team_name