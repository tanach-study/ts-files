# Generated by Django 2.2.7 on 2019-11-17 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tssite', '0005_auto_20191117_1715'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='mname',
            field=models.CharField(default=None, max_length=10, null=True),
        ),
    ]
