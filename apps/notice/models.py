from django.db import models
from competition.models import CompetitionProfile
from django.utils import timezone


# Create your models here.

class NoticeProfile(models.Model):
    '''
    公告
    '''
    notice_time = models.DateTimeField(default=timezone.now, null=True, verbose_name="公告时间")
    notice_title = models.TextField(null=True, verbose_name="公告题目")
    notice_content = models.TextField(null=True, verbose_name="公告内容")
    notice_competition = models.ForeignKey(CompetitionProfile, null=True, on_delete=models.CASCADE, verbose_name="比赛名称",
                                           related_name='competition_name1')

    class Meta:
        verbose_name = '比赛公告'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.id)