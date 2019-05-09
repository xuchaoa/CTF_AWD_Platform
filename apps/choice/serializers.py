from rest_framework import serializers
from .models import ChoiceLibrary


class ChoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChoiceLibrary
        fields = ('choice_question','choice_a','choice_b','choice_c','choice_d')