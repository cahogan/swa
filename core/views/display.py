from django.shortcuts import render


def display(request):
    context = {}
    return render(request, "core/display.html", context)
