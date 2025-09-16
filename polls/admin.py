from django.contrib import admin
from .models import Poll, Position, Candidate, Vote

class PositionInline(admin.TabularInline):
    model = Position
    extra = 1

class CandidateInline(admin.TabularInline):
    model = Candidate
    extra = 3
    fields = ('name', 'position', 'profile_picture', 'description')

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'duration', 'status')
    list_filter = ('start_time',)
    search_fields = ('title', 'description')
    inlines = [PositionInline]
    readonly_fields = ('status',)
    
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