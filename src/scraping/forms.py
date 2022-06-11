from django import forms

from .models import *


class FindForm(forms.Form):
    city = forms.ModelChoiceField(queryset=City.objects.all(), to_field_name='slug', required=False,
                                  widget=forms.Select(attrs={'class': 'form-select'}), label='Город'
                                  )
    language = forms.ModelChoiceField(queryset=Language.objects.all(), to_field_name='slug', required=False,
                                      widget=forms.Select(attrs={'class': 'form-select'}), label='Язык'
                                      )


class VacUpdateForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = '__all__'
        widgets = {
            'city': forms.Select(attrs={'class': 'form-select'}),
            'language': forms.Select(attrs={'class': 'form-select'}),
            'url': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
         }

        labels = {
            'city': 'Город',
            'language': 'Язык',
            'company': 'Компания',
            'description': 'Описание вакансии',
            'title': 'Вакансия',

        }
