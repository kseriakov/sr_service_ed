from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, ListView, CreateView, UpdateView
from datetime import datetime, timedelta

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


class VacDetail(DetailView):
    template_name = 'scraping/detail.html'
    pk_url_kwarg = 'pk_v'
    context_object_name = 'vacancy'

    def get_queryset(self):
        vacancies = Vacancy.objects.filter(timestamp__gte=datetime.today() - timedelta(3))
        return vacancies

    def get_object(self, queryset=None):
        vacancy = super(VacDetail, self).get_object(queryset=None)
        user_language = self.request.user.language.name
        vacancy_language = vacancy.language.name
        if user_language != vacancy_language:
            raise Http404('Вакансия не найдена')
        return vacancy


class VacListView(ListView):
    template_name = 'scraping/list_view.html'
    context_object_name = 'object_list'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(VacListView, self).get_context_data(**kwargs)
        context['city'] = self.request.GET.get('city', '')
        context['language'] = self.request.GET.get('language', '')
        context['params'] = f'city={context["city"]}&language={context["language"]}&'
        context['form'] = FindForm()
        return context

    def get_queryset(self):
        city = self.request.GET.get('city', '')
        language = self.request.GET.get('language', '')
        qs = []
        if city or language:
            _filter = {}
            if city:
                _filter['city__slug'] = city
            if language:
                _filter['language__slug'] = language
            qs = Vacancy.objects.filter(**_filter)
        return qs


class VacCreate(CreateView):
    template_name = 'scraping/create.html'
    model = Vacancy
    fields = '__all__'
    success_url = reverse_lazy('home')


class VacUpdate(UpdateView):
    template_name = 'scraping/create.html'
    model = Vacancy
    form_class = VacUpdateForm
    success_url = reverse_lazy('home')