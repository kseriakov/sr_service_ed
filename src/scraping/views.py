from django.shortcuts import render

from .models import *
from .forms import *


def home_view(request):
    form = FindForm()
    qs = []
    city = request.GET.get('city')
    language = request.GET.get('language')
    print(city, language)
    if city or language:
        _filter = {}
        if city:
            _filter['city__slug'] = city
        if language:
            _filter['language__slug'] = language
        qs = Vacancy.objects.filter(**_filter)

    return render(request, 'scraping/home.html', {'object_list': qs, 'form': form})