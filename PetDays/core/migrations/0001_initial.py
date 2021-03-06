# Generated by Django 3.2.4 on 2022-05-31 07:53

import PetDays.core.image_helpers
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Daycare',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('profile_picture', models.ImageField(upload_to=PetDays.core.image_helpers.images_filename_generator)),
                ('daycare', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.daycare')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('profile_picture', models.ImageField(upload_to=PetDays.core.image_helpers.images_filename_generator)),
                ('daycares', models.ManyToManyField(to='core.Daycare')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time_created', models.DateTimeField(auto_now_add=True)),
                ('text', models.TextField()),
                ('daycare', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.daycare')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.employee')),
                ('pets', models.ManyToManyField(to='core.Pet')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_picture', models.ImageField(upload_to=PetDays.core.image_helpers.images_filename_generator)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PostPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_vin', models.BooleanField(default=False)),
                ('photo', models.ImageField(upload_to=PetDays.core.image_helpers.images_filename_generator)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.post')),
            ],
        ),
        migrations.AddField(
            model_name='pet',
            name='parents',
            field=models.ManyToManyField(to='core.Profile'),
        ),
    ]
