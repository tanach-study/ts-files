# Generated by Django 2.2.7 on 2019-11-17 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tssite', '0009_auto_20191117_1726'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classes',
            name='teamim',
        ),
        migrations.AddField(
            model_name='classes',
            name='teamim',
            field=models.ManyToManyField(to='tssite.Teamim'),
        ),
    ]