# Generated by Django 2.2.7 on 2019-11-08 03:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cats', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='breed',
            name='home',
        ),
        migrations.AlterField(
            model_name='human',
            name='home',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cats.Home'),
        ),
    ]
