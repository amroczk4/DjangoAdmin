from django.db import models
from django.contrib.auth.models import User
from math import atan2, degrees, sin, cos, radians, asin, sqrt
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime


class Country(models.Model):
    name = models.CharField(max_length=128)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name

    # def distance(self, other, unit='mi'):
    #     """ Computes the distance ('mi' miles (default), or
    #       'km' kilometers) between one country and another
    #     """
    #     if self.name == other.name:
    #         return 0

    #     start_lat, start_lon, dest_lat, dest_lon = map(radians,
    #                                                    [self.latitude, self.longitude, other.latitude, other.longitude])
    #     # Haversine formula
    #     dlon = start_lon - dest_lon
    #     dlat = start_lat - dest_lat
    #     a = sin(dlat / 2) ** 2 + cos(start_lat) * cos(dest_lat) * sin(dlon / 2) ** 2

    #     c = 2 * asin(sqrt(a))

    #     # Radius of earth in kilometers is 6371. Use 3956 for miles
    #     if unit == 'mi':
    #         # print(f"Distance from {self.name} to {other.name} is {c * 3956} mi")
    #         return c * 3956
    #     else:
    #         # print(f"Distance from {self.name} to {other.name} is {c * 6371} km")
    #         return c * 6371

    # def bearing(self, other):
    #     dest_lon = other.longitude
    #     dest_lat = other.latitude
    #     start_lat = self.latitude
    #     start_lon = self.longitude

    #     start_lat, start_lon, dest_lat, dest_lon = map(radians,
    #                                                     [self.latitude, self.longitude, other.latitude, other.longitude])

    #     y = sin(dest_lon - start_lon) * cos(dest_lat)
    #     x = cos(start_lat) * sin(dest_lat) - sin(start_lat) * cos(dest_lat) * cos(dest_lon - start_lon)
    #     brng = atan2(y, x)
    #     brng = degrees(brng)
    #     if brng < 0:
    #         brng = brng + 360

    #     def card_ord_dir(brng):
            
    #         if 0 <= brng <= 22 or 337 < brng <= 360:
    #             return 'north'
    #         elif 22 < brng <= 67:
    #             return 'northeast'
    #         elif 67 < brng <= 112:
    #             return 'east'
    #         elif 112 < brng <= 157:
    #             return 'southeast'
    #         elif 157< brng <= 202:
    #             return 'south'
    #         elif 202 < brng <= 247:
    #             return 'southwest'
    #         elif 247 < brng <= 292:
    #             return 'west'
    #         else:
    #             return 'northwest'

    #     print(f'{brng} from {self.name} to {other.name}' )           
    #     return card_ord_dir(brng)


    # def direction(self, other):
    #     """
    #     Computes the direction of 'other' in relation to 'self'
    #     if the countries are within 'delta' degrees of latitude and
    #     longitude of one another bearing is used to compute
    #     direction instead
    #     """
    #     if self.name == other.name:
    #         return 'same'
        
    #     dlat = self.latitude - other.latitude
    #     dlon = self.longitude - other.longitude
    #     north_or_south = ''
    #     east_or_west = ''
    #     delta = 20
    #     while delta > 0:
    #         if abs(dlat) > delta:
    #             if dlat < 0:
    #                 north_or_south = 'north'
    #             else:
    #                 north_or_south = 'south'
    #         if abs(dlon) > delta:
    #             if dlon < 0:
    #                 east_or_west = 'east'
    #             else:
    #                 east_or_west = 'west'
    #         if north_or_south + east_or_west != '':
    #             break
    #         delta = delta - 2

    #     if north_or_south + east_or_west == '':
    #         return self.bearing(other)
    #     # print(f"{other.name} is {north_or_south + east_or_west} of {self.name}")
    #     return north_or_south + east_or_west


class Taste(models.Model):
    sweet = models.BooleanField()
    salty = models.BooleanField()
    sour = models.BooleanField()
    bitter = models.BooleanField()
    umami = models.BooleanField()

    def __str__(self):
        str = ''
        if self.sweet:
            str = str + "Sweet "
        if self.salty:
            str = str + "Salty "
        if self.sour:
            str = str + "Sour "
        if self.bitter:
            str = str + "Bitter "
        if self.umami:
            str = str + "Umami "
        return str


class MainIngredient(models.Model):
    name = models.CharField(max_length=128)
    food_group = models.IntegerField(
        validators=[MaxValueValidator(8), MinValueValidator(1)]
    )

    def __str__(self):
        return f"{self.name}: {self.food_group}"

    def same_name_same_group(self, other):
        return self.name == other.name and self.food_group == other.food_group

    def food_group_eq(self, other):
        """
            Returns True if the main ingredients share
            the same food_group and False otherwise
        """
        return self.food_group == other.food_group


class Dishes(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    taste = models.ForeignKey(Taste, on_delete=models.CASCADE)
    main_ingredient = models.ForeignKey(
        MainIngredient, on_delete=models.CASCADE)
    calories = models.BigIntegerField(default=0)

    def dish_name_eq(self, other):
        return self.name == other.name

    def __str__(self):
        return self.name


class UserStats(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    curr_streak = models.BigIntegerField(default=0)
    max_streak = models.BigIntegerField(default=0)
    last_played = models.DateField()
    games_played = models.BigIntegerField(default=0)
    win_1 = models.IntegerField(default=0)
    win_2 = models.IntegerField(default=0)
    win_3 = models.IntegerField(default=0)
    win_4 = models.IntegerField(default=0)
    win_5 = models.IntegerField(default=0)
    win_6 = models.IntegerField(default=0)

    def get_win_pct(self):
        wins = self.win_1 + self.win_2 + self.win_3 + self.win_4 + self.win_5 + self.win_6
        return wins / self.games_played * 100

    def __str__(self):
        return str(self.user)


class Puzzle(models.Model):
    last_used = models.DateField()
    dish = models.ForeignKey(Dishes, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.dish)

    def was_used_recently(self):
        now = datetime.datetime.now().date()
        return now - datetime.timedelta(days=7) <= self.last_used <= now

    def update_last_used(self):
        today = datetime.datetime.now.date()
        self.objects.get(dish=self.dish).update(last_used=today)


