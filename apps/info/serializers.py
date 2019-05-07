from rest_framework import serializers
from .models import CtfCompetitionTable,CtfSubmit
from ctf.serializers import CtfSerializer
from teams.models import TeamProfile
from info.models import CtfSubmit,CtfCompetitionTable
from ctf.models import CtfLibrary
from django.forms.models import model_to_dict
from django.db.models import Q
from .models import Illegality, UserCompetitionInfo, TeamCompetitionInfo


class TeamCompetitionInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = TeamCompetitionInfo
        fields = "__all__"


class UserCompetitionInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserCompetitionInfo
        fields = "__all__"


class IllegalitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Illegality
        fields = "__all__"



class CtfCompetitionTableSerializer(serializers.ModelSerializer):
    ctf = CtfSerializer()
    class Meta:
        model = CtfCompetitionTable
        fields = '__all__'


class CurrentCompetitionDefault(serializers.CurrentUserDefault):
    '''
    决定了每个用户只能在一个队伍中
    '''
    def set_context(self, serializer_field):
        self.user = serializer_field.context['request'].user
        team = TeamProfile.objects.get(team_captain=self.user)
        self.competition = team.competition


        self.ctf_id = serializer_field.context['request'].POST['ctf']
        # team = TeamProfile.objects.filter()
        self.ctf_competition = CtfCompetitionTable.objects.filter(ctf=self.ctf_id )
        # self.ctf = model_to_dict(self.ctf)
        # self.com = CtfCompetitionTable.objects.filter(ctf=self.ctf)
        self.ctf = self.ctf_competition.model.ctf
        self.com = self.ctf_competition.model.competition

    def __call__(self):
        return self.competition



class CtfSubmitAddSerializer(serializers.ModelSerializer):
    '''
    1.需要判断用户时都参加该比赛(不进行判断，后端自动填充)  ok
    2.是否在比赛时间内 TODO this
    3.判断用户提交的flag是否正确  ok 并更改相应表格 ok
    4.已经提交过正确答案则不允许再次提交  ok
    '''
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    competition= serializers.HiddenField(default=CurrentCompetitionDefault())
    submit_flag = serializers.CharField(required=True,allow_blank=False,help_text='在此处提交flag',label='flag',
                                        error_messages={
                                            'blank':'提交的flag为空',  #先验证这里，才会进入validate
                                            'required':'未提交任何flag'
                                        })
    submit_time = serializers.DateTimeField(read_only=True,format='%Y-%m-%d %H:%M:%S')
    submit_result = serializers.BooleanField(default=False,read_only=True)

    # def create(self, validated_data):
    #     print(validated_data)
    #     user = self.context['request'].user
    #


    # def validate_submit_flag(self, submit_flag):
    #     if self.validated_data.is_valid():
    #         flag = CtfLibrary.objects.get(id=self.validated_data['ctf'])
    #         print(flag)
    #         if flag == submit_flag:
    #             print('yes')

    def validate(self, attrs):
        if CtfSubmit.objects.filter(Q(user=attrs['user']) & Q(ctf=attrs['ctf']) & Q(submit_result=True)).exists():
            raise serializers.ValidationError('已提交过正确的flag')
        flag = attrs['ctf'].ctf_flag
        if flag == attrs['submit_flag']:
            attrs['submit_result'] = True
        else:
            attrs['submit_result'] = False
        return attrs

    class Meta:
        model = CtfSubmit
        fields = '__all__'


class CtfSubmitDetailSerializer(serializers.ModelSerializer):
    '''
    1.隐藏敏感flag字段 --> ok
    2.比赛结束不做限制 ok
    '''
    class Meta:
        model = CtfSubmit
        fields = ('id','user','competition','ctf','submit_time','submit_result')

