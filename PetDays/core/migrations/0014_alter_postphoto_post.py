# Generated by Django 3.2.4 on 2022-06-22 04:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_alter_post_pets'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postphoto',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_photos', to='core.post'),
        ),
    ]
