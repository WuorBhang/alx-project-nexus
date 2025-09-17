from rest_framework import serializers
from .models import Poll, Position, Candidate, Vote
from django.utils import timezone
from django.db.models import Count

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['id', 'name', 'profile_picture', 'description']

class PositionSerializer(serializers.ModelSerializer):
    candidates = CandidateSerializer(many=True, read_only=True)
    
    class Meta:
        model = Position
        fields = ['id', 'title', 'description', 'candidates']

class PollListSerializer(serializers.ModelSerializer):
    status = serializers.CharField(read_only=True)
    
    class Meta:
        model = Poll
        fields = ['id', 'title', 'description', 'start_time', 'duration', 'status']

class PollDetailSerializer(serializers.ModelSerializer):
    positions = PositionSerializer(many=True, read_only=True)
    status = serializers.CharField(read_only=True)
    end_time = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = Poll
        fields = ['id', 'title', 'description', 'start_time', 'duration', 'end_time', 'status', 'positions']

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id', 'position', 'candidate']
        read_only_fields = ['voter']
    
    def validate(self, attrs):
        position = attrs['position']
        candidate = attrs['candidate']
        poll = position.poll
        
        # Check if poll is active
        if not poll.is_active:
            raise serializers.ValidationError("This poll is not currently active.")
        
        # Check if candidate belongs to position
        if candidate.position != position:
            raise serializers.ValidationError("This candidate does not belong to the specified position.")
        
        # Check if user has already voted for this position
        voter = self.context['request'].user
        if Vote.objects.filter(voter=voter, position=position).exists():
            raise serializers.ValidationError("You have already voted for this position.")
        
        return attrs
    
    def create(self, validated_data):
        validated_data['voter'] = self.context['request'].user
        return super().create(validated_data)

class CandidateResultSerializer(serializers.ModelSerializer):
    vote_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Candidate
        fields = ['id', 'name', 'vote_count']

class PositionResultSerializer(serializers.ModelSerializer):
    candidates = serializers.SerializerMethodField()
    winner = serializers.SerializerMethodField()
    
    class Meta:
        model = Position
        fields = ['id', 'title', 'candidates', 'winner']
    
    def get_candidates(self, obj):
        candidates = obj.candidates.annotate(vote_count=Count('votes')).order_by('-vote_count')
        return CandidateResultSerializer(candidates, many=True).data
    
    def get_winner(self, obj):
        poll = obj.poll
        if not poll.has_ended:
            return None
        
        winner = obj.candidates.annotate(vote_count=Count('votes')).order_by('-vote_count').first()
        if winner:
            return CandidateResultSerializer(winner).data
        return None

class PollResultSerializer(serializers.ModelSerializer):
    positions = PositionResultSerializer(many=True, read_only=True)
    status = serializers.CharField(read_only=True)
    
    class Meta:
        model = Poll
        fields = ['id', 'title', 'status', 'positions']