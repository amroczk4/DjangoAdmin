# import imp
from django.shortcuts import render, redirect
from .forms import NewUserForm, GuessAnswerForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .models import Dishes, Puzzle
import foodrle.game as game
from random import choice


def homepage(request):
    # answer = get_puzzle_of_day().ans_dish.name
    dishes = Dishes.objects.values_list('name', flat=True)
    # guess_sim = choice(dishes)
    return render(request=request, template_name='foodrle/home.html', context={"dishes":dishes})


def create_puzzle(request):
    answer = game.create_puzzle_answer()
    guess_cnt = 0
    return redirect(f'/puzzles/{answer.id}/{guess_cnt}',context={"answer":answer.ans_dish.name})
    # return render(request=request, template_name='foodrle/home.html', context={"dishes":dishes, "guess": guess_sim, "answer": answer, "hints": hints}) 


def get_puzzle(request, id, guess_cnt):
    if guess_cnt < 0 or guess_cnt >= 6:
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
    guess_str = 'INVALID'
    if request.method == "POST":
        form = GuessAnswerForm(request.POST)
        if form.is_valid():
            guess_str = form.cleaned_data.get('dish_name').lower()
            if game.guess_is_valid_dish(guess_str):
                guess_cnt = guess_cnt + 1
                game.submit_guess(id, guess_str, guess_cnt)
                return display_hints(request, id, guess_cnt)
        messages.error(request, "Invalid dish, guess again")
    form = GuessAnswerForm()
    if guess_cnt > 0:
        hints_list = game.get_hints(Puzzle.objects.get(pk=id), guess_cnt)
    else:
        hints_list = []
    return render(
        request=request, template_name='foodrle/puzzle.html', 
        context={
            "dishes":dishes, 
            "guess": guess_str, 
            "answer": answer.name, 
            "hints_list": hints_list, 
            "form": form,
            })


def display_hints(request, id, guess_cnt):
    if guess_cnt <= 0 or guess_cnt > 6:
        return render(
            request=request, 
            template_name='foodrle/lose.html',
            context={ 
                "guess": 'GAME OVER', 
                "answer": 'CHEATER!!!', 
                "hints_list": [], 
                })
    
    answer = Puzzle.objects.get(pk=id)
    win = game.is_guess_correct(answer, guess_cnt)
    hints_list = game.get_hints(answer, guess_cnt)
    if win:
        return render(
            request=request, 
            template_name='foodrle/win.html',
            context={ 
                "guess": 'WIN!!!', 
                "answer": answer.ans_dish.name, 
                "hints_list": hints_list, 
                })
    
    elif guess_cnt == 6 and not win:
        return render(
            request=request, 
            template_name='foodrle/lose.html',
            context={
                "guess": 'LOSE :(', 
                "answer": answer.ans_dish.name, 
                "hints_list": hints_list, 
                })
            
    else:
        dishes = Dishes.objects.values_list('name', flat=True)
        return redirect(
            f'/puzzles/{id}/{guess_cnt}',
            context={
                "dishes":dishes, 
                "guess": 'foo', 
                "answer": answer.ans_dish.name, 
                "hints_list": hints_list,
                "form": GuessAnswerForm(),
                })


## Testing page
## Test all functions here (TODO: remove before merge)
# def test(request):
#     answer = Puzzle.objects.get(pk=1).ans_dish
#     dishes = Dishes.objects.values_list('name', flat=True)
#     guess_sim = choice(dishes)
#     hints = game.collect_hints(game.get_dish_by_name(guess_sim), answer)
#     if request.method == "POST":
#         print(request.POST)
#         form = GuessAnswerForm(request.POST)
#         if form.is_valid():
#             guess_str = form.cleaned_data.get('dish_name')
#             print(guess_str)
#             # test valid dish ? return hint : idk
#             if game.guess_is_valid_dish(guess_str):
#                 guess_dish = game.get_dish_by_name(guess_str)
#                 hints = game.collect_hints(guess_dish, answer)
#                 messages.success(request, "guess went through!")
#                 return render(request=request, template_name='foodrle/test.html', context={"dishes":dishes, "guess": guess_str, "answer": answer.name, "hints": hints, "form": form})
#             else:
#                 messages.error(request, "Invalid dish, guess again")
#         else:
#             messages.error(request, "Bad Form!")
#     form = GuessAnswerForm()    
#     return render(
#         request=request, template_name='foodrle/test.html', 
#         context={
#             "dishes":dishes, "guess": guess_sim, "answer": answer.name, 
#             "hints": hints, "form": form})


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
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
