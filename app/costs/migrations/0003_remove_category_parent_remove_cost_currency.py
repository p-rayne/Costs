# Generated by Django 4.1 on 2023-03-23 08:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('costs', '0002_cost_currency'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='cost',
            name='currency',
        ),
    ]