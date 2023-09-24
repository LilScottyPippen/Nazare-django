# Generated by Django 2.2 on 2023-09-24 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0005_auto_20230924_1534'),
    ]

    operations = [
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название')),
                ('hourlyPrice', models.IntegerField(default=0, verbose_name='Часовая стоимость (BYN)')),
                ('slug', models.SlugField(default='slug', max_length=100, unique=True, verbose_name='Псевдоним (English)')),
            ],
            options={
                'verbose_name': 'Услуга',
                'verbose_name_plural': 'Услуги',
            },
        ),
    ]
