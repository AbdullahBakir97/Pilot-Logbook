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

    def handle(self, *args, **options):
        json_file_path = os.path.join('Data/import-pilotlog_mcc.json')

        try:
            # Fetch user data and create a mapping for user IDs
            user_data = User.objects.all()
            user_id_map = {user.id: user.id for user in user_data}

            # Fetch data from the database
            aircraft_data = AircraftSerializer(Aircraft.objects.all(), many=True).data
            flight_logs_data = FlightLogSerializer(FlightLog.objects.all(), many=True).data
            approaches_data = ApproachSerializer(Approach.objects.all(), many=True).data
            persons_data = PersonSerializer(Person.objects.all(), many=True).data

            transformed_data = []
            current_timestamp = int(now().timestamp())

            def transform_instance_data(instance_data, table_name, related_fields=None):
                """Helper function to transform instance data."""
                if related_fields is None:
                    related_fields = []
                for instance in instance_data:
                    user_id = instance.get("user_id") or (instance.get("user") and instance["user"].get("id"))
                    transformed_instance = {
                        "user_id": user_id_map.get(user_id),
                        "table": table_name,
                        "guid": str(uuid4()),
                        "meta": {k: v for k, v in instance.items() if k not in related_fields},
                        "_modified": current_timestamp
                    }
                    transformed_data.append(transformed_instance)

            # Transform data for each model
            transform_instance_data(aircraft_data, "Aircraft")
            transform_instance_data(flight_logs_data, "FlightLog", related_fields=['aircraft', 'approaches', 'persons'])
            transform_instance_data(approaches_data, "Approach")
            transform_instance_data(persons_data, "Person", related_fields=['user'])

            # Ensure the directory exists
            os.makedirs(os.path.dirname(json_file_path), exist_ok=True)

            # Write the transformed data to JSON file
            with open(json_file_path, 'w') as json_file:
                json.dump(transformed_data, json_file, indent=4)

            self.stdout.write(self.style.SUCCESS(f'Successfully generated JSON data at {json_file_path}'))
        
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error generating JSON data: {e}'))
