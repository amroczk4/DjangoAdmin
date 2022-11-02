from random import randint
from .models import Country, Dishes, Taste, MainIngredient, Puzzle
from math import atan2, degrees, sin, cos, radians, asin, sqrt
import os

TOTAL_PUZZLES = Puzzle.objects.count()
RED = 0
YELLOW = 1
GREEN = 2

user_stats = {
    1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 'games_played': 0
}


def cls():
    os.system('cls' if os.name=='nt' else 'clear')


def main():
    cls()
    start_game()


if __name__ == '__main__':
    main()


def update_user_stats(guess_cnt: int, isWin: bool):
    if isWin:
        cnt = user_stats.get(guess_cnt)
        if cnt is None:
            user_stats.update({guess_cnt: 1})
        else:
            user_stats.update({guess_cnt: cnt + 1})
    played_games = user_stats.get('games_played')
    if played_games is None:
        user_stats.update({'games_played': 1})
    else:
        user_stats.update({'games_played': played_games + 1})

    show_user_stats()
    return


def show_user_stats():
    print(user_stats)


def print_welcome():
    print("Welcome to Foodrle:")
    print("\tYou have 6 guesses to Determine the right food")
    print("\tYour game starts now")


def get_puzzle() -> Dishes:
    """
    Selects a random puzzle from the database,
    updates last used date and returns dish
    """
    puzzle = Puzzle.objects.get(pk=randint(1, TOTAL_PUZZLES))
    puzzle.update_last_used()
    return puzzle.dish


def get_dish_by_name(dish_name: str):
    try:
        return Dishes.objects.get(name=dish_name)
    except Dishes.DoesNotExist:
        return None

def play_again() -> bool:
    answer = input('Would you like to play again [y/N]: ').lower()
    return answer == 'y'


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


def bearing(guessed_country: Country, answer: Country):
    dest_lon = answer.longitude
    dest_lat = answer.latitude
    start_lat = guessed_country.latitude
    start_lon = guessed_country.longitude

    start_lat, start_lon, dest_lat, dest_lon = map(radians,
                                                    [guessed_country.latitude, guessed_country.longitude, answer.latitude, answer.longitude])

    y = sin(dest_lon - start_lon) * cos(dest_lat)
    x = cos(start_lat) * sin(dest_lat) - sin(start_lat) * cos(dest_lat) * cos(dest_lon - start_lon)


def country_hint(answer_country: Country, guessed_country: Country):
    res = {
        'country': guessed_country.name, 
        'dist': distance(guessed_country, answer_country),
        'dir': direction(guessed_country, answer_country)
        }
    
    print(f'\tCountry: {res}')
    return res


def ingredient_eq(ingredient_a, ingredient_b) -> bool:
    return ingredient_a.name == ingredient_b.name


def food_group_eq(ingredient_a, ingredient_b) -> bool:
    return ingredient_a.food_group == ingredient_b.food_group


def main_ingredient_hint(answer: MainIngredient, guess_ingr: MainIngredient):
    res = {guess_ingr.name: RED}
    if ingredient_eq(answer, guess_ingr):
        res.update({guess_ingr.name: GREEN})
    elif food_group_eq(guess_ingr, answer):
        res.update({guess_ingr.name: YELLOW})
    else:
        res.update({guess_ingr.name: RED})
        
    print(f'\tIngredient: {res}')
    return res
    



def reveal_main_ingredient(answer: MainIngredient):
    print(f"\t[BIG HINT] The main ingredient in the Answer is: {answer.name}")


def calorie_hint(answer: Dishes, guess_dish: Dishes):
    diff = guess_dish.calories - answer.calories
    if diff >= 0:
        print('\tCalorie: '+ str({'+': diff}))
        return {'+': diff}
    else:
        print('\tCalorie: '+ str({'-': abs(diff)}))
        return {'-': abs(diff)}


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


def start_game():
    print_welcome()
    answer = get_dish_by_name('pizza')
    # answer = get_puzzle()
    
    guess_cnt = 0
    win = False
    while guess_cnt < 6:
        guess_str = input(f'Enter Guess {guess_cnt + 1}: ').lower()

        guess_dish = get_dish_by_name(guess_str)
        if guess_dish == None:
            print("Invalid answer: dish doesn\'t exist (yet)")
            continue

        if guess_dish.name == answer.name:
            print("congratulations, you win!")
            print(f'correct guess in {guess_cnt + 1} tries')
            win = True
        else:
            print("[Hints] The correct answer is: ")
            country_hint(answer.country, guess_dish.country)
            calorie_hint(answer, guess_dish)
            main_ingredient_hint(answer.main_ingredient, guess_dish.main_ingredient)
            taste_hint(answer.taste, guess_dish.taste)
            if guess_cnt >= 1:
                reveal_main_ingredient(answer.main_ingredient)

        guess_cnt = guess_cnt + 1
        if guess_cnt == 6 or win:
            print(f'The correct answer was: {answer.name}')
            update_user_stats(guess_cnt, win)
            if play_again():
                guess_cnt = 0
                win = False
                answer = get_puzzle()
            else:
                break

    if guess_cnt == 6 and not win:
        print('Better luck next time!')
    else:
        print('Way to go!')

    show_user_stats()
