from django.db import models

# Create your models here.
class Route(models.Model):
    route_id = models.CharField(max_length=200, primary_key=True)
    route_short_name = models.TextField()
    route_long_name = models.TextField()
    route_type = models.TextField()
    route_color = models.CharField(max_length=6)

    def __str__(self):
        return self.route_long_name


class Stop(models.Model):
    stop_id = models.CharField(max_length=20, primary_key=True)
    stop_code = models.CharField(max_length=20)
    stop_name = models.TextField()
    stop_lat = models.FloatField()
    stop_lon = models.FloatField()
    zone_id = models.CharField(max_length=20)
    stop_url = models.TextField()
    location_type = models.IntegerField()
    parent_station = models.CharField(max_length=20)
    platform_code = models.CharField(max_length=20)
    wheelchair_boarding = models.BooleanField()

    def __str__(self):
        return self.stop_name + ' ' + self.platform_code


class StopTime(models.Model):
    arrival_time = models.CharField(max_length=20)
    departure_time = models.CharField(max_length=20)
    stop_sequence = models.IntegerField()
    pickup_type = models.IntegerField()
    drop_off_type = models.IntegerField()
    trip = models.ForeignKey(
        'Trip',
        on_delete=models.CASCADE,
    )
    stop = models.ForeignKey(
        'Stop',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.arrival_time

class Trip(models.Model):
    trip_id = models.CharField(max_length=20, primary_key=True)
    trip_headsign = models.TextField()
    trip_short_name = models.TextField()
    service_id = models.TextField()
    direction_id = models.IntegerField()
    wheelchair_accessible = models.BooleanField()
    bikes_allowed = models.BooleanField()
    route = models.ForeignKey(
        'Route',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.trip_short_name
