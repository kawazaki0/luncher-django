# Generated by Django 2.0.10 on 2019-02-26 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meals', '0005_auto_20190222_2127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userorder',
            name='quantity',
            field=models.PositiveIntegerField(),
        ),
    ]