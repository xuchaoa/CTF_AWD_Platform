from rest_framework import serializers
from .models import CtfCompetitionTable,CtfSubmit
from ctf.serializers import CtfSerializer
from teams.models import TeamProfile
from info.models import CtfSubmit,CtfCompetitionTable
from ctf.models import CtfLibrary
from django.forms.models import model_to_dict


class CtfCompetitionTableSerializer(serializers.ModelSerializer):
    ctf = CtfSerializer()
    class Meta:
        model = CtfCompetitionTable
        fields = '__all__'


class CurrentTeamDefault(serializers.CurrentUserDefault):
    def set_context(self, serializer_field):
        self.user = serializer_field.context['request'].user
        self.ctf_id = serializer_field.context['request'].POST['submit_ctf']
        # team = TeamProfile.objects.filter()
        self.ctf = CtfCompetitionTable.objects.filter(ctf=self.ctf_id )
        # self.ctf = model_to_dict(self.ctf)
        # self.com = CtfCompetitionTable.objects.filter(ctf=self.ctf)

    def __call__(self):
        return self.ctf

class CtfSubmitSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    competition= serializers.HiddenField(default=CurrentTeamDefault())

    # def create(self, validated_data):
    #     print(validated_data)
    #     user = self.context['request'].user
    #


    class Meta:
        model = CtfSubmit
        fields = '__all__'

