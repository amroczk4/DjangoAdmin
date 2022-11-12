from django.contrib import admin

from import_export.admin import ImportExportActionModelAdmin
from .models import Dishes, Puzzle, MainIngredient, Taste, Country


@admin.register(Country)
class CountryAdmin(ImportExportActionModelAdmin):
    list_display = ("id", "name", "latitude", "longitude")
    pass


@admin.register(Taste)
class TasteAdmin(ImportExportActionModelAdmin):
    list_display = ("id", "sweet", "salty", "sour", "bitter", "umami")
    pass


@admin.register(MainIngredient)
class MainIngredientAdmin(ImportExportActionModelAdmin):
    list_display = ("id", "name", "food_group")
    pass


@admin.register(Puzzle)
class PuzzleAdmin(ImportExportActionModelAdmin):
    list_display = ("id", "player", "is_win", "ans_dish", "guess1", "guess2", "guess3", "guess4", "guess5", "guess6")
    pass


@admin.register(Dishes)
class TasteAdmin(ImportExportActionModelAdmin):
    list_display = ("id", "name", "country", "taste", "main_ingredient", "calories")
    pass

