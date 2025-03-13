from django.urls import path, include

from users.views import login, registration, profile, editprofile,changelogin,addmail,addmailcorrect,restorepassword

app_name = 'users'




urlpatterns = [
    path('login/', login, name='login'),
    path('registration/',registration , name='registration'),
    path('profile/',profile , name='profile'),
    path('changelogin/',changelogin , name='changelogin'),
    path('editprofile/',editprofile , name='editprofile'),
    path('addmail/',addmail , name='addmail'),
    path('addmailcorrect/',addmailcorrect , name='addmailcorrect'),
    path('restorepassword/',restorepassword , name='restorepassword'),



]
