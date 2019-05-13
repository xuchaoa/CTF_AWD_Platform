from django.db import models
from competition.models import CompetitionProfile
# from users.models import UserProfile
from django.contrib.auth import get_user_model

UserProfile = get_user_model()

# Create your models here.


class TeamProfile(models.Model):
    '''
    team表
    '''
    team_name = models.CharField(max_length=50,null=True,blank=False,verbose_name='队伍名称')
    team_captain = models.ForeignKey(UserProfile,null=True,blank=True,on_delete=models.CASCADE,related_name='team_captain',verbose_name='队长')
    team_member1 = models.ForeignKey(UserProfile,null=True,blank=True,on_delete=models.SET_NULL,related_name='team_member1')
    team_member2 = models.ForeignKey(UserProfile,null=True,blank=True,on_delete=models.SET_NULL,related_name='team_member2')
    team_member3 = models.ForeignKey(UserProfile,null=True,blank=True,on_delete=models.SET_NULL,related_name='team_member3')
    team_token = models.CharField(max_length=30,default=None)
    competition = models.ForeignKey(CompetitionProfile,null=True,blank=True,on_delete=models.SET_NULL,related_name='team_competition')


    class Meta:
        db_table = 'TeamProfile'
        verbose_name = '团队管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.team_name