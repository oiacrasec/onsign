from django.core.management import BaseCommand
from django.db.models import Count
from django.conf import settings
from django.utils import timezone
import json
import csv
import os

from weather.models import Tracker


class Command(BaseCommand):
    """
    Usage:
    JSON > manage.py export_data
    CSV > manage.py export_data csv

    Help > manage.py export_data --help
    """

    def add_arguments(self, parser):
        parser.add_argument('type', type=str, help='Options: json / csv, default json', nargs='?', default='json')

    def handle(self, *args, **kwargs):
        path = '{path}/generated_{now}.{extension}'
        config = {
            'path': self.get_folder(),
            'now': timezone.now().strftime('%Y_%m_%d_%H_%M_%S')
        }
        option = kwargs['type'].lower()
        if option == 'json':
            self.file_json(path, config)
        elif option == 'csv':
            self.file_csv(path, config)
        else:
            raise NotImplementedError

    def file_json(self, path, config):
        config.update(extension='json')
        with open(path.format(**config), "w") as out:
            out.write(json.dumps(list(self.get_queryset()), indent=4, sort_keys=True, default=str))

    def file_csv(self, path, config):
        config.update(extension='csv')
        with open(path.format(**config), "w", newline='') as out:
            out_writer = csv.writer(out, delimiter=';')
            out_writer.writerow(['date', 'ip_address', 'usage'])
            for obj in self.get_queryset():
                out_writer.writerow([obj['date'].strftime('%Y-%m-%d'), obj['ip_address'], obj['usage']])

    @staticmethod
    def get_queryset():
        return Tracker.objects.filter(consulted=True).extra({
            'date': 'date(created_at)'
        }).values('ip_address', 'date').annotate(usage=Count('id'))

    @staticmethod
    def get_folder():
        folder_path = os.path.join(settings.MEDIA_ROOT, 'exported')
        if not os.path.exists(folder_path):
            os.makedirs(folder_path, exist_ok=True)
        return folder_path
