# Generated by Django 4.0.4 on 2022-06-11 08:27

from django.db import migrations, models
import scraping.models


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0003_url'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vacancy',
            options={'ordering': ['-timestamp'], 'verbose_name': 'Вакансия', 'verbose_name_plural': 'Вакансии'},
        ),
        migrations.AlterField(
            model_name='url',
            name='data',
            field=models.JSONField(default=scraping.models.default_urls),
        ),
    ]
