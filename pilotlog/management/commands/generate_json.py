import json
import os
from uuid import uuid4
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from pilotlog.models import Aircraft, FlightLog, Approach, Person
from pilotlog.serializers import AircraftSerializer, FlightLogSerializer, ApproachSerializer, PersonSerializer

class Command(BaseCommand):
    help = 'Generate JSON data from the current database state'

    def handle(self, *args, **options) -> None:
        json_file_path = os.path.join('Data/import-pilotlog_mcc.json')

        try:
            # Fetch and map user data
            user_data = User.objects.all()
            user_id_map = {user.id: user.id for user in user_data}

            # Fetch data from the database
            data_map = {
                "Aircraft": AircraftSerializer(Aircraft.objects.all(), many=True).data,
                "FlightLog": FlightLogSerializer(FlightLog.objects.all(), many=True).data,
                "Approach": ApproachSerializer(Approach.objects.all(), many=True).data,
                "Person": PersonSerializer(Person.objects.all(), many=True).data,
            }

            transformed_data = []
            current_timestamp = int(now().timestamp())

            def transform_instance_data(instance_data: list, table_name: str, related_fields: list = None) -> None:
                """
                Helper function to transform instance data.
                :param instance_data: List of serialized data instances.
                :param table_name: Name of the table corresponding to the data.
                :param related_fields: List of related fields to exclude from meta.
                """
                if related_fields is None:
                    related_fields = []
                for instance in instance_data:
                    user_id = instance.get("user_id") or (instance.get("user") and instance["user"].get("id"))
                    transformed_instance = {
                        "user_id": user_id_map.get(user_id),
                        "table": table_name,
                        "guid": str(uuid4()),
                        "meta": {k: v for k, v in instance.items() if k not in related_fields},
                        "_modified": current_timestamp,
                    }
                    transformed_data.append(transformed_instance)

            # Transform data for each model
            transform_instance_data(data_map["Aircraft"], "Aircraft")
            transform_instance_data(data_map["FlightLog"], "FlightLog", related_fields=['aircraft', 'approaches', 'persons'])
            transform_instance_data(data_map["Approach"], "Approach")
            transform_instance_data(data_map["Person"], "Person", related_fields=['user'])

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