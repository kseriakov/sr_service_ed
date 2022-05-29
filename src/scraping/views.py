from django.shortcuts import render

from .models import *


def home_view(request):
    qs = Vacancy.objects.all()
    return render(request, 'home.html', {'object_list': qs})