# Generated by Django 2.2.7 on 2019-11-18 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cats', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cat',
            name='date_of_birth',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='human',
            name='date_of_birth',
            field=models.DateField(),
        ),
    ]
