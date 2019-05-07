import xadmin
from .models import CtfLibrary

class CtfLibraryDisplay(object):
    list_display = ('id','ctf_title','ctf_description','ctf_score','ctf_address','ctf_flag')

xadmin.site.register(CtfLibrary,CtfLibraryDisplay)