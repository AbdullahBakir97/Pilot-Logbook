import json
from django.core.management.base import BaseCommand
from django.http import HttpResponse
from pilotlog.utils.exporter import PilotLogExporter
from django.core.files.storage import default_storage

class Command(BaseCommand):
    help = 'Export pilot logs to a CSV file.'

    def add_arguments(self, parser):
        parser.add_argument('json_file_path', type=str, help='Path to the JSON file for configuration.')
        parser.add_argument('csv_file_path', type=str, help='Path to the output CSV file.')

    def handle(self, *args, **kwargs):
        json_file_path = kwargs['json_file_path']
        csv_file_path = kwargs['csv_file_path']
        try:
            exporter = PilotLogExporter(json_file_path, csv_file_path)
            exporter.export_to_csv()
            self.stdout.write(self.style.SUCCESS('Pilot logs exported successfully.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error exporting logs: {e}'))

