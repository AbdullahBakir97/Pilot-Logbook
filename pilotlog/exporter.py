import json
import csv
from django.apps import apps
from django.db.models import Model
from .models import Aircraft, FlightLog, Approach, Person
from .custom_field_renderer import CustomFieldRenderer

def get_model_field_names(model: Model):
    return [field.name for field in model._meta.get_fields() if not field.is_relation]

class PilotLogExporter:
    def __init__(self, json_file_path, csv_file_path):
        self.json_file_path = json_file_path
        self.csv_file_path = csv_file_path

    def export_to_csv(self):
        with open(self.json_file_path, 'r') as file:
            data = json.load(file)

        aircraft_fieldnames = get_model_field_names(Aircraft)
        flight_fieldnames = get_model_field_names(FlightLog)

        with open(self.csv_file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)

            # Export Aircraft data
            writer.writerow(['Aircraft Table'])
            writer.writerow(aircraft_fieldnames)
            for aircraft in Aircraft.objects.all():
                row = [getattr(aircraft, field, '') for field in aircraft_fieldnames]
                writer.writerow(row)

            # Export Flight Log data
            writer.writerow([])
            writer.writerow(['Flights Table'])
            # Determine the custom field names from the first flight log entry
            custom_fieldnames = self.get_custom_fieldnames(data)
            writer.writerow(flight_fieldnames + custom_fieldnames + ['approaches', 'persons'])

            for flight in FlightLog.objects.all():
                custom_fields = self.render_custom_fields(flight.custom_fields, flight)

                # Add fields to row
                row = [getattr(flight, field, '') for field in flight_fieldnames]
                custom_field_values = [custom_fields.get(field, '') for field in custom_fieldnames]
                row.extend(custom_field_values)

                # Add approaches and persons as comma-separated values
                approaches = ';'.join([approach.type for approach in flight.approaches.all()])
                persons = ';'.join([person.role for person in flight.persons.all()])
                row.append(approaches)
                row.append(persons)

                writer.writerow(row)

        print("Data exported successfully.")

    def get_custom_fieldnames(self, data):
        """Extracts custom field names from the data."""
        if not data:
            return []

        # Find custom field names from the first entry
        for item in data:
            if item['table'] == 'FlightLog' and 'custom_fields' in item['meta']:
                custom_fields = item['meta']['custom_fields']
                return sorted(custom_fields.keys())  # Return sorted custom field names for consistency

        return []

    def render_custom_fields(self, custom_fields, instance):
        """Render custom fields using CustomFieldRenderer."""
        renderer = CustomFieldRenderer(custom_fields, instance)
        return renderer.render_custom_fields()
