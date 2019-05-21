from django.db import models

# Create your models here.

from teams.models import TeamProfile
from competition.models import CompetitionProfile
from users.models import UserProfile
from ctf.models import CtfLibrary
from choice.models import ChoiceLibrary
from django.utils import timezone


class TeamCompetitionInfo(models.Model):
    '''
    队伍比赛团队得分表
    '''
    team = models.ForeignKey(TeamProfile, on_delete=models.CASCADE, verbose_name='队伍',default=None)
    competition = models.ForeignKey(CompetitionProfile, on_delete=models.CASCADE, verbose_name='比赛',default=None)
    score_all = models.IntegerField(default=0, verbose_name="队伍总得分")
    score_choice = models.IntegerField(default=0, verbose_name="选择题得分")
    score_ctf = models.IntegerField(default=0, verbose_name="ctf分数")
    score_awd = models.IntegerField(default=0, verbose_name="awd分数")

    class Meta:
        ordering = ['-score_all']
        verbose_name = '团队比赛详情'
        verbose_name_plural = verbose_name
        unique_together = ('team', 'competition')  # 多个字段作为一个联合唯一索引

    def __str__(self):
        return str(self.id)

from CTF_AWD_Platform.settings import MEDIA_ROOT

def upload_to(instance,filename):
    return '/'.join([MEDIA_ROOT+'/upload/wp_upload',instance.competition.competition_name,instance.team.team_name,instance.user.username,filename])


class UserCompetitionInfo(models.Model):
    '''
    团队比赛个人得分表
    '''
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='队员',related_name='user_info',default=None)
    team = models.ForeignKey(TeamProfile, on_delete=models.CASCADE, verbose_name='队伍',default=None)
    competition = models.ForeignKey(CompetitionProfile, on_delete=models.CASCADE, verbose_name='比赛',related_name='user_competition')
    score_all = models.IntegerField(default=0, verbose_name="个人总分")
    score_choice = models.IntegerField(default=0, verbose_name="选择题分数")
    score_ctf = models.IntegerField(default=0, verbose_name="ctf总分")
    score_awd = models.IntegerField(default=0, verbose_name="awd总分")
    wp = models.FileField(null=True,blank=True,upload_to=upload_to)

    class Meta:
        verbose_name = '个人比赛详情'
        verbose_name_plural = verbose_name
        unique_together = ('user', 'team', 'competition')

    def __str__(self):
        return str(self.id)


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
    illegality_time = models.DateTimeField(default=timezone.now, verbose_name='添加记录的时间')
    illegality_action = models.SmallIntegerField(choices=illegality_type, default=2, verbose_name="行为")
    illegality_times = models.IntegerField(verbose_name='违规次数',default=1)
    illegality_duration = models.IntegerField(verbose_name='封禁时间(分钟)')
    illegality_starttime = models.DateTimeField(verbose_name='封禁开始时间')
    illegality_endtime = models.DateTimeField(verbose_name='封禁结束时间')
    duration_status = models.BooleanField(verbose_name='封禁状态')

    class Meta:
        verbose_name = '比赛违规'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username


class CtfCompetitionTable(models.Model):
    '''
    每场比赛的CTF题目,包括提交次数字段
    '''
    ctf = models.ForeignKey(CtfLibrary, on_delete=models.CASCADE, verbose_name='题目编号',default=None)
    competition = models.ForeignKey(CompetitionProfile, on_delete=models.CASCADE, verbose_name='比赛编号',default=None)
    submit_times = models.IntegerField(default=0, verbose_name='正确提交次数')

    class Meta:
        verbose_name = '比赛CTF题目'
        verbose_name_plural = verbose_name
        unique_together = ('ctf', 'competition')
    def __str__(self):
        return '{}.{}'.format(self.ctf,self.competition)


class CtfSubmit(models.Model):
    '''
    CTF提交flag表
    '''
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='队员',default=None)
    competition = models.ForeignKey(CompetitionProfile, on_delete=models.CASCADE, verbose_name='比赛',default=None)
    ctf = models.ForeignKey(CtfLibrary, on_delete=models.CASCADE, verbose_name="提交题目",default=None)
    submit_time = models.DateTimeField(default=timezone.now, verbose_name="提交时间")
    submit_flag = models.CharField(max_length=255, verbose_name="提交flag")
    submit_result = models.BooleanField(verbose_name="判定结果")

    class Meta:
        verbose_name = 'CTF提交记录'
        verbose_name_plural = verbose_name





class AwdSubmit(models.Model):
    '''
    AWD攻防提交flag表
    '''
    team = models.ForeignKey(TeamProfile, on_delete=models.CASCADE, verbose_name='队伍',default=None)
    competition = models.ForeignKey(CompetitionProfile, on_delete=models.CASCADE, verbose_name='比赛',
                                    related_name="competition_id",default=None)
    awd_submit_time = models.DateTimeField(default=timezone.now, verbose_name="提交时间")
    awd_submit_team = models.ForeignKey(TeamProfile, on_delete=models.CASCADE, verbose_name="目标队伍编号",
                                          related_name="team_id",default=None)
    awd_submit_flag = models.CharField(max_length=255, verbose_name="提交flag")
    awd_submit_result = models.BooleanField(verbose_name="判定结果")

    class Meta:
        verbose_name = 'AWD提交flag'
        verbose_name_plural = verbose_name
        unique_together = ('team', 'competition')


class CompetitionChoiceSubmit(models.Model):
    '''
    选择题抽取题目&提交记录
    '''
    result_choice = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D')
    )
    competition = models.ForeignKey(CompetitionProfile, on_delete=models.CASCADE, related_name="competition_choice",default=None)
    team = models.ForeignKey(TeamProfile, on_delete=models.CASCADE, verbose_name='队伍',default=None)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_choice_submit', default=None)
    choice = models.ForeignKey(ChoiceLibrary, on_delete=models.CASCADE, verbose_name="选择题ID",
                               related_name="choice_choice",default=None)
    score = models.IntegerField()
    true_result = models.CharField(max_length=2,choices=result_choice,verbose_name='正确答案')
    submit_result = models.CharField(max_length=2,choices=result_choice,null=True,blank=True,verbose_name='提交的答案')
    result = models.BooleanField(null=True,blank=True,verbose_name='答案是否正确')

    def __str__(self):
        return '{}.{}.{}'.format(self.competition,self.team,self.user)

    class Meta:
        verbose_name = '比赛选择题题目及提交状况'
        verbose_name_plural = verbose_name
        unique_together = ('competition','team','user', 'choice')


class UserChoiceInfo(models.Model):
    '''
    用户选择题情况表
    '''
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='user_choice_1',default=None)
    team = models.ForeignKey(TeamProfile,on_delete=models.CASCADE,related_name='team_choice_1',default=None)
    competition = models.ForeignKey(CompetitionProfile,on_delete=models.CASCADE,related_name='competition_choice_info',default=None)
    submit_status = models.NullBooleanField(default=None)  #默认为NULL
    score = models.IntegerField(default=0)

    def __str__(self):
        return "{}.{}".format(self.team,self.user)

    class Meta:
        verbose_name = '用户选择题情况表'
        verbose_name_plural = verbose_name
        unique_together = ('user', 'team','competition')


