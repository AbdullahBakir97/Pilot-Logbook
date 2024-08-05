import json
from pilotlog.models import Aircraft, FlightLog, Approach, Person
from django.contrib.auth.models import User
from .custom_field_renderer import CustomFieldRenderer

class PilotLogImporter:
    """
    Class to handle the import of pilot log data from a JSON file.
    """
    def __init__(self, json_file_path):
        """
        Initialize the importer with the given JSON file path.
        :param json_file_path: Path to the JSON file containing the data to import.
        """
        self.json_file_path = json_file_path

    def import_logs(self):
        """
        Import logs from the JSON file and populate the database.
        """
        try:
            with open(self.json_file_path, 'r') as file:
                data = json.load(file)

            self.import_aircraft(data)
            approach_dict, person_dict, aircraft_dict = self.create_dicts()
            self.import_approaches(data, approach_dict)
            self.import_persons(data, person_dict)
            self.import_flight_logs(data, approach_dict, person_dict, aircraft_dict)

            print("Data imported successfully.")
        except FileNotFoundError:
            print(f"Error: File not found - {self.json_file_path}")
        except json.JSONDecodeError:
            print("Error: Failed to decode JSON file.")
        except Exception as e:
            print(f"Error: Unexpected error occurred during import - {e}")

    def import_aircraft(self, data):
        """
        Import aircraft data from the JSON data.
        :param data: JSON data.
        """
        [Aircraft.objects.update_or_create(aircraft_id=item['meta']['aircraft_id'], defaults=item['meta'])
         for item in data if item['table'] == 'Aircraft']

    def create_dicts(self):
        """
        Create dictionaries to keep track of related objects.
        :return: Tuple containing dictionaries for approaches, persons, and aircraft.
        """
        approach_dict = {}
        person_dict = {}
        aircraft_dict = {aircraft.aircraft_id: aircraft for aircraft in Aircraft.objects.all()}
        return approach_dict, person_dict, aircraft_dict

    def import_approaches(self, data, approach_dict):
        """
        Import approaches data from the JSON data.
        :param data: JSON data.
        :param approach_dict: Dictionary to keep track of approaches.
        """
        [self.create_or_update_approach(item, approach_dict) for item in data if item['table'] == 'Approach']

    def create_or_update_approach(self, item, approach_dict):
        """
        Create or update an approach.
        :param item: JSON item containing approach data.
        :param approach_dict: Dictionary to keep track of approaches.
        """
        approach_data = item['meta']
        approach, _ = Approach.objects.update_or_create(id=approach_data['id'], defaults=approach_data)
        approach_dict[approach_data['id']] = approach

    def import_persons(self, data, person_dict):
        """
        Import persons data from the JSON data.
        :param data: JSON data.
        :param person_dict: Dictionary to keep track of persons.
        """
        [self.create_or_update_person(item, person_dict) for item in data if item['table'] == 'Person']

    def create_or_update_person(self, item, person_dict):
        """
        Create or update a person.
        :param item: JSON item containing person data.
        :param person_dict: Dictionary to keep track of persons.
        """
        person_data = item['meta']
        user_data = person_data.pop('user', None)
        user = User.objects.get_or_create(username=user_data['username'], defaults=user_data)[0] if user_data else None
        person, _ = Person.objects.update_or_create(user=user, defaults=person_data)
        person_dict[person_data.get('id')] = person

    def import_flight_logs(self, data, approach_dict, person_dict, aircraft_dict):
        """
        Import flight logs data from the JSON data.
        :param data: JSON data.
        :param approach_dict: Dictionary to keep track of approaches.
        :param person_dict: Dictionary to keep track of persons.
        :param aircraft_dict: Dictionary to keep track of aircraft.
        """
        for item in data:
            if item['table'] == 'FlightLog':
                flight_log_data = item['meta']
                aircraft_data = flight_log_data.pop('aircraft', {})

                # Get or create the aircraft instance
                aircraft = aircraft_dict.get(aircraft_data.get('aircraft_id'))
                if not aircraft:
                    aircraft, _ = Aircraft.objects.update_or_create(aircraft_id=aircraft_data['aircraft_id'], defaults=aircraft_data)
                    aircraft_dict[aircraft_data['aircraft_id']] = aircraft

                flight_log_data['aircraft'] = aircraft

                # Extract custom fields and render them
                custom_fields = flight_log_data.pop('custom_fields', {})
                renderer = CustomFieldRenderer(custom_fields, None)  # No instance needed for import
                flight_log_data['custom_fields'] = renderer.render_custom_fields()

                # Handle FlightLog creation
                flight_log, created = FlightLog.objects.update_or_create(id=flight_log_data.get('id'), defaults=flight_log_data)

                # Set related approaches
                approaches_ids = flight_log_data.pop('approaches', [])
                flight_log.approaches.set([approach_dict.get(app_id) for app_id in approaches_ids if approach_dict.get(app_id)])

                # Set related persons
                persons_ids = flight_log_data.pop('persons', [])
                flight_log.persons.set([person_dict.get(person_id) for person_id in persons_ids if person_dict.get(person_id)])
