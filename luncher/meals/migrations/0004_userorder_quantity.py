# Generated by Django 2.1.7 on 2019-02-22 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meals', '0003_restaurant_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='userorder',
            name='quantity',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
