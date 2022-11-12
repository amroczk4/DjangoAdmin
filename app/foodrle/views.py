from django.shortcuts import render, redirect
from .forms import NewUserForm, GuessAnswerForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .models import User, Dishes, Puzzle
import foodrle.game as game
from datetime import datetime
from random import choice


def homepage(request):
    # answer = get_puzzle_of_day().ans_dish.name
    # dishes = Dishes.objects.values_list('name', flat=True)
    # guess_sim = choice(dishes)
    user = request.user
    response = render(request=request, template_name='foodrle/home.html') # , context={"dishes":dishes}
    user_stats = game.get_game_stats(user)
    for k, v in user_stats.items():
        response.set_cookie(k, str(v), max_age=120)
    return response


def create_puzzle(request):
    user = request.user
    answer = game.create_puzzle_answer(user)
    guess_cnt = 0
    stats = game.get_game_stats(user)
    return redirect(f'/puzzles/{answer.id}/{guess_cnt}', context={"answer":answer.ans_dish.name, "player_stats": stats})
    # return render(request=request, template_name='foodrle/home.html', context={"dishes":dishes, "guess": guess_sim, "answer": answer, "hints": hints}) 


def get_puzzle(request, id, guess_cnt):
    # print(request.user) #TODO: user is null is possible
    if guess_cnt < 0 or guess_cnt > 6:
        return render(
            request=request, 
            template_name='foodrle/lose.html',
            context={ 
                "guess": 'GAME OVER', 
                "answer": "CHEATER!!!", 
                "hints_list": [], 
                })

    answer = Puzzle.objects.get(pk=id).ans_dish
    dishes = Dishes.objects.values_list('name', flat=True)
    guess_str = ''
    if request.method == "POST":
        form = GuessAnswerForm(request.POST)    
        if form.is_valid():
            guess_str = form.cleaned_data.get('dish_name').lower()
            if game.guess_is_valid_dish(guess_str):
                guess_cnt = game.find_guess_cnt(id, guess_cnt+1)
                if game.submit_guess(id, guess_str, guess_cnt):
                    return display_hints(request, id, guess_cnt)
        messages.error(request, "Invalid dish, guess again")
    form = GuessAnswerForm()
    if guess_cnt > 0:
        hints_list = game.get_hints(Puzzle.objects.get(pk=id), guess_cnt)
    else:
        hints_list = []
    response = render(
        request=request, template_name='foodrle/puzzle.html', 
        context={
            "dishes":dishes, 
            "guess": guess_str, 
            "answer": answer.name, 
            "hints_list": hints_list, 
            "form": form,
            })
    user_stats = game.get_game_stats(request.user)
    for k, v in user_stats.items():
        response.set_cookie(k, str(v), max_age=120)
    return response


def display_hints(request, id, guess_cnt):
    if guess_cnt <= 0 or guess_cnt > 6:
        response = render(
            request=request, 
            template_name='foodrle/lose.html',
            context={ 
                "guess": 'GAME OVER', 
                "answer": 'CHEATER!!!', 
                "hints_list": [], 
                })
    
    puzzle = Puzzle.objects.get(pk=id)
    win = game.is_guess_correct(puzzle, guess_cnt)
    hints_list = game.get_hints(puzzle, guess_cnt)
    if win:
        Puzzle.objects.filter(pk=id).update(is_win=win)
        response = render(
            request=request, 
            template_name='foodrle/win.html',
            context={ 
                "guess": 'WIN!!!', 
                "answer": puzzle.ans_dish.name, 
                "hints_list": hints_list, 
                })
        user_stats = game.get_game_stats(request.user)
        for k, v in user_stats.items():
            response.set_cookie(k, v, max_age=120)        
        
    
    elif guess_cnt == 6 and not win:
        response = render(
            request=request, 
            template_name='foodrle/lose.html',
            context={
                "guess": 'LOSE :(', 
                "answer": puzzle.ans_dish.name, 
                "hints_list": hints_list, 
                })
        user_stats = game.get_game_stats(request.user)
        for k, v in user_stats.items():
            response.set_cookie(k, str(v), max_age=120)
            
    else:
        dishes = Dishes.objects.values_list('name', flat=True)
        response = redirect(
            f'/puzzles/{id}/{guess_cnt}',
            context={
                "dishes":dishes, 
                "guess": 'foo', 
                "answer": puzzle.ans_dish.name, 
                "hints_list": hints_list,
                "form": GuessAnswerForm(),
                })
    
    return response


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Registration successful. Welcome {user.username}")
            return redirect("foodrle:homepage")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(
        request=request, template_name="foodrle/register.html", 
        context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("foodrle:homepage")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="foodrle/login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("foodrle:homepage")
