# Generated by Django 3.2.6 on 2022-05-01 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20220430_2229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='discounted_price',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='ratings',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='product',
            name='selling_price',
            field=models.FloatField(),
        ),
    ]
