# Generated by Django 3.0.3 on 2020-03-20 03:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tssite', '0025_auto_20200320_0334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='talmudstudy',
            name='date',
            field=models.DateTimeField(),
        ),
    ]