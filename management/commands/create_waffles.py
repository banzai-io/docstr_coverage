from django.core.management.base import BaseCommand

from waffle.models import Switch


class Command(BaseCommand):
    def handle(self, *args, **options):
        switches = [
            'preview_file_functionality',
            'dialer_functionality',
            'auto_archive_functionality',
            'heap_analytics_production',
            'heap_analytics_staging',
            'email_automation_service',
        ]
        for switch in switches:
            if not Switch.objects.filter(name=switch).exists():
                Switch.objects.create(name=switch, active=False)
