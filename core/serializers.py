from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import *

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'email', 'groups']


class SurveySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Poll
        fields = ['id', 'user','survey_title', 'choices', 'survey_type', 'date_created', 'slug']


class ChoiceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'user', 'survey_title',  'first_choice', 'second_choice', 'third_choice', 'fourth_choice', 'yes_or_no_choice']


class VoteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Vote
        fields = ['id', 'user','survey_title', 'choices', 'timestamp']

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password']