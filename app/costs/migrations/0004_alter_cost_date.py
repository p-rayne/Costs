# Generated by Django 4.1 on 2023-04-05 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('costs', '0003_remove_category_parent_remove_cost_currency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cost',
            name='date',
            field=models.DateField(db_index=True),
        ),
    ]
