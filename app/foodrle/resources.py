from import_export import resources
from foodrle.models import Country, Taste, Dishes, MainIngredient, Puzzle

class CountryResource(resources.ModelResource):
    class Meta:
        model = Country


class TasteResource(resources.ModelResource):
    class Meta:
        model = Taste


class DishResource(resources.ModelResource):
    class Meta:
        model = Dishes


class MainIngredientResource(resources.ModelResource):
    class Meta:
        model = MainIngredient


class PuzzleResource(resources.ModelResource):
    class Meta:
        model = Puzzle