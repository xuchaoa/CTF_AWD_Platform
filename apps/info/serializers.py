from rest_framework import serializers
from .models import CtfCompetitionTable,CtfSubmit
from ctf.serializers import CtfSerializer
from teams.models import TeamProfile
from info.models import CtfSubmit,CtfCompetitionTable
from ctf.models import CtfLibrary
from django.forms.models import model_to_dict
from django.db.models import Q
from .models import Illegality, UserCompetitionInfo, TeamCompetitionInfo,CompetitionChoiceSubmit,UserChoiceInfo
from choice.serializers import ChoiceSerializer
from hashlib import md5
from rest_framework.exceptions import APIException
from django.utils.translation import ugettext_lazy as _
from django.http import JsonResponse
from utils.CompetitionLimited import CompetitionIsStarted
from competition.models import CompetitionProfile
from utils.IllegalityLimited import limited

class TeamCompetitionInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = TeamCompetitionInfo
        fields = "__all__"


class UserCompetitionInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserCompetitionInfo
        fields = "__all__"


class UserCompetitionInfoUpdateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    wp = serializers.FileField(required=True,error_messages={
        'blank':'未选中文件',
        'required':'未选中文件'
    })

    class Meta:
        model = UserCompetitionInfo
        fields = ('user','wp')

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
        team = TeamProfile.objects.get(Q(team_captain=self.user) | Q(team_member1=self.user) | Q(team_member2=self.user) | Q(team_member3=self.user))
        self.competition = team.competition


        # self.ctf_id = serializer_field.context['request'].POST['ctf']
        # # team = TeamProfile.objects.filter()
        # self.ctf_competition = CtfCompetitionTable.objects.filter(ctf=self.ctf_id )
        # # self.ctf = model_to_dict(self.ctf)
        # # self.com = CtfCompetitionTable.objects.filter(ctf=self.ctf)
        # self.ctf = self.ctf_competition.model.ctf
        # self.com = self.ctf_competition.model.competition

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
                                        },write_only=True)
    submit_time = serializers.DateTimeField(read_only=True,format='%Y-%m-%d %H:%M:%S')
    submit_result = serializers.BooleanField(default=False,read_only=True)


    def validate(self, attrs):
        CompetitionIsStarted(attrs['competition'])
        limited(attrs['user'])
        if CtfSubmit.objects.filter(Q(user=attrs['user']) & Q(ctf=attrs['ctf']) & Q(submit_result=True)).exists():
            raise serializers.ValidationError({'401':'已提交过正确的flag'})
        flag = attrs['ctf'].ctf_flag
        jwt = self._context['request'].auth
        ## 在调试界面会出现NoneType情况,直接用postman调试
        jwt = jwt.decode()
        _ = jwt.split(".")[2]
        flag = md5((flag + _).encode()).hexdigest()
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

class CompetitionChoiceDetailSerializer(serializers.ModelSerializer):
    # is_start = serializers.IntegerField
    choice = ChoiceSerializer()

    class Meta:
        model = CompetitionChoiceSubmit
        fields = ('id','choice','score','submit_result','user')

class CompetitionChoiceUpdateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    def validate(self, attrs):
        CompetitionIsStarted(self.instance.competition)
        return attrs

    class Meta:
        model = CompetitionChoiceSubmit
        fields = ('id','submit_result','user')


class CurrentTeamDefault(serializers.CurrentUserDefault):
    '''
    决定了每个用户只能在一个队伍中
    '''
    def set_context(self, serializer_field):
        self.user = serializer_field.context['request'].user
        self.team = TeamProfile.objects.get(Q(team_captain=self.user) | Q(team_member1=self.user) | Q(team_member2=self.user) | Q(team_member3=self.user))


    def __call__(self):
        return self.team



class UserChoiceInfoAddSerializer(serializers.ModelSerializer):
    '''
    生成题库时使用该serializer
    '''
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    team = serializers.HiddenField(
        default=CurrentTeamDefault()
    )
    competition = serializers.HiddenField(
        default=CurrentCompetitionDefault()
    )

    submit_status = serializers.NullBooleanField()
    score = serializers.IntegerField(read_only=True)

    def validate_submit_status(self,submit_status):

        if submit_status == 0:
            pass
        elif submit_status == None:
            raise serializers.ValidationError('不允许重置')
        if submit_status == 1:
            raise serializers.ValidationError('不允许提交')


    def validate(self, attrs):
        CompetitionIsStarted(attrs['competition'])
        attrs['submit_status'] = 0
        return attrs

    class Meta:
        model = UserChoiceInfo
        fields = "__all__"



class HaveSubmitedFlag(APIException):
    status_code = 461
    default_detail = _('Incorrect authentication credentials.')
    default_code = 'authentication_failed'

class UserChoiceInfoUpdateSerializer(serializers.ModelSerializer):
    '''
    提交选择题时使用
    '''
    submit_status = serializers.NullBooleanField()

    def validate_submit_status(self, submit_status):
        print(submit_status)
        current_submit_status = UserChoiceInfo.objects.filter(user=self.context['request'].user)
        current_submit_status = current_submit_status[0].submit_status
        if current_submit_status == 0:
            pass
        elif current_submit_status == None:
            raise serializers.ValidationError('未获取题目，不能提交')
        if current_submit_status == 1:
            raise serializers.ValidationError(detail='已经提交题目，不必重复提交',code=461)
            # raise HaveSubmitedFlag()
    def validate(self, attrs):
        CompetitionIsStarted(self.instance.competition)
        attrs['submit_status'] = 1
        return attrs

    class Meta:
        model = UserChoiceInfo
        fields = ('submit_status',)


class UserChoiceInfoDetailSerializer(serializers.ModelSerializer):
    '''
    获取详情时使用
    '''
    class Meta:
        model = UserChoiceInfo
        fields = "__all__"