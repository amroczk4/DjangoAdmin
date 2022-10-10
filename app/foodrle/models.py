from django.db import models
from django.contrib.auth.models import User


class Colors(models.Model):
    name = models.CharField(max_length=128)
    left_neighbor = models.CharField(max_length=128)
    right_neighbor = models.CharField(max_length=128)


class Country(models.Model):
    name = models.CharField(max_length=128)
    latitude = models.FloatField()
    longitude = models.FloatField()


class Taste(models.Model):
    sweet = models.BooleanField()
    salty = models.BooleanField()
    sour = models.BooleanField()
    bitter = models.BooleanField()
    umami = models.BooleanField()


class MainIngredient(models.Model):
    name = models.CharField(max_length=128)
    food_group = models.CharField(max_length=128)


class Calories(models.Model):
    name = models.CharField(max_length=128)
    calories = models.IntegerField()


class Dishes(models.Model):
    name = models.CharField(max_length=128)
    colors_id = models.ForeignKey(Colors, on_delete=models.CASCADE)
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE)
    taste_id = models.ForeignKey(Taste, on_delete=models.CASCADE)
    main_ingredient_id = models.ForeignKey(MainIngredient, on_delete=models.CASCADE)
    calories = models.ForeignKey(Calories, on_delete=models.CASCADE)


class UserStats(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    curr_streak = models.BigIntegerField()
    max_streak = models.BigIntegerField()
    last_played = models.DateField()
    games_played = models.BigIntegerField()
    win_1 = models.IntegerField()
    win_2 = models.IntegerField()
    win_3 = models.IntegerField()
    win_4 = models.IntegerField()
    win_5 = models.IntegerField()
    win_6 = models.IntegerField()


class Puzzle(models.Model):
    last_used = models.DateField()
    dish_id = models.ForeignKey(Dishes, on_delete=models.CASCADE)


