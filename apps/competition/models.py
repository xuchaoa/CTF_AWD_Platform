from django.db import models

# Create your models here.

class CompetitionProfile(models.Model):
    competition_type_choice = (
        (0,'CTF'),
        (1,'AWD'),
        (2,'CHOICE'),
        (3,'CTF&CHOICE'),
        (4,'CTF&AWD'),
        (5,'CHOICE&AWD'),
        (6,'CHOICE&AWD&CTF'),
    )
    competition_name = models.CharField(max_length=30,null=True, blank=False, verbose_name="比赛名称")
    competition_type = models.SmallIntegerField(choices=competition_type_choice,default=6,verbose_name='比赛类别')
    competition_choicenum = models.CharField(max_length=30,null=True, blank=False, verbose_name="选择题数量")

    class Meta:
        verbose_name = '比赛设置'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.competition_name
