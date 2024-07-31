import os
import django
import random
from datetime import datetime, timedelta
from faker import Faker

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

from pilotlog.models import Aircraft, FlightLog, Person, Approach

fake = Faker()


def generate_unique_aircraft_id():
    while True:
        aircraft_id = f"N{random.randint(10000, 99999)}"
        if not Aircraft.objects.filter(aircraft_id=aircraft_id).exists():
            return aircraft_id

def create_aircraft():
    aircraft_data = {
        'aircraft_id': generate_unique_aircraft_id(),
        'equipment_type': 'Single Engine',
        'type_code': 'C172',
        'year': 2015,
        'make': 'Cessna',
        'model': '172 Skyhawk',
        'category': 'Landplane',
        'aircraft_class': 'Light',
        'gear_type': 'Tricycle',
        'engine_type': 'Piston',
        'complex': False,
        'high_performance': False,
        'pressurized': False,
        'taa': False
    }

    aircraft = Aircraft.objects.create(**aircraft_data)
    print(f"Successfully created aircraft: {aircraft}")
    return aircraft

def create_flight_log(aircraft):
    departure_time = fake.date_time_this_year()
    arrival_time = departure_time + timedelta(hours=random.uniform(0.5, 2.0))

    flight_log_data = {
        'aircraft': aircraft,
        'date': departure_time.date(),
        'from_airport': fake.city(),
        'to_airport': fake.city(),
        'route': fake.text(max_nb_chars=50),
        'time_out': departure_time.time(),
        'time_off': departure_time.time(),
        'time_on': arrival_time.time(),
        'time_in': arrival_time.time(),
        'on_duty': departure_time.time(),
        'off_duty': arrival_time.time(),
        'total_time': (arrival_time - departure_time).seconds / 3600.0,
        'pic': random.uniform(0, 2),
        'sic': random.uniform(0, 2),
        'night': random.uniform(0, 2),
        'solo': random.uniform(0, 2),
        'cross_country': random.uniform(0, 2),
        'nvg': random.uniform(0, 2),
        'nvg_ops': random.uniform(0, 2),
        'distance': random.uniform(50, 500),
        'day_takeoffs': random.randint(0, 5),
        'day_landings_full_stop': random.randint(0, 5),
        'night_takeoffs': random.randint(0, 2),
        'night_landings_full_stop': random.randint(0, 2),
        'all_landings': random.randint(0, 10),
        'actual_instrument': random.uniform(0, 2),
        'simulated_instrument': random.uniform(0, 2),
        'hobbs_start': random.uniform(0, 1000),
        'hobbs_end': random.uniform(0, 1000),
        'tach_start': random.uniform(0, 1000),
        'tach_end': random.uniform(0, 1000),
        'holds': random.randint(0, 10),
        'dual_given': random.uniform(0, 2),
        'dual_received': random.uniform(0, 2),
        'simulated_flight': random.uniform(0, 2),
        'ground_training': random.uniform(0, 2),
        'instructor_name': fake.name(),
        'instructor_comments': fake.text(max_nb_chars=100),
        'flight_review': fake.boolean(),
        'checkride': fake.boolean(),
        'ipc': fake.boolean(),
        'nvg_proficiency': fake.boolean(),
        'faa_6158': fake.boolean(),
        'remarks': fake.text(max_nb_chars=200),
        'custom_fields': {
            'CustomFieldNameText': fake.word(),
            'CustomFieldNameNumeric': random.uniform(0, 100),
            'CustomFieldNameHours': random.uniform(0, 100),
            'CustomFieldNameCounter': random.randint(0, 100),
            'CustomFieldNameDate': str(fake.date_this_year()),
            'CustomFieldNameDateTime': str(fake.date_time_this_year()),
            'CustomFieldNameToggle': fake.boolean()
        }
    }

    flight_log = FlightLog.objects.create(**flight_log_data)
    print(f"Successfully created flight log: {flight_log}")
    return flight_log

def create_people(flight_log):
    people = []
    for _ in range(6):
        person = Person(
            flight_log=flight_log,
            name=fake.name(),
            role=fake.word(),
            email=fake.email()
        )
        people.append(person)
    Person.objects.bulk_create(people)
    print(f"Successfully created {len(people)} people.")

def create_approaches(flight_log):
    approaches = []
    for _ in range(6):
        approach = Approach(
            flight_log=flight_log,
            type=fake.word(),
            runway=fake.bothify(text='##'),
            airport=fake.city(),
            comments=fake.text(max_nb_chars=100)
        )
        approaches.append(approach)
    Approach.objects.bulk_create(approaches)
    print(f"Successfully created {len(approaches)} approaches.")

if __name__ == "__main__":
    print("Creating Aircraft...")
    aircraft = create_aircraft()
    print("Creating Flight Log...")
    flight_log = create_flight_log(aircraft)
    print("Creating People...")
    create_people(flight_log)
    print("Creating Approaches...")
    create_approaches(flight_log)
    print("Data population complete.")