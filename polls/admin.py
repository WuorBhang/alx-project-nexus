from django.contrib import admin
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count
from .models import Poll, Position, Candidate, Vote

class PositionInline(admin.TabularInline):
    model = Position
    extra = 1

class CandidateInline(admin.TabularInline):
    model = Candidate
    extra = 3
    fields = ('name', 'position', 'profile_picture', 'description')

def calculate_poll_results_action(modeladmin, request, queryset):
    """Admin action to manually calculate poll results"""
    for poll in queryset:
        if not poll.has_ended:
            messages.warning(request, f'Poll "{poll.title}" has not ended yet')
            continue
        
        try:
            results = {}
            
            # Calculate results for each position
            for position in poll.positions.all():
                candidates = position.candidates.annotate(
                    vote_count=Count('votes')
                ).order_by('-vote_count')
                
                winner = candidates.first()
                
                if winner and winner.vote_count > 0:
                    results[position.title] = {
                        'winner': winner.name,
                        'vote_count': winner.vote_count,
                    }
            
            # Update poll status to 'Ended'
            poll.status = 'Ended'
            poll.save()
            
            messages.success(
                request, 
                f'Results calculated for poll "{poll.title}". Status updated to Ended.'
            )
            
        except Exception as e:
            messages.error(
                request, 
                f'Error calculating results for poll "{poll.title}": {str(e)}'
            )

calculate_poll_results_action.short_description = "Calculate poll results"

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'duration', 'status')
    list_filter = ('start_time',)
    search_fields = ('title', 'description')
    inlines = [PositionInline]
    readonly_fields = ('status',)
    actions = [calculate_poll_results_action]
    
    def status(self, obj):
        return obj.status

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('title', 'poll')
    list_filter = ('poll',)
    search_fields = ('title', 'description')
    inlines = [CandidateInline]

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'poll')
    list_filter = ('position', 'poll')
    search_fields = ('name', 'description')
    
    def poll(self, obj):
        return obj.position.poll

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('voter', 'poll', 'position', 'candidate', 'timestamp')
    list_filter = ('poll', 'position', 'timestamp')
    search_fields = ('voter__username', 'candidate__name')
    readonly_fields = ('voter', 'poll', 'position', 'candidate', 'timestamp')