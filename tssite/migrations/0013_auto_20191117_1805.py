# Generated by Django 2.2.7 on 2019-11-17 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tssite', '0012_auto_20191117_1804'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
