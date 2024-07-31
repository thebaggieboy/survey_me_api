from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import *
from .models import *
from django.views.generic import CreateView, FormView, DeleteView, View
# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class SurveyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Poll.objects.all()
    serializer_class = SurveySerializer
    #permission_classes = [permissions.IsAuthenticated]


class VoteViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    #permission_classes = [permissions.IsAuthenticated]


class ChoiceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [permissions.IsAuthenticated]



class CreateSurveyView(CreateView):
    model = Poll
    template_name = 'create_survey.html'

    


class HomeView(View):

    def get(self, request):
        polls = Poll.objects.all()
        return render(
            request,
            template_name="survey_list.html",
            context={
                "polls": polls,
            }
        )


class PollView(View):

    def get(self, request, poll_slug):
        poll = Poll.objects.get(slug=poll_slug)
        return render(
            request,
            template_name="poll.html",
            context={
                "poll": poll,
            }
        )

    def post(self, request, poll_slug):
            requestData = request.POST

            choice_id = requestData.get('choice_id')

            poll = Poll.objects.get(slug=poll_slug)
            choice = Choice.objects.get(id=choice_id)
            Vote.objects.create(
                poll=poll,
                choice=choice,
            )

            poll_results = []
            for choice in poll.choices.all():
                voteCount = Vote.objects.filter(poll=poll, choice=choice).count()
                poll_results.append([choice.name, voteCount])

            return render(
                request,
                template_name="poll.html",
                context={
                    "poll": poll,
                    "success_message": "Voted Successfully",
                    "poll_results":poll_results
                }
            )