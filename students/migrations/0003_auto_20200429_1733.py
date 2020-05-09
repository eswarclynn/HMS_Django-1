# Generated by Django 3.0.5 on 2020-04-29 12:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('institute', '0004_auto_20200429_1304'),
        ('students', '0002_auto_20200429_1726'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='id',
        ),
        migrations.RemoveField(
            model_name='details',
            name='id',
        ),
        migrations.AlterField(
            model_name='attendance',
            name='regd_no',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='institute.Institutestd'),
        ),
        migrations.AlterField(
            model_name='details',
            name='regd_no',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='institute.Institutestd'),
        ),
    ]
