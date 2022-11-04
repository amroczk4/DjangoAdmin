# import imp
from django.shortcuts import render, redirect
from .forms import NewUserForm, GuessAnswerForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .models import Dishes, Puzzle
from .game import create_puzzle_answer, get_hints, guess_is_valid_dish
from random import choice
# from .shellgame import get_puzzle as random_dish

def homepage(request):
    # answer = get_puzzle_of_day().ans_dish.name
    dishes = Dishes.objects.values_list('name', flat=True)
    # guess_sim = choice(dishes)
    return render(request=request, template_name='foodrle/home.html', context={"dishes":dishes})


def create_puzzle(request):
    answer = create_puzzle_answer()
    # Create new puzzle record
    return redirect(f'/puzzles/{answer.id}',context={"answer":answer.ans_dish.name})
    #return render(request=request, template_name='foodrle/home.html', context={"dishes":dishes, "guess": guess_sim, "answer": answer, "hints": hints}) 


def get_puzzle(request, id):
    # ORIGINAL
    # answer = Puzzle.objects.get(pk=id).ans_dish
    # dishes = Dishes.objects.values_list('name', flat=True)
    # guess_sim = choice(dishes)
    # #TODO: submit_guess(guess_sim)
    # hints = get_hints(guess_sim, answer)
    # return render(request=request, template_name='foodrle/puzzle.html', context={"dishes":dishes, "guess": guess_sim, "answer": answer.name, "hints": hints})

    answer = Puzzle.objects.get(pk=1).ans_dish
    dishes = Dishes.objects.values_list('name', flat=True)
    guess_sim = choice(dishes)
    hints = get_hints(guess_sim, answer)
    if request.method == "POST":
        print(request.POST)
        form = GuessAnswerForm(request.POST)
        if form.is_valid():
            guess = form.cleaned_data.get('dish_name')
            print(guess)
            if guess_is_valid_dish(guess):
                hints = get_hints(guess, answer)
                messages.success(request, "guess went through!")
                return render(request=request, template_name='foodrle/puzzle.html', context={"dishes":dishes, "guess": guess, "answer": answer.name, "hints": hints, "form": form})
            else:
                messages.error(request, "Invalid dish, guess again")
        else:
            messages.error(request, "Bad Form!")
    form = GuessAnswerForm()    
    return render(request=request, template_name='foodrle/puzzle.html', context={"dishes":dishes, "guess": guess_sim, "answer": answer.name, "hints": hints, "form": form})

#create new function to take input, send to server, pass the id of the puzzle, create logic to respond to guess

## Testing page
## Test all functions here 
def test(request):
    answer = Puzzle.objects.get(pk=1).ans_dish
    dishes = Dishes.objects.values_list('name', flat=True)
    guess_sim = choice(dishes)
    hints = get_hints(guess_sim, answer)
    if request.method == "POST":
        print(request.POST)
        form = GuessAnswerForm(request.POST)
        if form.is_valid():
            guess = form.cleaned_data.get('dish_name')
            print(guess)
            # test valid dish ? return hint : idk
            if guess_is_valid_dish(guess):
                hints = get_hints(guess, answer)
                messages.success(request, "guess went through!")
                return render(request=request, template_name='foodrle/test.html', context={"dishes":dishes, "guess": guess, "answer": answer.name, "hints": hints, "form": form})
            else:
                messages.error(request, "Invalid dish, guess again")
        else:
            messages.error(request, "Bad Form!")
    form = GuessAnswerForm()    
    return render(request=request, template_name='foodrle/test.html', context={"dishes":dishes, "guess": guess_sim, "answer": answer.name, "hints": hints, "form": form})

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
    return render(request=request, template_name="foodrle/register.html", context={"register_form": form})


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
