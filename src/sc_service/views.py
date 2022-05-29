from django.shortcuts import render
import datetime


def home(request):
    time_now = datetime.datetime.now().date()
    name = 'Every'
    context = {'time': time_now, 'name': name}
    return render(request, 'home.html', context=context)