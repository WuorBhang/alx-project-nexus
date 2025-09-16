from django.urls import path
from .views import PollListView, PollDetailView, VoteCreateView, PollResultsView

urlpatterns = [
    path('polls/', PollListView.as_view(), name='poll-list'),
    path('polls/<int:pk>/', PollDetailView.as_view(), name='poll-detail'),
    path('polls/<int:pk>/vote/', VoteCreateView.as_view(), name='poll-vote'),
    path('polls/<int:pk>/results/', PollResultsView.as_view(), name='poll-results'),
]