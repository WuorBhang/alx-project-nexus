from celery import shared_task
from django.utils import timezone
from django.db.models import Count
from django.core.mail import send_mail
from django.conf import settings
from .models import Poll, Position, Candidate, Vote

@shared_task
def calculate_poll_results(poll_id):
    """
    Calculate the final results for a poll and send notifications
    """
    try:
        poll = Poll.objects.get(pk=poll_id)
        
        # Check if the poll has ended
        if not poll.has_ended:
            return "Poll has not ended yet"
        
        results = {}
        
        # Calculate results for each position
        for position in poll.positions.all():
            # Get candidates with vote counts
            candidates = position.candidates.annotate(vote_count=Count('votes')).order_by('-vote_count')
            
            # Determine winner
            winner = candidates.first()
            
            if winner:
                results[position.title] = {
                    'winner': winner.name,
                    'vote_count': winner.vote_count,
                    'all_candidates': [
                        {'name': c.name, 'votes': c.vote_count} 
                        for c in candidates
                    ]
                }
        
        # Send notifications to all voters
        send_results_notification(poll, results)
        
        return f"Results calculated for poll: {poll.title}"
    
    except Poll.DoesNotExist:
        return f"Poll with ID {poll_id} does not exist"
    except Exception as e:
        return f"Error calculating results: {str(e)}"

def send_results_notification(poll, results):
    """
    Send notification to all voters about the poll results
    """
    # In a real application, you would send emails or push notifications
    # For this example, we'll just print the notification
    
    # Get all voters who participated in this poll
    voters = set(Vote.objects.filter(poll=poll).values_list('voter__email', flat=True))
    
    # Prepare the notification message
    subject = f"Results for {poll.title}"
    message = f"The results for {poll.title} are in!\n\n"
    
    for position, result in results.items():
        message += f"\n{position}:\n"
        message += f"Winner: {result['winner']} with {result['vote_count']} votes\n"
        message += "All candidates:\n"
        for candidate in result['all_candidates']:
            message += f"- {candidate['name']}: {candidate['votes']} votes\n"
    
    # In a real application, you would send actual emails
    # For now, we'll just print the message
    print(f"Subject: {subject}")
    print(f"To: {', '.join(voters)}")
    print(f"Message: {message}")
    
    # Uncomment this to send actual emails in production
    # for voter_email in voters:
    #     send_mail(
    #         subject,
    #         message,
    #         settings.DEFAULT_FROM_EMAIL,
    #         [voter_email],
    #         fail_silently=False,
    #     )