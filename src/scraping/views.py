from django.core.paginator import Paginator
from django.shortcuts import render

from .models import *
from .forms import *


def home_view(request):
    form = FindForm()
    return render(request, 'scraping/home.html', {'form': form})


def list_view(request):
    form = FindForm()
    qs = []
    page_obj = []
    params = {}
    city = request.GET.get('city', '')
    language = request.GET.get('language', '')
    if city or language:
        _filter = {}
        if city:
            _filter['city__slug'] = city
        if language:
            _filter['language__slug'] = language
        qs = Vacancy.objects.filter(**_filter)

        paginator = Paginator(qs, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        params = f'city={city}&language={language}&'

    return render(request, 'scraping/list_view.html', {'object_list': page_obj, 'form': form, 'params': params})