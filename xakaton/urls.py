from django.urls import path, include

from xakaton.views import aboutproject, xaki, registcommand, aboutmirea, aboutcommand, teamaccept, createteam

app_name = 'xakaton'




urlpatterns = [
    path('aboutproject/', aboutproject, name='aboutproject'),
    path('', xaki, name='xaki'),
    path('registcommand', registcommand, name='registcommand'),
    path('aboutmirea', aboutmirea, name='aboutmirea'),
    path('aboutcommand', aboutcommand, name='aboutcommand'),
    path('teamaccept', teamaccept, name='teamaccept'),
    path('createteam', createteam, name='createteam'),





]