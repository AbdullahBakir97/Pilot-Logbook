import json
from django.core.management.base import BaseCommand
from pilotlog.models import Aircraft, FlightLog, Approach, Person
from pilotlog.utils.importer import PilotLogImporter

class Command(BaseCommand):
    help = 'Import pilot logs from a JSON file.'

    def add_arguments(self, parser):
        parser.add_argument('json_file_path', type=str, help='Path to the JSON file to be imported.')

    def handle(self, *args, **kwargs):
        json_file_path = kwargs['json_file_path']
        try:
            importer = PilotLogImporter(json_file_path)
            importer.import_logs()
            self.stdout.write(self.style.SUCCESS('Pilot logs imported successfully.'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('File not found. Please ensure the file path is correct.'))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR('Error decoding JSON file. Please check the file format.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing logs: {e}'))
