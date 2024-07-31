import json
import os
from uuid import uuid4
from django.core.management.base import BaseCommand
from pilotlog.models import Aircraft, FlightLog, Approach, Person
from pilotlog.serializers import AircraftSerializer, FlightLogSerializer, ApproachSerializer, PersonSerializer

class Command(BaseCommand):
    help = 'Generate JSON data from the current database state'

    def handle(self, *args, **options):
        json_file_path = os.path.join('Data/import-pilotlog_mcc.json')

        # Fetch data from the database
        aircraft_data = AircraftSerializer(Aircraft.objects.all(), many=True).data
        flight_logs_data = FlightLogSerializer(FlightLog.objects.all(), many=True).data
        approaches_data = ApproachSerializer(Approach.objects.all(), many=True).data
        persons_data = PersonSerializer(Person.objects.all(), many=True).data

        transformed_data = []

        # Transform Aircraft
        for aircraft in aircraft_data:
            transformed_data.append({
                "user_id": 125880,  # Example user_id
                "table": "Aircraft",
                "guid": str(uuid4()),  # Generate a unique identifier
                "meta": {
                    "aircraft_id": aircraft.get("aircraft_id"),
                    "equipment_type": aircraft.get("equipment_type"),
                    "type_code": aircraft.get("type_code"),
                    "year": aircraft.get("year"),
                    "make": aircraft.get("make"),
                    "model": aircraft.get("model"),
                    "category": aircraft.get("category"),
                    "aircraft_class": aircraft.get("aircraft_class"),
                    "gear_type": aircraft.get("gear_type"),
                    "engine_type": aircraft.get("engine_type"),
                    "complex": aircraft.get("complex"),
                    "high_performance": aircraft.get("high_performance"),
                    "pressurized": aircraft.get("pressurized"),
                    "taa": aircraft.get("taa")
                },
                "platform": 9,
                "_modified": 1616317613  # Example timestamp
            })

        # Transform Flight Logs
        for log in flight_logs_data:
            transformed_data.append({
                "user_id": 125880,  # Example user_id
                "table": "FlightLog",
                "guid": str(uuid4()),  # Generate a unique identifier
                "meta": {
                    "id": log.get("id"),
                    "aircraft": log.get("aircraft"),
                    "approaches": log.get("approaches"),
                    "persons": log.get("persons"),
                    "date": log.get("date"),
                    "from_airport": log.get("from_airport"),
                    "to_airport": log.get("to_airport"),
                    "route": log.get("route"),
                    "time_out": log.get("time_out"),
                    "time_off": log.get("time_off"),
                    "time_on": log.get("time_on"),
                    "time_in": log.get("time_in"),
                    "on_duty": log.get("on_duty"),
                    "off_duty": log.get("off_duty"),
                    "total_time": log.get("total_time"),
                    "pic": log.get("pic"),
                    "sic": log.get("sic"),
                    "night": log.get("night"),
                    "solo": log.get("solo"),
                    "cross_country": log.get("cross_country"),
                    "nvg": log.get("nvg"),
                    "nvg_ops": log.get("nvg_ops"),
                    "distance": log.get("distance"),
                    "day_takeoffs": log.get("day_takeoffs"),
                    "day_landings_full_stop": log.get("day_landings_full_stop"),
                    "night_takeoffs": log.get("night_takeoffs"),
                    "night_landings_full_stop": log.get("night_landings_full_stop"),
                    "all_landings": log.get("all_landings"),
                    "actual_instrument": log.get("actual_instrument"),
                    "simulated_instrument": log.get("simulated_instrument"),
                    "hobbs_start": log.get("hobbs_start"),
                    "hobbs_end": log.get("hobbs_end"),
                    "tach_start": log.get("tach_start"),
                    "tach_end": log.get("tach_end"),
                    "holds": log.get("holds"),
                    "dual_given": log.get("dual_given"),
                    "dual_received": log.get("dual_received"),
                    "simulated_flight": log.get("simulated_flight"),
                    "ground_training": log.get("ground_training"),
                    "instructor_name": log.get("instructor_name"),
                    "instructor_comments": log.get("instructor_comments"),
                    "flight_review": log.get("flight_review"),
                    "checkride": log.get("checkride"),
                    "ipc": log.get("ipc"),
                    "nvg_proficiency": log.get("nvg_proficiency"),
                    "faa_6158": log.get("faa_6158"),
                    "remarks": log.get("remarks"),
                    "custom_fields": log.get("custom_fields")
                }
            })

        # Transform Approaches
        for approach in approaches_data:
            transformed_data.append({
                "user_id": 125880,  # Example user_id
                "table": "Approach",
                "guid": str(uuid4()),  # Generate a unique identifier
                "meta": {
                    "id": approach.get("id"),
                    "type": approach.get("type"),
                    "runway": approach.get("runway"),
                    "airport": approach.get("airport"),
                    "comments": approach.get("comments")
                }
            })

        # Transform Persons
        for person in persons_data:
            transformed_data.append({
                "user_id": 125880,  # Example user_id
                "table": "Person",
                "guid": str(uuid4()),  # Generate a unique identifier
                "meta": {
                    "user_id": person.get("user_id"),
                    "role": person.get("role")
                }
            })

        # Ensure the directory exists
        os.makedirs(os.path.dirname(json_file_path), exist_ok=True)

        # Write the transformed data to JSON file
        with open(json_file_path, 'w') as json_file:
            json.dump(transformed_data, json_file, indent=4)

        self.stdout.write(self.style.SUCCESS(f'Successfully generated JSON data at {json_file_path}'))
