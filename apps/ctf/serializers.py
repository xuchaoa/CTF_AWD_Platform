from rest_framework import serializers
from .models import CtfLibrary



class CtfSerializer(serializers.ModelSerializer):
    '''
    注意隐藏敏感字段
    '''

    class Meta:
        model = CtfLibrary
        fields = ('id','ctf_type','ctf_title','ctf_description','ctf_score','ctf_address')