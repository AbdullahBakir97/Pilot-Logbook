import json
from .models import Aircraft, FlightLog, Approach, Person
from django.contrib.auth.models import User

class PilotLogImporter:
    def __init__(self, json_file_path):
        self.json_file_path = json_file_path

    def import_logs(self):
        with open(self.json_file_path, 'r') as file:
            data = json.load(file)

        # Import Aircraft
        for item in data:
            if item['table'] == 'Aircraft':
                aircraft_data = item['meta']
                Aircraft.objects.update_or_create(aircraft_id=aircraft_data['aircraft_id'], defaults=aircraft_data)

        # Create dictionaries to keep track of related objects
        approach_dict = {}
        person_dict = {}
        aircraft_dict = {aircraft.aircraft_id: aircraft for aircraft in Aircraft.objects.all()}

        # Import Approaches
        for item in data:
            if item['table'] == 'Approach':
                approach_data = item['meta']
                approach, _ = Approach.objects.update_or_create(id=approach_data['id'], defaults=approach_data)
                approach_dict[approach_data['id']] = approach

        # Import Persons
        for item in data:
            if item['table'] == 'Person':
                person_data = item['meta']
                user, _ = User.objects.get_or_create(username=person_data['user']['username'], defaults=person_data['user'])
                person_data['user'] = user
                person, _ = Person.objects.update_or_create(user=user, defaults=person_data)
                person_dict[person_data['user']['id']] = person

        # Import Flight Logs
        for item in data:
            if item['table'] == 'FlightLog':
                flight_log_data = item['meta']
                aircraft_data = flight_log_data.pop('aircraft')

                # Get or create the aircraft instance
                aircraft = aircraft_dict.get(aircraft_data['aircraft_id'])
                if not aircraft:
                    aircraft, _ = Aircraft.objects.update_or_create(aircraft_id=aircraft_data['aircraft_id'], defaults=aircraft_data)
                    aircraft_dict[aircraft_data['aircraft_id']] = aircraft

                # Set the aircraft instance to the flight log data
                flight_log_data['aircraft'] = aircraft

                # Pop approaches and persons from the flight log data to handle them separately
                approaches_ids = flight_log_data.pop('approaches', [])
                persons_ids = flight_log_data.pop('persons', [])

                # Handle FlightLog creation
                flight_log, created = FlightLog.objects.update_or_create(id=flight_log_data['id'], defaults=flight_log_data)

                # Set related approaches
                flight_log.approaches.set([approach_dict[app_id] for app_id in approaches_ids])

                # Set related persons
                flight_log.persons.set([person_dict[person_id] for person_id in persons_ids])

