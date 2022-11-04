from random import choice
from .models import Dishes, MainIngredient, Puzzle
import foodrle.game as game
import os


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
    Selects a random puzzle from 
    the database and returns dish
    """
    puzzles = Puzzle.objects.all()
    rand_puzzle = choice(puzzles)
    return rand_puzzle.ans_dish


def play_again() -> bool:
    answer = input('Would you like to play again [y/N]: ').lower()
    return answer == 'y'


def reveal_main_ingredient(answer: MainIngredient):
    print(f"\t[BIG HINT] The main ingredient in the Answer is: {answer.name}")


def start_game():
    print_welcome()
    # answer = game.get_dish_by_name('pizza')
    answer = get_puzzle()
    
    guess_cnt = 0
    win = False
    while guess_cnt < 6:
        guess_str = input(f'Enter Guess {guess_cnt + 1}: ').lower()

        guess_dish = game.get_dish_by_name(guess_str)
        if guess_dish == None:
            print("Invalid answer: dish doesn\'t exist (yet)")
            continue

        if guess_dish.name == answer.name:
            print("congratulations, you win!")
            print(f'correct guess in {guess_cnt + 1} tries')
            win = True
        else:
            print("[Hints] The correct answer is: ")
            game.country_hint(answer.country, guess_dish.country)
            game.calorie_hint(answer, guess_dish)
            game.main_ingredient_hint(answer.main_ingredient, guess_dish.main_ingredient)
            game.taste_hint(answer.taste, guess_dish.taste)
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
