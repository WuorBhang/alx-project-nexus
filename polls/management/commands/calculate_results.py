from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import Count
from polls.models import Poll, Position, Candidate, Vote

class Command(BaseCommand):
    help = 'Calculate results for ended polls'

    def add_arguments(self, parser):
        parser.add_argument(
            '--poll-id',
            type=int,
            help='Calculate results for a specific poll ID'
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Calculate results for all ended polls'
        )

    def handle(self, *args, **options):
        if options['poll_id']:
            self.calculate_poll_results(options['poll_id'])
        elif options['all']:
            self.calculate_all_ended_polls()
        else:
            self.stdout.write(
                self.style.WARNING('Please specify --poll-id <id> or --all')
            )

    def calculate_poll_results(self, poll_id):
        """Calculate results for a specific poll"""
        try:
            poll = Poll.objects.get(pk=poll_id)
            
            if not poll.has_ended:
                self.stdout.write(
                    self.style.WARNING(f'Poll "{poll.title}" has not ended yet')
                )
                return
            
            self.stdout.write(f'Calculating results for poll: {poll.title}')
            
            results = {}
            
            # Calculate results for each position
            for position in poll.positions.all():
                # Get candidates with vote counts
                candidates = position.candidates.annotate(
                    vote_count=Count('votes')
                ).order_by('-vote_count')
                
                # Determine winner
                winner = candidates.first()
                
                if winner and winner.vote_count > 0:
                    results[position.title] = {
                        'winner': winner.name,
                        'vote_count': winner.vote_count,
                        'all_candidates': [
                            {'name': c.name, 'votes': c.vote_count} 
                            for c in candidates
                        ]
                    }
                    
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'  {position.title}: {winner.name} wins with {winner.vote_count} votes'
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'  {position.title}: No votes cast')
                    )
            
            self.stdout.write(
                self.style.SUCCESS(f'Results calculated for poll: {poll.title}')
            )
            
        except Poll.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'Poll with ID {poll_id} does not exist')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error calculating results: {str(e)}')
            )

    def calculate_all_ended_polls(self):
        """Calculate results for all ended polls"""
        ended_polls = Poll.objects.filter(
            end_time__lt=timezone.now()
        ).exclude(status='Ended')
        
        if not ended_polls.exists():
            self.stdout.write(
                self.style.WARNING('No ended polls found')
            )
            return
        
        self.stdout.write(f'Found {ended_polls.count()} ended polls')
        
        for poll in ended_polls:
            self.calculate_poll_results(poll.id)
            # Update poll status to 'Ended'
            poll.status = 'Ended'
            poll.save()
            self.stdout.write(f'Updated poll "{poll.title}" status to Ended')
        
        self.stdout.write(
            self.style.SUCCESS('All ended polls processed')
        )
