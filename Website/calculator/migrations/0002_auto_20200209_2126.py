# Generated by Django 3.0.3 on 2020-02-09 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='graph',
            name='image',
            field=models.ImageField(upload_to='graphs/'),
        ),
    ]
