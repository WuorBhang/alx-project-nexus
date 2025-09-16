from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import Count
from .models import Poll, Position, Candidate, Vote
from .serializers import (
    PollListSerializer, PollDetailSerializer, VoteSerializer, 
    PollResultSerializer
)
from drf_spectacular.utils import extend_schema, OpenApiParameter
from django.utils import timezone

class IsVoter(permissions.BasePermission):
    """
    Custom permission to only allow voters to vote
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_voter()

class PollListView(generics.ListAPIView):
    """
    List all polls
    """
    queryset = Poll.objects.all().order_by('-start_time')
    serializer_class = PollListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @extend_schema(
        summary="List all polls",
        description="Returns a list of all polls with their basic information"
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class PollDetailView(generics.RetrieveAPIView):
    """
    Retrieve a specific poll with its positions and candidates
    """
    queryset = Poll.objects.all()
    serializer_class = PollDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @extend_schema(
        summary="Get poll details",
        description="Returns detailed information about a specific poll, including positions and candidates"
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class VoteCreateView(generics.CreateAPIView):
    """
    Cast a vote for a candidate in a specific position and poll
    """
    serializer_class = VoteSerializer
    permission_classes = [IsVoter]
    
    @extend_schema(
        summary="Cast a vote",
        description="Cast a vote for a candidate in a specific position and poll",
        parameters=[
            OpenApiParameter(name="poll_id", location=OpenApiParameter.PATH, required=True, type=int)
        ]
    )
    def post(self, request, *args, **kwargs):
        poll_id = self.kwargs.get('pk')
        poll = get_object_or_404(Poll, pk=poll_id)
        
        # Check if poll is active
        if not poll.is_active:
            return Response(
                {"error": "This poll is not currently active"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Add poll to request data
        data = request.data.copy()
        data['poll'] = poll_id
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class PollResultsView(generics.RetrieveAPIView):
    """
    Get the results of a poll
    """
    queryset = Poll.objects.all()
    serializer_class = PollResultSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @extend_schema(
        summary="Get poll results",
        description="Returns the results of a poll, including vote counts for each candidate",
        parameters=[
            OpenApiParameter(name="poll_id", location=OpenApiParameter.PATH, required=True, type=int)
        ]
    )
    def get(self, request, *args, **kwargs):
        poll = self.get_object()
        
        # If poll hasn't ended, only show results if user is admin
        if not poll.has_ended and not request.user.is_admin():
            return Response(
                {"error": "Results are only available after the poll has ended"}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().get(request, *args, **kwargs)