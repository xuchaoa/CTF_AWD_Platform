import xadmin
from . import models


class ChoiceLibraryDisplay(object):
    list_display = ['choice_question', 'choice_A', 'choice_B', 'choice_C', 'choice_D', 'choice_answer']
    search_fields = ['choice_question',  'choice_A', 'choice_B', 'choice_C', 'choice_D']
    list_filter = ['choice_question']
    list_per_page = 10
    ordering = ['id']
    readonly_fields = []
    exclude = []


xadmin.site.register(models.ChoiceLibrary, ChoiceLibraryDisplay)