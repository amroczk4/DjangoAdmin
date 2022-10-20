from django.contrib import admin

# Register your models here.

from .models import Dishes, Puzzle, UserStats, MainIngredient, Taste, Country

admin.site.register(Dishes)
admin.site.register(UserStats)
admin.site.register(Puzzle)
admin.site.register(MainIngredient)
admin.site.register(Taste)
admin.site.register(Country)