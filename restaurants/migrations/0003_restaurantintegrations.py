# Generated by Django 3.0.7 on 2020-07-01 13:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0002_auto_20200630_0047'),
    ]

    operations = [
        migrations.CreateModel(
            name='RestaurantIntegrations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wc_consumer_key', models.CharField(max_length=50)),
                ('wc_consumer_secret', models.CharField(max_length=50)),
                ('woo_commerce_url', models.URLField()),
                ('restaurat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurants.Restaurant')),
            ],
        ),
    ]
