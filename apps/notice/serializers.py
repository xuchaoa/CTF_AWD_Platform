from rest_framework import serializers
from .models import NoticeProfile


class NoticeSerializer(serializers.ModelSerializer):

    class Meta:
        model = NoticeProfile
        fields = "__all__"