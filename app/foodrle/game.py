from random import choice
from .models import Country, Dishes, Taste, MainIngredient, Puzzle
from math import atan2, degrees, sin, cos, radians, asin, sqrt

RED = 0
YELLOW = 1
GREEN = 2

   
def create_puzzle_answer() -> Puzzle:
    """ Chooses a random dish to serve as the
        user puzzle, creates a puzzle entry
        and returns it
    """
    answer = choice(Dishes.objects.all())
    puzzle = Puzzle(ans_dish=answer)
    puzzle.save()
    return puzzle


def find_guess_cnt(id: int, guess_cnt: int) -> int:
    """ return the guess number for the 
        first empty guess value (protect against user changing url)
    """
    puzzle = Puzzle.objects.get(pk=id)
    guess_dict = puzzle.get_guesses_as_dict()
    print('checking guess_cnt')
    if guess_can_be_made(puzzle, guess_cnt):
        return guess_cnt
    
    else:
        for i in range(1,7):
            if guess_dict.get(f'guess{i}') == '':
                guess_cnt = i
                break
        return guess_cnt


def submit_guess(puzzle_id: int, guess_str: str, guess_no: int) -> bool:
    puzzle = Puzzle.objects.get(pk=puzzle_id)
    if guess_no not in range(1,7):
        print("submit_guess: game over")
        return False
    if not guess_is_valid_dish(guess_str):
        print("submit_guess: invalid guess!")
        return False
    elif guess_is_unique(puzzle, guess_str) and guess_can_be_made(puzzle, guess_no):
        guess_dict = {f'guess{guess_no}': guess_str}
        Puzzle.objects.filter(pk=puzzle_id).update(**guess_dict)
        # print(f'submit_guess: {guess_dict} add successful!')
        return True
    else:
        return False


def guess_is_unique(puzzle: Puzzle, guess_str: str) -> bool:
    guess_dict = puzzle.get_guesses_as_dict()
    
    for k, v in guess_dict.items():
        if guess_str == v:
            return False
    
    return True
    

def guess_can_be_made(puzzle: Puzzle, guess_cnt: int) -> bool:
    guess_dict = puzzle.get_guesses_as_dict()
    
    # Check all prev guesses
    for i in range(1, guess_cnt):
        guess = guess_dict.get(f"guess{i}")
        if guess == '':
            print("a previous guess was not entered")
            return False
            
    # Check current guess
    # Check future guesses
    for i in range(guess_cnt, 7):
        guess = guess_dict.get(f'guess{i}')
        if guess != '':
            print("current or future guesses have been made")
            return False
            
    # safe to enter the guess
    return True


def get_dish_by_name(dish_name: str):
    """ SELECT * FROM Dishes WHERE name=dish_name
        Returns None if dish_name represents a non-existent dish
    """
    try:
        return Dishes.objects.get(name=dish_name)
    except Dishes.DoesNotExist:
        return None


def guess_is_valid_dish(guess_str: str) -> bool:
    if get_dish_by_name(guess_str) == None:
        return False
    else:
        return True

        
def distance(guessed_country: Country, answer_country: Country) -> int:
    """ Computes the distance in miles
        between guessed_country and answer_country
    """
    if guessed_country.name == answer_country.name:
        return 0

    start_lat, start_lon, dest_lat, dest_lon = map(radians,
                                                    [guessed_country.latitude, 
                                                    guessed_country.longitude, 
                                                    answer_country.latitude, 
                                                    answer_country.longitude])
    # Haversine formula
    dlon = start_lon - dest_lon
    dlat = start_lat - dest_lat
    a = sin(dlat / 2) ** 2 + cos(start_lat) * cos(dest_lat) * sin(dlon / 2) ** 2

    c = 2 * asin(sqrt(a))

    return round(c * 3956)


def direction(guessed_country: Country, answer_country: Country) -> str:
        """
        Computes the direction of 'other' in relation to 'self'
        if the countries are within 'delta' degrees of latitude and
        longitude of one another bearing is used to compute
        direction instead
        """
        if guessed_country.name == answer_country.name:
            return 'same'
        
        dlat = guessed_country.latitude - answer_country.latitude
        dlon = guessed_country.longitude - answer_country.longitude
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
            return bearing(guessed_country, answer_country)

        return north_or_south + east_or_west


def bearing(guessed_country: Country, answer_country: Country) -> str:
    """ Serving as a backup to direction function,
        computes the bearing angle between
        two countries and returns a direction string
    """
    
    dest_lon = answer_country.longitude
    dest_lat = answer_country.latitude
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
        'dist': str(distance(guessed_country, answer_country))+' Mi',
        'dir': direction(guessed_country, answer_country)
        }
    
    # print(f'\tCountry: {res}')
    return res


def main_ingredient_hint(answer: MainIngredient, guess_ingr: MainIngredient):
    res = {}
    if answer.id == guess_ingr.id:
        res.update({guess_ingr.name: GREEN})
    elif answer.food_group == guess_ingr.food_group:
        res.update({guess_ingr.name: YELLOW})
    else:
        res.update({guess_ingr.name: RED})
        
    # print(f'\tIngredient: {res}')
    return res


def calorie_hint(answer: Dishes, guess_dish: Dishes):
    """ If guess has more cals than answer 
        a negative number is returned
        If guess has fewer cals than answer
        a positive number is returned
    """
    diff = answer.calories - guess_dish.calories
    res = {'calories': diff}
    # print(f'\tCalories: {res}')
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
    if len(res) < 3:
        res.update({'placeholder': ''})
    # print("\tTaste: "+ str(res))
    return res


def is_guess_correct(puzzle: Puzzle, guess_cnt: int) -> bool:
    answer = puzzle.ans_dish.name
    guess_dict = puzzle.get_guesses_as_dict()
    current_guess = guess_dict.get(f'guess{guess_cnt}')
    return current_guess == answer


def collect_hints(guess_dish: Dishes, answer_dish: Dishes):
    
    guess_dict = {'guess': guess_dish.name}
    country_dict = country_hint(answer_dish.country, guess_dish.country)
    taste_dict = taste_hint(answer_dish.taste, guess_dish.taste)
    calorie_dict = calorie_hint(answer_dish, guess_dish)
    ingr_dict = main_ingredient_hint(answer_dish.main_ingredient, guess_dish.main_ingredient)
    
    return [guess_dict, country_dict, taste_dict, calorie_dict, ingr_dict]


def get_hints(puzzle: Puzzle, guess_cnt: int):
    if guess_cnt not in range(1,7):
        return []
    guess_dict = puzzle.get_guesses_as_dict()
    answer = puzzle.ans_dish
    hints_list = []
    for i in range(1, guess_cnt+1):
        guess_n = guess_dict.get(f'guess{i}')
        if guess_n == '':
            break
        dish_n = get_dish_by_name(guess_n)
        hint_n = collect_hints(dish_n, answer)
        hints_list.append(hint_n)
    
    return hints_list

