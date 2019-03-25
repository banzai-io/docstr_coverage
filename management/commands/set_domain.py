from django.conf import settings
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand
import os


class Command(BaseCommand):
    def handle(self, *args, **options):
        domain = os.getenv('DOMAIN')
        if not domain:
            raise Exception("Domain is not set")
        site = Site.objects.get(pk=settings.SITE_ID)
        site.domain = domain
        site.name = domain
        site.save()
