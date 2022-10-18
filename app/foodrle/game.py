from random import randint
from .models import Country, Dishes, Taste, MainIngredient

TOTAL_PUZZLES = 32

def print_welcome():
    print("Welcome to Foodrle:")
    print("\tYou have 6 guesses to Determine the right food")
    print("\tYour game starts now")


def get_dish(id):
    return Dishes.objects.get(pk=id)


def get_dish_by_name(dish_name):
    return Dishes.objects.get(name=dish_name)


def play_again():
    answer = input('Would you like to play again [y/N]: ').lower()
    return answer == 'y'


def get_country_hint(answer, guess_dish):
    guessed_country = guess_dish.country
    country_hint = str(guessed_country.distance(
                answer.country))
    country_hint = country_hint + ' ' + guessed_country.direction(
                answer.country
            )
    print(
        'answer is from a country',country_hint, 
        f'of {guessed_country.name}'
        )


def get_calory_hint(answer, guess_dish):
    diff = guess_dish.calories - answer.calories
    if diff > 0:
        print(f'{diff} calories higher than answer')
    else:
        print(f'{abs(diff)} calories lower than answer')


def start_game():
    print_welcome()
    answer = get_dish(randint(1, TOTAL_PUZZLES))
    guess_cnt = 0
    win = False
    while guess_cnt < 6:
        guess_str = input(f'Enter Guess {guess_cnt}: ').lower()

        # TODO: some manner of exception handling
        guess_dish = get_dish_by_name(guess_str)

        if guess_dish.name == answer.name:
            print("congratulations, you win!")
            print(f'correct guess in {guess_cnt} tries')
            win = True
        else:
            get_country_hint(answer, guess_dish)
            get_calory_hint(answer, guess_dish)
            #TODO: finish

        guess_cnt = guess_cnt + 1
        if guess_cnt == 6 or win:
            print(f'The correct answer was: {answer.name}')
            if play_again():
                guess_cnt = 0
                win = False
                answer = get_dish(randint(1, TOTAL_PUZZLES))
            else:
                break

    if guess_cnt == 6:
        print('Better luck next time!')
    else:
        print('Way to go!')

    # TODO show user stats    
    


