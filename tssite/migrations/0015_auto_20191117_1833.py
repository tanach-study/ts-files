# Generated by Django 2.2.7 on 2019-11-17 18:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tssite', '0014_auto_20191117_1832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teamim',
            name='reader',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.SET_DEFAULT, to='tssite.Teacher'),
        ),
    ]