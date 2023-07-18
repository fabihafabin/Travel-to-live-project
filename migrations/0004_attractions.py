# Generated by Django 3.2.6 on 2022-04-30 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20220318_1251'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attractions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place_name', models.CharField(max_length=100)),
                ('location', models.FloatField()),
                ('description', models.TextField()),
                ('popularity', models.CharField(max_length=100)),
                ('product_image', models.ImageField(upload_to='productimg')),
            ],
        ),
    ]