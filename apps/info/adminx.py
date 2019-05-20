import xadmin

from . import models
from .models import CtfCompetitionTable, UserCompetitionInfo, TeamCompetitionInfo, Illegality,CtfSubmit


class CtfCompetitionTableDisplay(object):
    list_display = ('id','ctf','submit_times','competition')


xadmin.site.register(CtfCompetitionTable,CtfCompetitionTableDisplay)



class TeamCompetitionInfoDisplay(object):
    list_display = ['team', 'competition', 'score_all', 'score_choice', 'score_ctf', 'score_awd']
    search_fields = ['team__team_name', 'competition__competition_name','score_all', 'score_choice',
                     'score_ctf', 'score_awd']
    list_filter = ['competition', 'team', 'score_all', 'score_choice', 'score_ctf', 'score_awd']
    list_per_page = 10
    ordering = ['id']
    readonly_fields = []
    exclude = []


xadmin.site.register(models.TeamCompetitionInfo, TeamCompetitionInfoDisplay)


class UserCompetitionInfoDisplay(object):
    list_display = ['user', 'team', 'competition', 'score_all', 'score_choice', 'score_ctf', 'score_awd','wp']
    search_fields = ['user__username', 'team__team_name', 'competition__competition_name', 'score_all', 'score_choice',
                     'score_ctf', 'score_awd']
    list_filter = ['team', 'competition',  'score_all', 'score_choice', 'score_ctf', 'score_awd']
    list_per_page = 10
    ordering = ['id']
    readonly_fields = []
    exclude = []


xadmin.site.register(models.UserCompetitionInfo, UserCompetitionInfoDisplay)


class IllegalityDisplay(object):
    list_display = ['competition', 'team', 'user', 'illegality_time', 'illegality_action', 'illegality_times',
                    'illegality_duration', 'illegality_starttime', 'illegality_endtime', 'duration_status']
    search_fields = ['team__team_name', 'user__username', 'competition__competition_name']
    list_filter = ['competition', 'team', 'user', 'illegality_time', 'illegality_action', 'illegality_times',
                   'illegality_duration', 'illegality_starttime', 'illegality_endtime', 'duration_status']
    list_per_page = 10
    ordering = ['id']
    readonly_fields = []
    exclude = []


xadmin.site.register(models.Illegality, IllegalityDisplay)


class CompetitionChoiceSubmitDisplay(object):
    list_display = ['id','competition','team','user','score','choice','true_result','submit_result','result']
    list_per_page = 10
    ordering = ['id']
    readonly_fields = []
    exclude = []

xadmin.site.register(models.CompetitionChoiceSubmit,CompetitionChoiceSubmitDisplay)


class CtfSubmitDisplay(object):
    list_display = ('id', 'user','competition','submit_time','ctf','submit_flag','submit_result')
    list_per_page = 15
    ordering = ['id']

xadmin.site.register(CtfSubmit,CtfSubmitDisplay)

class UserChoiceInfoDisplay(object):
    list_display = ['id','user','team','submit_status','score']

xadmin.site.register(models.UserChoiceInfo,UserChoiceInfoDisplay)

