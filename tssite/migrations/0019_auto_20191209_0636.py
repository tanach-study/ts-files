# Generated by Django 2.2.8 on 2019-12-09 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tssite', '0018_auto_20191208_2346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='part',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='class',
            name='series',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
