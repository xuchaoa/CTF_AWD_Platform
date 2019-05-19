import xadmin
from . import models
from . import resources


class ChoiceLibraryDisplay(object):
    import_export_args = {'import_resource_class': resources.ChoiceResource}
    list_display = ['choice_question', 'choice_a', 'choice_b', 'choice_c', 'choice_d', 'choice_answer', 'choice_score']
    search_fields = ['choice_question', 'choice_a', 'choice_b', 'choice_c', 'choice_d']
    list_filter = ['choice_question']
    list_per_page = 10
    ordering = ['id']
    readonly_fields = []
    exclude = []


xadmin.site.register(models.ChoiceLibrary, ChoiceLibraryDisplay)
