from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Team_Profile(models.Model):
    team_name = models.CharField(max_length=50,default='',verbose_name='队伍名称')

    def __str__(self):
        return self.team_name