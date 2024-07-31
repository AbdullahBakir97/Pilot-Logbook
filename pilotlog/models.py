from django.db import models
from django.contrib.auth.models import User
import json
from django.template import Context, Template
from django.core.exceptions import ValidationError
from .custom_field_renderer import CustomFieldRenderer

class Aircraft(models.Model):
    aircraft_id = models.CharField(max_length=50, unique=True)
    equipment_type = models.CharField(max_length=50)
    type_code = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    aircraft_class = models.CharField(max_length=50)
    gear_type = models.CharField(max_length=50)
    engine_type = models.CharField(max_length=50)
    complex = models.BooleanField()
    high_performance = models.BooleanField()
    pressurized = models.BooleanField()
    taa = models.BooleanField()

    def __str__(self):
        return f"{self.make} {self.model} ({self.aircraft_id})"
    
class Approach(models.Model):
    type = models.CharField(max_length=100)
    runway = models.CharField(max_length=50)
    airport = models.CharField(max_length=50)
    comments = models.TextField(blank=True)

    def __str__(self):
        return f"Approach {self.type} at {self.airport}"
    
class Person(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user', null=True, blank=True)
    role = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username if self.user else 'No user'} ({self.role})"


    
class FlightLog(models.Model):
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE, related_name='aircraft')
    date = models.DateField()
    from_airport = models.CharField(max_length=50)
    to_airport = models.CharField(max_length=50)
    route = models.TextField(null=True, blank=True)
    time_out = models.TimeField()
    time_off = models.TimeField()
    time_on = models.TimeField()
    time_in = models.TimeField()
    on_duty = models.TimeField()
    off_duty = models.TimeField()
    total_time = models.DecimalField(max_digits=6, decimal_places=2)
    pic = models.DecimalField(max_digits=6, decimal_places=2)
    sic = models.DecimalField(max_digits=6, decimal_places=2)
    night = models.DecimalField(max_digits=6, decimal_places=2)
    solo = models.DecimalField(max_digits=6, decimal_places=2)
    cross_country = models.DecimalField(max_digits=6, decimal_places=2)
    nvg = models.DecimalField(max_digits=6, decimal_places=2)
    nvg_ops = models.DecimalField(max_digits=6, decimal_places=2)
    distance = models.DecimalField(max_digits=6, decimal_places=2)
    day_takeoffs = models.PositiveIntegerField()
    day_landings_full_stop = models.PositiveIntegerField()
    night_takeoffs = models.PositiveIntegerField()
    night_landings_full_stop = models.PositiveIntegerField()
    all_landings = models.PositiveIntegerField()
    actual_instrument = models.DecimalField(max_digits=6, decimal_places=2)
    simulated_instrument = models.DecimalField(max_digits=6, decimal_places=2)
    hobbs_start = models.DecimalField(max_digits=6, decimal_places=2)
    hobbs_end = models.DecimalField(max_digits=6, decimal_places=2)
    tach_start = models.DecimalField(max_digits=6, decimal_places=2)
    tach_end = models.DecimalField(max_digits=6, decimal_places=2)
    holds = models.PositiveIntegerField()
    dual_given = models.DecimalField(max_digits=6, decimal_places=2)
    dual_received = models.DecimalField(max_digits=6, decimal_places=2)
    simulated_flight = models.DecimalField(max_digits=6, decimal_places=2)
    ground_training = models.DecimalField(max_digits=6, decimal_places=2)
    instructor_name = models.CharField(max_length=100, blank=True)
    instructor_comments = models.TextField(blank=True)
    flight_review = models.BooleanField(default=False)
    checkride = models.BooleanField(default=False)
    ipc = models.BooleanField(default=False)
    nvg_proficiency = models.BooleanField(default=False)
    faa_6158 = models.BooleanField(default=False)
    remarks = models.TextField(blank=True, null=True)
    custom_fields = models.JSONField(default=dict, blank=True)
    approaches = models.ManyToManyField(Approach, related_name='approaches')
    persons = models.ManyToManyField(Person, related_name='persons')
    
    def __str__(self):
        return f"Flight on {self.date} from {self.from_airport} to {self.to_airport}"

    def clean(self):
        # Custom validation for custom fields
        super().clean()
        custom_fields = self.custom_fields
        if 'required_key' not in custom_fields:
            raise ValidationError('Custom fields must include "required_key"')

    def save(self, *args, **kwargs):
        # Process custom fields before saving
        renderer = CustomFieldRenderer(self.custom_fields, self)
        self.custom_fields = renderer.render_custom_fields()
        super().save(*args, **kwargs)
