# Generated by Django 3.0.5 on 2020-04-29 21:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0006_remove_outing_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attendance',
            old_name='date',
            new_name='dates',
        ),
    ]
