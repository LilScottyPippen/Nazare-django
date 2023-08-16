# Generated by Django 4.2.4 on 2023-08-16 13:15

from django.db import migrations, models
import django.db.models.deletion
import index.models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0002_apartment_alter_callback_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='apartment',
            options={'verbose_name': 'Апартаменты', 'verbose_name_plural': 'Апартаменты'},
        ),
        migrations.CreateModel(
            name='ApartmentPhoto',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to=index.models.getImageUploadPath)),
                ('nameImage', models.CharField(max_length=50)),
                ('apartment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.apartment', verbose_name='Аппартамент')),
            ],
        ),
    ]
