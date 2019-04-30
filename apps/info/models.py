from django.db import models

# Create your models here.

from teams.models import TeamProfile
from competition.models import CompetitionProfile
from users.models import UserProfile
from ctf.models import CtfLibrary
from django.utils import timezone

class TeamCompetitionInfo(models.Model):
    '''
    队伍比赛团队得分表
    '''
    team = models.ForeignKey(TeamProfile,on_delete=models.CASCADE,verbose_name='队伍')
    competition = models.ForeignKey(CompetitionProfile,on_delete=models.CASCADE,verbose_name='比赛')
    score_all = models.IntegerField()
    score_choice = models.IntegerField()
    score_ctf = models.IntegerField()
    score_awd = models.IntegerField()

    class Meta:
        verbose_name = '比赛情况'
        verbose_name_plural = verbose_name
        unique_together = ('team','competition')  #多个字段作为一个联合唯一索引


class UserCompetitionInfo(models.Model):
    '''
    团队比赛个人得分表
    '''
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE,verbose_name='队员')
    team = models.ForeignKey(TeamProfile,on_delete=models.CASCADE,verbose_name='队伍')
    competition = models.ForeignKey(CompetitionProfile,on_delete=models.CASCADE,verbose_name='比赛')
    score_all = models.IntegerField()
    score_choice = models.IntegerField()
    score_ctf = models.IntegerField()
    score_awd = models.IntegerField()

    class Meta:
        verbose_name = '比赛情况'
        verbose_name_plural = verbose_name
        unique_together = ('user','team', 'competition')

class Illegality(models.Model):
    '''
    团队比赛违规表
    '''
    illegality_type = (
        (0, '作弊'),
        (1, '攻击平台'),
        (2, '其他')
    )
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='队员')
    team = models.ForeignKey(TeamProfile, on_delete=models.CASCADE, verbose_name='队伍')
    competition = models.ForeignKey(CompetitionProfile, on_delete=models.CASCADE, verbose_name='比赛')
    illegality_time = models.DateTimeField(default=timezone.now,verbose_name='')
    illegality_action = models.SmallIntegerField(choices=illegality_type,default=2)
    illegality_timea = models.IntegerField(verbose_name='违规次数')
    illegality_duration = models.IntegerField(verbose_name='封禁时间')
    illegality_starttime = models.DateTimeField(verbose_name='封禁开始时间')
    illegality_endtime = models.DateTimeField(verbose_name='封禁结束时间')
    duration_status = models.BooleanField(verbose_name='封禁状态')

    class Meta:
        verbose_name = '比赛违规'
        verbose_name_plural = verbose_name
        unique_together = ('user', 'team', 'competition')





class CtfCompetitionTable(models.Model):
    '''
    每场比赛的CTF题目
    '''
    ctf = models.ForeignKey(CtfLibrary,on_delete=models.CASCADE,verbose_name='')
    competition = models.ForeignKey(CompetitionProfile,on_delete=models.CASCADE,verbose_name='')
    submit_times = models.IntegerField()

    class Meta:
        verbose_name = '比赛CTF题目'
        verbose_name_plural = verbose_name
        unique_together = ('ctf','competition')


class CtfSubmit(models.Model):
    pass