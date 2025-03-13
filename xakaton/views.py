from django.shortcuts import render

def xaki(request):
    return render(request, 'xakaton/xaki.html')

def aboutproject(request):
    return render(request, 'xakaton/aboutproject.html')

def registcommand(request):
    return render(request, 'xakaton/registcommand.html')

def aboutmirea(request):
    return render(request, 'xakaton/aboutmirea.html')

def aboutcommand(request):
    return render(request, 'xakaton/aboutcommand.html')

def teamaccept(request):
    return render(request, 'xakaton/teamaccept.html')

def createteam(request):
    return render(request, 'xakaton/createteam.html')