from django.db import models

# Create your models here.


class CtfLibrary(models.Model):
    '''
    CTF题库
    '''
    ctf_type = models.SmallIntegerField()
    ctf_title = models.CharField()
    ctf_description = models.TextField()
    ctf_score = models.IntegerField()
    ctf_address = models.CharField()
    ctf_flag = models.CharField()

    class Meta:
        verbose_name = 'CTF题库'
        verbose_name_plural = verbose_name