from django.core.management.base import BaseCommand
from django.utils import timezone
from simplechatbot.utils import calculate_session_analytics

class Command(BaseCommand):
    help = 'Update daily chat analytics'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--date',
            type=str,
            help='Calculate analytics for specific date (YYYY-MM-DD). Defaults to today.',
        )
    
    def handle(self, *args, **options):
        if options['date']:
            try:
                target_date = timezone.datetime.strptime(options['date'], '%Y-%m-%d').date()
                self.stdout.write(f'Calculating analytics for {target_date}...')
            except ValueError:
                self.stdout.write(
                    self.style.ERROR('Invalid date format. Use YYYY-MM-DD.')
                )
                return
        else:
            target_date = timezone.now().date()
            self.stdout.write(f'Calculating analytics for today ({target_date})...')
        
        try:
            analytics = calculate_session_analytics()
            if analytics:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Analytics updated successfully:\n'
                        f'Sessions: {analytics.total_sessions}\n'
                        f'Messages: {analytics.total_messages}\n'
                        f'Avg Session Length: {analytics.avg_session_length} min\n'
                        f'Leads: {analytics.leads_generated}\n'
                        f'Conversion Rate: {analytics.conversion_rate}%'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING('No sessions found for the specified date.')
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error updating analytics: {str(e)}')
            )