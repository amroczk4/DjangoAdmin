from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime


class Country(models.Model):
    name = models.CharField(max_length=128)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name


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
        return f"{self.name}"


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
    id = models.BigAutoField(primary_key=True)
    ans_dish = models.ForeignKey(Dishes, on_delete=models.CASCADE)
    guess1 = models.CharField(max_length=128, blank=True, default='')
    guess2 = models.CharField(max_length=128, blank=True, default='')
    guess3 = models.CharField(max_length=128, blank=True, default='')
    guess4 = models.CharField(max_length=128, blank=True, default='')
    guess5 = models.CharField(max_length=128, blank=True, default='')
    guess6 = models.CharField(max_length=128, blank=True, default='')

    def get_guesses_as_dict(self):
        """ returns guess1 ... guess6 as a dictionary
        """
        full_dict = self.__dict__
        ignore_keys = ['_state', 'id', 'ans_dish_id']
        guess_dict = {
            key: full_dict[key] for key in full_dict
            if key not in ignore_keys
        }
        return guess_dict


