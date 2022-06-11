from django.contrib import admin

from .models import *


class VacancyAdmin(admin.ModelAdmin):
    list_display = ('id', "__str__", 'timestamp')
    list_display_links = ('id', "__str__",)


admin.site.register(City)
admin.site.register(Language)
admin.site.register(Vacancy, VacancyAdmin)
admin.site.register(Error)
admin.site.register(Url)
