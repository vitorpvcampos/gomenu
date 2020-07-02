# Generated by Django 3.0.7 on 2020-07-02 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0003_restaurantintegrations'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='online_sales',
            field=models.BooleanField(default=False, verbose_name='Vendas online'),
        ),
    ]
