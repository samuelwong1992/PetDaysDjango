# Generated by Django 3.2.4 on 2022-06-09 03:31

import PetDays.core.image_helpers
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_pet_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='profile_picture',
            field=models.ImageField(blank=True, upload_to=PetDays.core.image_helpers.images_filename_generator),
        ),
    ]
