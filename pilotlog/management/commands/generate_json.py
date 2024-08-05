import json
import os
from django.core.management.base import BaseCommand
from django.utils.timezone import now
from pilotlog.utils.data_transformer import DataTransformer

class Command(BaseCommand):
    help = 'Generate JSON data from the current database state'

    def handle(self, *args, **options) -> None:
        json_file_path = os.path.join('Data/import-pilotlog_mcc.json')

        try:
            data_map, user_id_map = DataTransformer.fetch_data()
            current_timestamp = int(now().timestamp())

            # Transform data
            transformed_data = []
            transformed_data.extend(DataTransformer.transform_instance_data(
                data_map["Aircraft"], "Aircraft",
                user_id_map, current_timestamp
            ))
            transformed_data.extend(DataTransformer.transform_instance_data(
                data_map["FlightLog"], "FlightLog",
                user_id_map, current_timestamp, 
                related_fields=['aircraft', 'approaches', 'persons']
            ))
            transformed_data.extend(DataTransformer.transform_instance_data(
                data_map["Approach"], "Approach",
                user_id_map, current_timestamp
            ))
            transformed_data.extend(DataTransformer.transform_instance_data(
                data_map["Person"], "Person",
                user_id_map, current_timestamp,
                related_fields=['user']
            ))

            # Ensure the directory exists
            os.makedirs(os.path.dirname(json_file_path), exist_ok=True)

            # Write the transformed data to JSON file
            with open(json_file_path, 'w') as json_file:
                json.dump(transformed_data, json_file, indent=4)

            self.stdout.write(self.style.SUCCESS(f'Successfully generated JSON data at {json_file_path}'))
        
        except FileNotFoundError as e:
            self.stdout.write(self.style.ERROR(f'File not found: {e}'))
        except json.JSONDecodeError as e:
            self.stdout.write(self.style.ERROR(f'JSON decode error: {e}'))
        except IOError as e:
            self.stdout.write(self.style.ERROR(f'I/O error: {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Unexpected error: {e}'))
