from rest_framework import serializers
from .models import CtfLibrary



class CtfSerializer(serializers.ModelSerializer):

    class Meta:
        model = CtfLibrary
        fields = '__all__'