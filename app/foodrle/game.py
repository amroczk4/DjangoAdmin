from random import randint
from .models import Country, Dishes, Taste, MainIngredient, Puzzle
from math import atan2, degrees, sin, cos, radians, asin, sqrt
from datetime import datetime

TOTAL_PUZZLES = Puzzle.objects.count()
RED = 0
YELLOW = 1
GREEN = 2

def get_puzzle_of_day() -> Dishes:
    """ Finds the puzzle of the day (pod) and returns
        a dish, if the puzzle hasn't been selected
        yet, a random puzzle is chosen as the pod
    """
    today = datetime.now().date()
    try:
        pod = Puzzle.objects.get(last_used=today)
    except Puzzle.DoesNotExist:
        # select a random puzzle, update last used, and return it
        pod = Puzzle.objects.get(pk=randint(1, TOTAL_PUZZLES))
        pod.update_last_used()
    
    return pod.dish
    

def get_dish_by_name(dish_name: str):
    """ SELECT * FROM Dishes WHERE name=dish_name
        Returns None if dish_name represents a non-existent dish
    """
    try:
        return Dishes.objects.get(name=dish_name)
    except Dishes.DoesNotExist:
        return None
        
        
def distance(guessed_country: Country, answer: Country, unit='mi') -> int:
    """ Computes the distance ('mi' miles (default), or
        'km' kilometers) between one country and another
    """
    if guessed_country.name == answer.name:
        return 0

    start_lat, start_lon, dest_lat, dest_lon = map(radians,
                                                    [guessed_country.latitude, guessed_country.longitude, 
                                                    answer.latitude, answer.longitude])
    # Haversine formula
    dlon = start_lon - dest_lon
    dlat = start_lat - dest_lat
    a = sin(dlat / 2) ** 2 + cos(start_lat) * cos(dest_lat) * sin(dlon / 2) ** 2

    c = 2 * asin(sqrt(a))

    # Radius of earth in kilometers is 6371. Use 3956 for miles
    if unit == 'mi':
        return round(c * 3956)
    else: # km
        return round(c * 6371)


def direction(guessed_country: Country, answer: Country) -> str:
        """
        Computes the direction of 'other' in relation to 'self'
        if the countries are within 'delta' degrees of latitude and
        longitude of one another bearing is used to compute
        direction instead
        """
        if guessed_country.name == answer.name:
            return 'same'
        
        dlat = guessed_country.latitude - answer.latitude
        dlon = guessed_country.longitude - answer.longitude
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
            if north_or_south + east_or_west != '':
                break
            delta = delta - 2

        if north_or_south + east_or_west == '':
            return guessed_country.bearing(answer)

        return north_or_south + east_or_west


def bearing(guessed_country: Country, answer: Country) -> str:
    """ Serving as a backup to direction function,
        computes the bearing angle between
        two countries and returns a direction string
    """
    
    dest_lon = answer.longitude
    dest_lat = answer.latitude
    start_lat = guessed_country.latitude
    start_lon = guessed_country.longitude

    #
    def card_ord_dir(brng: float) -> str:
        if 0 <= brng <= 22 or 337 < brng <= 360:
            return 'north'
        elif 22 < brng <= 67:
            return 'northeast'
        elif 67 < brng <= 112:
            return 'east'
        elif 112 < brng <= 157:
            return 'southeast'
        elif 157< brng <= 202:
            return 'south'
        elif 202 < brng <= 247:
            return 'southwest'
        elif 247 < brng <= 292:
            return 'west'
        else:
            return 'northwest' 
    #

    start_lat, start_lon, dest_lat, dest_lon = map(radians, [start_lat, start_lon, dest_lat, dest_lon])

    y = sin(dest_lon - start_lon) * cos(dest_lat)
    x = cos(start_lat) * sin(dest_lat) - sin(start_lat) * cos(dest_lat) * cos(dest_lon - start_lon)
    brng = atan2(y, x)
    brng = degrees(brng)
    if brng < 0:
        brng = brng + 360

    return card_ord_dir(brng)


def country_hint(answer_country: Country, guessed_country: Country):
    res = {
        'country': guessed_country.name, 
        'dist': distance(guessed_country, answer_country),
        'dir': direction(guessed_country, answer_country)
        }
    
    print(f'\tCountry: {res}')
    return res


def main_ingredient_hint(answer: MainIngredient, guess_ingr: MainIngredient):
    res = {}
    if answer.name == guess_ingr.name:
        res.update({guess_ingr.name: GREEN})
    elif answer.food_group == guess_ingr.food_group:
        res.update({guess_ingr.name: YELLOW})
    else:
        res.update({guess_ingr.name: RED})
        
    print(f'\tIngredient: {res}')
    return res


def calorie_hint(answer: Dishes, guess_dish: Dishes):
    """ If guess has more cals than answer 
        a negative number is returned
        If guess has fewer cals than answer
        a positive number is returned
    """
    res = {'Calories': answer.calories - guess_dish.calories}
    print(f'\tCalories: {res}')
    return res


def taste_hint (answer: Taste, guess_dish: Taste):
    res = {}
    ans_dict = answer.__dict__
    guess_dict = guess_dish.__dict__
    
    for k, v in guess_dict.items():
        # NEEDS to be nested if-then-else to work!!!
        if v == True: 
            if ans_dict.get(k) == True:
                res.update({k: GREEN})
            else:
                res.update({k: RED})
    print("\tTaste: "+ str(res))
    return res


def get_hints(guess_str: str):
    guess = get_dish_by_name(guess_str)
    
    if guess == None:
        # TODO: how do I handle this?
        print("You guessed a dish that doesn't exist!!")
        return list()
    
    ans = get_puzzle_of_day()
    # print(ans.name)
    country_dict = country_hint(ans.country, guess.country)
    taste_dict = taste_hint(ans.taste, guess.taste)
    calorie_dict = calorie_hint(ans, guess)
    ingr_dict = main_ingredient_hint(ans.main_ingredient, guess.main_ingredient)
    
    return [country_dict, taste_dict, calorie_dict, ingr_dict]