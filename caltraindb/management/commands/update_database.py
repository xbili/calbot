#!/usr/bin/env python

"""
Author: Bili Xu
## Update Database Management Command ##

Updates the database entries with newly parsed data from the developer website
"""

from django.core.management.base import BaseCommand, CommandError
from caltraindb.models import *
from lib import get_parsed_schedule


class Command(BaseCommand):
    help = 'Updates the database entires with new parsed data from the website'

    def handle(self, *args, **kwargs):
        Route.objects.all().delete()
        Stop.objects.all().delete()
        StopTime.objects.all().delete()
        Trip.objects.all().delete()

        data = get_parsed_schedule()

        new_routes = []
        new_stops = []
        new_stop_times = []
        new_trips = []

        for tbl, rows in data.items():
            for row in rows:
                if tbl == 'routes':
                    new_route = Route(
                        route_id=row[0],
                        route_short_name=row[1],
                        route_long_name=row[2],
                        route_type=row[3],
                        route_color=row[4],
                    )
                    new_routes.append(new_route)
                elif tbl == 'stops':
                    new_stop = Stop(
                        stop_id=row[0],
                        stop_code=row[1],
                        stop_name=row[2],
                        stop_lat=float(row[3]),
                        stop_lon=float(row[4]),
                        zone_id=row[5],
                        stop_url=row[6],
                        location_type=row[7],
                        parent_station=row[8],
                        platform_code=row[9],
                        wheelchair_boarding=row[10],
                    )
                    new_stops.append(new_stop)
                elif tbl == 'stop_times':
                    new_stop_time = StopTime(
                        arrival_time=row[1],
                        departure_time=row[2],
                        stop_sequence=int(row[4]),
                        pickup_type=int(row[5]),
                        drop_off_type=int(row[6]),
                        trip_id=row[0],
                        stop_id=int(row[3]),
                    )
                    new_stop_times.append(new_stop_time)
                elif tbl == 'trips':
                    new_trip = Trip(
                        trip_id=row[2],
                        trip_headsign=row[3],
                        trip_short_name=row[4],
                        service_id=row[1],
                        direction_id=int(row[5]),
                        wheelchair_accessible=row[7],
                        bikes_allowed=row[8],
                        route_id=row[0],
                    )
                    new_trips.append(new_trip)
                else:
                    self.stdout.error(self.style.ERROR('Invalid table type.'))
                    break

        [route.save() for route in new_routes]
        [stop.save() for stop in new_stops]
        [trip.save() for trip in new_trips]
        [stop_time.save() for stop_time in new_stop_times]

        self.stdout.write(self.style.SUCCESS('Successfully updated database'))
