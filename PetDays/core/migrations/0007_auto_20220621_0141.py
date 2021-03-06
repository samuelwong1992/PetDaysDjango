# Generated by Django 3.2.4 on 2022-06-21 01:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_profile_profile_picture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pet',
            name='daycares',
        ),
        migrations.CreateModel(
            name='PetDaycareRelationship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_approved', models.BooleanField(default=False)),
                ('daycare', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.daycare')),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.pet')),
            ],
        ),
    ]
