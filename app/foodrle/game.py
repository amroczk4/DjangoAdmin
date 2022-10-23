from random import randint
from .models import Country, Dishes, Taste, MainIngredient, Puzzle
from math import atan2, degrees, sin, cos, radians, asin, sqrt
import os
import datetime

TOTAL_PUZZLES = 33
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


def get_dish_by_name(dish_name) -> Dishes:
    return Dishes.objects.get(name=dish_name)


def play_again() -> bool:
    answer = input('Would you like to play again [y/N]: ').lower()
    return answer == 'y'


def distance(guessed_country: Country, answer: Country, unit='mi'):
    """ Computes the distance ('mi' miles (default), or
        'km' kilometers) between one country and another
    """
    if guessed_country.name == answer.name:
        return 0

    start_lat, start_lon, dest_lat, dest_lon = map(radians,
                                                    [guessed_country.latitude, guessed_country.longitude, answer.latitude, answer.longitude])
    # Haversine formula
    dlon = start_lon - dest_lon
    dlat = start_lat - dest_lat
    a = sin(dlat / 2) ** 2 + cos(start_lat) * cos(dest_lat) * sin(dlon / 2) ** 2

    c = 2 * asin(sqrt(a))

    # Radius of earth in kilometers is 6371. Use 3956 for miles
    if unit == 'mi':
        # print(f"Distance from {self.name} to {other.name} is {c * 3956} mi")
        return c * 3956
    else:
        # print(f"Distance from {self.name} to {other.name} is {c * 6371} km")
        return c * 6371


def direction(guessed_country: Country, answer: Country):
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
            return bearing(guessed_country, answer)
        # print(f"{other.name} is {north_or_south + east_or_west} of {self.name}")
        return north_or_south + east_or_west


def bearing(guessed_country: Country, answer: Country):
    dest_lon = answer.longitude
    dest_lat = answer.latitude
    start_lat = guessed_country.latitude
    start_lon = guessed_country.longitude

    #
    def card_ord_dir(brng):
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
    brng = atan2(y, x);
    brng = degrees(brng);
    if brng < 0:
        brng = brng + 360

    # print(f'bearing is {brng}')
    return card_ord_dir(brng)


def country_hint(answer_country: Country, guessed_country: Country):
    cntry_hint = str(distance(guessed_country, answer_country)) + ' miles'
    cntry_hint = cntry_hint + ' ' + direction(guessed_country, answer_country)
    print('\tFrom a country', cntry_hint, f'of {guessed_country}')


def same_name(ingredient_a, ingredient_b):
    return ingredient_a.name == ingredient_b.name


def food_group_eq(ingredient_a, ingredient_b):
    return ingredient_a.food_group == ingredient_b.food_group


def main_ingredient_hint(answer: MainIngredient, guess_ingr: MainIngredient):
    if same_name(answer, guess_ingr):
        print(f'\tCORRECT main ingredient: {answer.name}')
    elif food_group_eq(guess_ingr, answer):
        print(f'\tWRONG main ingredient: {guess_ingr.name}; CORRECT food group')
    else:
        print(f'\tWRONG main ingredient: {guess_ingr.name}; WRONG food group')


def reveal_main_ingredient(answer: MainIngredient):
    print(f"\t[BIG HINT] The main ingredient in the Answer is: {answer.name}")


def calorie_hint(answer: Dishes, guess_dish: Dishes):
    diff = guess_dish.calories - answer.calories
    if diff > 0:
        print(f'\t{diff} calories more than {guess_dish.name}')
    else:
        print(f'\t{abs(diff)} calories less than {guess_dish.name}')


def taste_hint(answer: Taste, guess_dish: Taste):
    taste_res = ''

    if guess_dish.sweet:
        if not answer.sweet:
            taste_res = taste_res + 'NOT '
        taste_res = taste_res + 'sweet; '
    if guess_dish.salty:
        if not answer.salty:
            taste_res = taste_res + 'NOT '
        taste_res = taste_res + 'salty; '
    if guess_dish.sour:
        if not answer.sour:
            taste_res = taste_res + 'NOT '
        taste_res = taste_res + 'sour; '
    if guess_dish.bitter:
        if not answer.bitter:
            taste_res = taste_res + 'NOT '
        taste_res = taste_res + 'bitter; '
    if guess_dish.umami:
        if not answer.umami:
            taste_res = taste_res + 'NOT '
        taste_res = taste_res + 'umami; '
    print('\t'+taste_res)


def start_game():
    print_welcome()
    # answer = get_dish_by_name('fries')
    # answer = get_puzzle()
    answer = Puzzle.objects.get(pk=17).dish
    guess_cnt = 0
    win = False
    while guess_cnt < 6:
        guess_str = input(f'Enter Guess {guess_cnt + 1}: ').lower()

        try:
            guess_dish = get_dish_by_name(guess_str)
        except Dishes.DoesNotExist:
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
            # if guess_cnt >= 4:
            #     print("\tI am displaying a pixilated image of the answer")

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
