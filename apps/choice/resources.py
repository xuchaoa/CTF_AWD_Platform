from import_export import resources, fields
from .models import ChoiceLibrary


class ChoiceResource(resources.ModelResource):

    choice_question = fields.Field(attribute='choice_question', column_name='问题描述')
    choice_a = fields.Field(attribute='choice_a', column_name='选项A')
    choice_b = fields.Field(attribute='choice_b', column_name='选项B')
    choice_c = fields.Field(attribute='choice_c', column_name='选项C')
    choice_d = fields.Field(attribute='choice_d', column_name='选项D')
    choice_answer = fields.Field(attribute='choice_answer', column_name='正确答案')
    choice_score = fields.Field(attribute='choice_score', column_name='分数')

    class Meta:
        model = ChoiceLibrary
        fields = ( 'choice_question', 'choice_a', 'choice_b', 'choice_c', 'choice_d', 'choice_answer', 'choice_score')
        exclude = ('id')
        import_id_fields = ['choice_question']