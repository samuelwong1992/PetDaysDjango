# Generated by Django 3.2.4 on 2022-06-19 12:31

import PetDays.core.image_helpers
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_pet_daycares'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(blank=True, upload_to=PetDays.core.image_helpers.images_filename_generator),
        ),
    ]
