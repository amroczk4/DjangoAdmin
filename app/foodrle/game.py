from random import randint
from .models import Country, Dishes, Taste, MainIngredient
from django.core.exceptions import ObjectDoesNotExist
import os


TOTAL_PUZZLES = 32
user_stats = {
    1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 'games_played': 0
}


def cls():
    os.system('cls' if os.name=='nt' else 'clear')


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


def get_puzzle(id: int) -> Dishes:
    return Dishes.objects.get(pk=id)


def get_dish_by_name(dish_name) -> Dishes:
    return Dishes.objects.get(name=dish_name)


def play_again() -> bool:
    answer = input('Would you like to play again [y/N]: ').lower()
    return answer == 'y'


def country_hint(answer_country: Country, guessed_country: Country):
    cntry_hint = str(guessed_country.distance(answer_country)) + ' miles'
    cntry_hint = cntry_hint + ' ' + guessed_country.direction(answer_country)
    print('\tFrom a country', cntry_hint, f'of {guessed_country}')


def main_ingredient_hint(answer: Dishes, guess_dish: Dishes):
    guess_main_ingr = guess_dish.main_ingredient
    if answer.main_ingredient.same_name_same_group(guess_main_ingr):
        print(f'\tCORRECT main ingredient: {answer.main_ingredient}')
    elif guess_main_ingr.food_group_eq(answer.main_ingredient):
        print(f'\tWRONG main ingredient: {guess_main_ingr.name}: CORRECT food group')
    else:
        print(f'\tWRONG main ingredient: {guess_main_ingr.name}: WRONG food group')


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
    answer = get_puzzle(randint(1, TOTAL_PUZZLES))
    guess_cnt = 0
    win = False
    while guess_cnt < 6:
        guess_str = input(f'Enter Guess {guess_cnt + 1}: ').lower()

        # TODO: some manner of exception handling
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
            main_ingredient_hint(answer, guess_dish)
            taste_hint(answer.taste, guess_dish.taste)  # TODO
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
                answer = get_puzzle(randint(1, TOTAL_PUZZLES))
            else:
                break

    if guess_cnt == 6 and not win:
        print('Better luck next time!')
    else:
        print('Way to go!')

    show_user_stats()
