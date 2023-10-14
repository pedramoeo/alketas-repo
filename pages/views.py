from django.shortcuts import render, redirect





def home(request):
    return render(request, 'home.html')


def projects(request):
    return render(request, "projects.html")
