from django.contrib import admin

from import_export.admin import ImportExportActionModelAdmin
from .models import Dishes, Puzzle, MainIngredient, Taste, Country


@admin.register(Country)
class CountryAdmin(ImportExportActionModelAdmin):
    list_display = ("id", "name", "latitude", "longitude")


@admin.register(Taste)
class TasteAdmin(ImportExportActionModelAdmin):
    list_display = ("id", "sweet", "salty", "sour", "bitter", "umami")


@admin.register(MainIngredient)
class MainIngredientAdmin(ImportExportActionModelAdmin):
    list_display = ("id", "name", "food_group")


@admin.register(Puzzle)
class PuzzleAdmin(ImportExportActionModelAdmin):
    list_display = ("id", "player", "is_win", "ans_dish", "guess1", "guess2", "guess3", "guess4", "guess5", "guess6")


@admin.register(Dishes)
class TasteAdmin(ImportExportActionModelAdmin):
    list_display = ("id", "name", "country", "taste", "main_ingredient", "calories")