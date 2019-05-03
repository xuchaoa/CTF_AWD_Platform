from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .serializers import CompetitionSerializer
from .models import CompetitionProfile
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

class CompetitionViewSet(viewsets.ModelViewSet):
    queryset = CompetitionProfile.objects.all()
    serializer_class = CompetitionSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
