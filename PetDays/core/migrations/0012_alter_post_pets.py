# Generated by Django 3.2.4 on 2022-06-22 03:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_remove_post_daycare'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='pets',
            field=models.ManyToManyField(blank=True, null=True, to='core.Pet'),
        ),
    ]
