import json
import csv
from django.apps import apps
from django.db.models import Model
from .models import Aircraft, FlightLog, Approach, Person
from .custom_field_renderer import CustomFieldRenderer

class PilotLogExporter:
    """
    Class to handle the export of pilot log data to a CSV file.
    """
    def __init__(self, json_file_path, csv_file_path):
        """
        Initialize the exporter with the given JSON and CSV file paths.
        :param json_file_path: Path to the JSON file containing the data to export.
        :param csv_file_path: Path to the CSV file to write the exported data.
        """
        self.json_file_path = json_file_path
        self.csv_file_path = csv_file_path

    def export_to_csv(self):
        """
        Export the data to a CSV file.
        """
        try:
            with open(self.json_file_path, 'r') as file:
                data = json.load(file)

            self.export_aircraft_data()
            self.export_flight_log_data(data)

            print("Data exported successfully.")
        except FileNotFoundError:
            print(f"Error: File not found - {self.json_file_path}")
        except json.JSONDecodeError:
            print("Error: Failed to decode JSON file.")
        except IOError as e:
            print(f"Error: I/O operation failed - {e}")
        except Exception as e:
            print(f"Error: Unexpected error occurred - {e}")

    def export_aircraft_data(self):
        """
        Export aircraft data to the CSV file.
        """
        fieldnames = self.get_model_field_names(Aircraft)
        with open(self.csv_file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Aircraft Table'])
            writer.writerow(fieldnames)
            writer.writerows([[getattr(aircraft, field, '') for field in fieldnames] for aircraft in Aircraft.objects.all()])

    def export_flight_log_data(self, data):
        """
        Export flight log data to the CSV file.
        :param data: JSON data.
        """
        fieldnames = self.get_model_field_names(FlightLog)
        custom_fieldnames = self.get_custom_fieldnames(data)
        combined_fieldnames = fieldnames + custom_fieldnames + ['approaches', 'persons']

        with open(self.csv_file_path, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([])
            writer.writerow(['Flights Table'])
            writer.writerow(combined_fieldnames)
            
            for flight in FlightLog.objects.all():
                custom_fields = self.render_custom_fields(flight.custom_fields, flight)
                row = [getattr(flight, field, '') for field in fieldnames]
                custom_field_values = [custom_fields.get(field, '') for field in custom_fieldnames]
                approaches = ';'.join([approach.type for approach in flight.approaches.all()])
                persons = ';'.join([person.role for person in flight.persons.all()])
                writer.writerow(row + custom_field_values + [approaches, persons])

    @staticmethod
    def get_model_field_names(model: Model):
        """
        Get the field names of a given model.
        :param model: Django model.
        :return: List of field names.
        """
        return [field.name for field in model._meta.get_fields() if not field.is_relation]

    def get_custom_fieldnames(self, data):
        """
        Extract custom field names from the JSON data.
        :param data: JSON data.
        :return: List of custom field names.
        """
        if not data:
            return []
        return sorted({key for item in data if item['table'] == 'FlightLog' for key in item['meta'].get('custom_fields', {}).keys()})

    def render_custom_fields(self, custom_fields, instance):
        """
        Render custom fields using CustomFieldRenderer.
        :param custom_fields: Custom fields data.
        :param instance: The instance of the model (if applicable).
        :return: Dictionary of rendered custom fields.
        """
        try:
            renderer = CustomFieldRenderer(custom_fields, instance)
            return renderer.render_custom_fields()
        except Exception as e:
            print(f"Error rendering custom fields: {e}")
            return {}