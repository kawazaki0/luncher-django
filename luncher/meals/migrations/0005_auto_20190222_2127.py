# Generated by Django 2.1.7 on 2019-02-22 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meals', '0004_userorder_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meal',
            name='date',
            field=models.DateField(),
        ),
    ]
