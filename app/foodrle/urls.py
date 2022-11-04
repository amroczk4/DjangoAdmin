from django.urls import path
from . import views

app_name = "foodrle"


urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name="logout"),
    path("test",views.test, name="test"),
    path("puzzle/new",views.create_puzzle, name="newpuzzle"),
    path("puzzles/<int:id>",views.get_puzzle, name="getpuzzle"),
]

