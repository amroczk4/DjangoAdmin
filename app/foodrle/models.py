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
    last_used = models.DateField()
    dish = models.ForeignKey(Dishes, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.dish)

    def was_used_recently(self):
        now = datetime.datetime.now().date()
        return now - datetime.timedelta(days=7) <= self.last_used <= now

    def update_last_used(self):
        today = datetime.datetime.now().date()
        Puzzle.objects.filter(id=self.id).update(last_used=today)


