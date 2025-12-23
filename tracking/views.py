from django.shortcuts import render


def goto_home(request):
    return render(request, "home.html")
