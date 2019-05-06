import xadmin
from . import models
from .models import CtfCompetitionTable, UserCompetitionInfo, TeamCompetitionInfo, Illegality

class CtfCompetitionTableDisplay(object):
    list_display = ('id','submit_times','competition','ctf')


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
    list_display = ['user', 'team', 'competition', 'score_all', 'score_choice', 'score_ctf', 'score_awd']
    search_fields = ['user__username', 'team__team_name', 'competition__competition_name', 'score_all', 'score_choice',
                     'score_ctf', 'score_awd']
    list_filter = ['team', 'competition',  'score_all', 'score_choice', 'score_ctf', 'score_awd']
    list_per_page = 10
    ordering = ['id']
    readonly_fields = []
    exclude = []


xadmin.site.register(models.UserCompetitionInfo, UserCompetitionInfoDisplay)


class IllegalityDisplay(object):
    list_display = ['competition', 'team', 'user', 'illegality_time', 'illegality_action', 'illegality_timea',
                    'illegality_duration', 'illegality_starttime', 'illegality_endtime', 'duration_status']
    search_fields = ['team__team_name', 'user__username', 'competition__competition_name']
    list_filter = ['competition', 'team', 'user', 'illegality_time', 'illegality_action', 'illegality_timea',
                   'illegality_duration', 'illegality_starttime', 'illegality_endtime', 'duration_status']
    list_per_page = 10
    ordering = ['id']
    readonly_fields = []
    exclude = []


xadmin.site.register(models.Illegality, IllegalityDisplay)