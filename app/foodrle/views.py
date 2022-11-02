# import imp
from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .models import Dishes
from .game import get_puzzle_of_day, get_hints
from random import choice
# from .shellgame import get_puzzle as random_dish

def homepage(request):
    answer = get_puzzle_of_day().name
    dishes = Dishes.objects.values_list('name', flat=True)
    guess_sim = choice(dishes)
    hints = get_hints(guess_sim)
    return render(request=request, template_name='foodrle/home.html', context={"dishes":dishes, "guess": guess_sim, "answer": answer, "hints": hints})
    # return render(request=request, template_name='foodrle/home.html', context={"dishes":dishes})


## Testing page
## Test all functions here 
def test(request):
    answer = get_puzzle_of_day().name
    dishes = Dishes.objects.values_list('name', flat=True)
    guess_sim = choice(dishes)
    hints = get_hints(guess_sim)
    return render(request=request, template_name='foodrle/test.html', context={"dishes":dishes, "guess": guess_sim, "answer": answer, "hints": hints})

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
