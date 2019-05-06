import xadmin
from .models import CtfCompetitionTable

class CtfCompetitionTableDisplay(object):
    list_display = ('id','submit_times','competition','ctf')


xadmin.site.register(CtfCompetitionTable,CtfCompetitionTableDisplay)