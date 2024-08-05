from django.db import models

class FlightLogQuerySet(models.QuerySet):
    def with_custom_fields(self):
        return self.filter(custom_fields__isnull=False)

    def by_aircraft(self, aircraft_id):
        return self.filter(aircraft__id=aircraft_id)

    def by_date_range(self, start_date, end_date):
        return self.filter(date__range=(start_date, end_date))

    def total_flight_time(self):
        return self.aggregate(total_time=models.Sum('total_time'))['total_time']

    def total_landings(self):
        return self.aggregate(total_landings=models.Sum('all_landings'))['total_landings']

    def recent_flights(self, limit=10):
        return self.order_by('-date')[:limit]

    def filter_by_pilot(self, user_id):
        return self.filter(persons__user_id=user_id)

class FlightLogManager(models.Manager):
    def get_queryset(self):
        return FlightLogQuerySet(self.model, using=self._db)

    def with_custom_fields(self):
        return self.get_queryset().with_custom_fields()

    def by_aircraft(self, aircraft_id):
        return self.get_queryset().by_aircraft(aircraft_id)

    def by_date_range(self, start_date, end_date):
        return self.get_queryset().by_date_range(start_date, end_date)

    def total_flight_time(self):
        return self.get_queryset().total_flight_time()

    def total_landings(self):
        return self.get_queryset().total_landings()

    def recent_flights(self, limit=10):
        return self.get_queryset().recent_flights(limit)

    def filter_by_pilot(self, user_id):
        return self.get_queryset().filter_by_pilot(user_id)