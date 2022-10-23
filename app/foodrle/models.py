from django.db import models
from django.contrib.auth.models import User
from math import sin, cos, radians, asin, sqrt
from django.core.validators import MaxValueValidator, MinValueValidator

# class Colors(models.Model):
#     name = models.CharField(max_length=128)
#     left_neighbor = models.CharField(max_length=128)
#     right_neighbor = models.CharField(max_length=128)


class Country(models.Model):
    name = models.CharField(max_length=128)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def distance(self, other, unit='mi'):
        """ Computes the distance ('mi' miles (default), or
          'km' kilometers) between one country and another
        """
        if self.name == other.name:
            return 0

        start_lat, start_lon, dest_lat, dest_lon = map(radians,
                                                       [self.latitude, self.longitude, other.latitude, other.longitude])
        # Haversine formula
        dlon = start_lon - dest_lon
        dlat = start_lat - dest_lat
        a = sin(dlat / 2) ** 2 + cos(start_lat) * cos(dest_lat) * sin(dlon / 2) ** 2

        c = 2 * asin(sqrt(a))

        # Radius of earth in kilometers is 6371. Use 3956 for miles
        if unit == 'mi':
            # print(f"Distance from {self.name} to {other.name} is {c * 3956} mi")
            return c * 3956
        else:
            # print(f"Distance from {self.name} to {other.name} is {c * 6371} km")
            return c * 6371

    def direction(self, other):
        if self.name == other.name:
            return 'same'

        dlat = self.latitude - other.latitude
        dlon = self.longitude - other.longitude
        north_or_south = ''
        east_or_west = ''
        delta = 20
        while delta > 0:
            if abs(dlat) > delta:
                if dlat < 0:
                    north_or_south = 'north'
                else:
                    north_or_south = 'south'
            if abs(dlon) > delta:
                if dlon < 0:
                    east_or_west = 'east'
                else:
                    east_or_west = 'west'
            if (north_or_south + east_or_west) != '':
                break
            delta -= 2
        
        if north_or_south + east_or_west == '':
            print("ERROR: ", self.name, other.name)
            assert north_or_south + east_or_west != ''
        # print(f"{other.name} is {north_or_south + east_or_west} of {self.name}")
        return north_or_south + east_or_west


class Taste(models.Model):
    sweet = models.BooleanField()
    salty = models.BooleanField()
    sour = models.BooleanField()
    bitter = models.BooleanField()
    umami = models.BooleanField()


class MainIngredient(models.Model):
    name = models.CharField(max_length=128)
    food_group = models.IntegerField(
        validators=[MaxValueValidator(8), MinValueValidator(1)]
    )


# class Calories(models.Model):
#     name = models.CharField(max_length=128)
#     calories = models.IntegerField()

#     def get_difference(self, other):
#         return self.calories - other.calories


class Dishes(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    # colors_id = models.ForeignKey(Colors, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    taste = models.ForeignKey(Taste, on_delete=models.CASCADE)
    main_ingredient = models.ForeignKey(MainIngredient, on_delete=models.CASCADE)
    calories = models.IntegerField(default=0)
    def is_same(self, other):
        return self.name == other.name


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


class Puzzle(models.Model):
    last_used = models.DateField()
    dish = models.ForeignKey(Dishes, on_delete=models.CASCADE)


