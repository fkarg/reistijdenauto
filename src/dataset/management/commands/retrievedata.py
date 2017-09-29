from django.core.management.base import BaseCommand

from dataset.models import WegStuk
from dataset.update import download_and_update


class Command(BaseCommand):
    help = 'Retrieve a new reistijden GeoJSON and store in the database.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Downloading new data set'))
        download_and_update()
        self.stdout.write(self.style.SUCCESS(
            'Stored {} stretches of road.'.format(WegStuk.objects.count())
        ))
