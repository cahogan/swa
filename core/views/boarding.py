from django.shortcuts import render, redirect
from core.models import Ticket


def boarding(request):
    context = {}
    return render(request, "core/boarding.html", context)
