import xadmin
from .models import CtfCompetitionTable,CtfSubmit

class CtfCompetitionTableDisplay(object):
    list_display = ('id','ctf','submit_times','competition')


xadmin.site.register(CtfCompetitionTable,CtfCompetitionTableDisplay)


class CtfSubmitDisplay(object):
    list_display = ('id', 'user','competition','submit_time','ctf','submit_flag','submit_result')

xadmin.site.register(CtfSubmit,CtfSubmitDisplay)