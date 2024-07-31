import json
import csv
from .models import Aircraft, FlightLog, Approach, Person

class PilotLogExporter:
    def __init__(self, json_file_path, csv_file_path):
        self.json_file_path = json_file_path
        self.csv_file_path = csv_file_path

    def export_to_csv(self):
        with open(self.json_file_path, 'r') as file:
            data = json.load(file)

        aircraft_fieldnames = [
            'AircraftID', 'EquipmentType', 'TypeCode', 'Year', 'Make', 'Model',
            'Category', 'Class', 'GearType', 'EngineType', 'Complex',
            'HighPerformance', 'Pressurized', 'TAA'
        ]

        flight_fieldnames = [
            'Date', 'AircraftID', 'From', 'To', 'Route', 'TimeOut', 'TimeOff',
            'TimeOn', 'TimeIn', 'OnDuty', 'OffDuty', 'TotalTime', 'PIC', 'SIC',
            'Night', 'Solo', 'CrossCountry', 'NVG', 'NVGOps', 'Distance',
            'DayTakeoffs', 'DayLandingsFullStop', 'NightTakeoffs', 'NightLandingsFullStop',
            'AllLandings', 'ActualInstrument', 'SimulatedInstrument', 'HobbsStart',
            'HobbsEnd', 'TachStart', 'TachEnd', 'Holds', 'Approach1', 'Approach2',
            'Approach3', 'Approach4', 'Approach5', 'Approach6', 'DualGiven',
            'DualReceived', 'SimulatedFlight', 'GroundTraining', 'InstructorName',
            'InstructorComments', 'Person1', 'Person2', 'Person3', 'Person4',
            'Person5', 'Person6', 'FlightReview', 'Checkride', 'IPC',
            'NVGProficiency', 'FAA6158', 'CustomFieldText', 'CustomFieldNumeric',
            'CustomFieldHours', 'CustomFieldCounter', 'CustomFieldDate',
            'CustomFieldDateTime', 'CustomFieldToggle'
        ]

        with open(self.csv_file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)

            writer.writerow(['Aircraft Table'])
            writer.writerow(aircraft_fieldnames)
            for aircraft in Aircraft.objects.all():
                row = [
                    aircraft.aircraft_id, aircraft.equipment_type, aircraft.type_code, aircraft.year, aircraft.make,
                    aircraft.model, aircraft.category, aircraft.aircraft_class, aircraft.gear_type, aircraft.engine_type,
                    aircraft.complex, aircraft.high_performance, aircraft.pressurized, aircraft.taa
                ]
                writer.writerow(row)

            writer.writerow([])
            writer.writerow(['Flights Table'])
            writer.writerow(flight_fieldnames)
            for flight in FlightLog.objects.all():
                custom_fields = self.get_custom_fields(flight.custom_fields)
                
                row = [
                    flight.date, flight.aircraft.aircraft_id, flight.from_airport, flight.to_airport, flight.route, flight.time_out,
                    flight.time_off, flight.time_on, flight.time_in, flight.on_duty, flight.off_duty, flight.total_time, flight.pic,
                    flight.sic, flight.night, flight.solo, flight.cross_country, flight.nvg, flight.nvg_ops, flight.distance,
                    flight.day_takeoffs, flight.day_landings_full_stop, flight.night_takeoffs, flight.night_landings_full_stop,
                    flight.all_landings, flight.actual_instrument, flight.simulated_instrument, flight.hobbs_start, flight.hobbs_end,
                    flight.tach_start, flight.tach_end, flight.holds, *self.get_approaches(flight),
                    flight.dual_given, flight.dual_received, flight.simulated_flight, flight.ground_training, flight.instructor_name,
                    flight.instructor_comments, *self.get_persons(flight), flight.flight_review,
                    flight.checkride, flight.ipc, flight.nvg_proficiency, flight.faa_6158,
                    custom_fields.get('CustomFieldText', ''), custom_fields.get('CustomFieldNumeric', ''),
                    custom_fields.get('CustomFieldHours', ''), custom_fields.get('CustomFieldCounter', ''),
                    custom_fields.get('CustomFieldDate', ''), custom_fields.get('CustomFieldDateTime', ''),
                    custom_fields.get('CustomFieldToggle', '')
                ]

                writer.writerow(row)

        print("Data exported successfully.")

    def get_approaches(self, flight):
        approaches = list(flight.approaches.values_list('id', flat=True))
        return approaches + [''] * (6 - len(approaches))  # Ensure 6 approach fields

    def get_persons(self, flight):
        persons = list(flight.persons.values_list('user__username', flat=True))
        return persons + [''] * (6 - len(persons))  # Ensure 6 person fields

    def get_custom_fields(self, custom_fields):
        """Extracts specific custom fields and returns them in a dictionary."""
        return {
            'CustomFieldText': custom_fields.get('Text', ''),
            'CustomFieldNumeric': custom_fields.get('Numeric', ''),
            'CustomFieldHours': custom_fields.get('Hours', ''),
            'CustomFieldCounter': custom_fields.get('Counter', ''),
            'CustomFieldDate': custom_fields.get('Date', ''),
            'CustomFieldDateTime': custom_fields.get('DateTime', ''),
            'CustomFieldToggle': custom_fields.get('Toggle', '')
        }