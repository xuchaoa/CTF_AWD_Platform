from django.db import models
from competition.models import CompetitionProfile
# Create your models here.


class CtfLibrary(models.Model):
    '''
    CTF题库
    '''
    ctf_type_choice = (
        (0, 'WEB'),
        (1, 'REVERSE'),
        (2, 'MISC'),
        (3, 'STEGA'),
        (4, 'PWN'),
        (5, 'CRYPTO'),
        (6, 'PPC'),
    )
    ctf_type = models.IntegerField(default=0,choices=ctf_type_choice,verbose_name='题目类型',help_text='')
    ctf_title = models.CharField(max_length=30, null=True, verbose_name="题目标题")
    ctf_description = models.TextField(max_length=255, null=True, verbose_name="题目描述")
    ctf_score = models.IntegerField(default=0, verbose_name="题目分数")
    ctf_address = models.CharField(max_length=255, null=True, verbose_name="题目地址")
    ctf_flag = models.CharField(max_length=255, null=True, verbose_name="flag")

    class Meta:
        verbose_name = '题库'
        verbose_name_plural = verbose_name