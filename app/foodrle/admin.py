from django.contrib import admin

# Register your models here.

from .models import Dishes, Puzzle, UserStats

admin.site.register(Dishes)
admin.site.register(UserStats)
admin.site.register(Puzzle)