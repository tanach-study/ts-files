# Generated by Django 2.2.7 on 2019-11-17 17:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tssite', '0010_auto_20191117_1735'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classes',
            name='teamim',
        ),
        migrations.RemoveField(
            model_name='teamim',
            name='audio_url',
        ),
        migrations.AddField(
            model_name='teamim',
            name='audio',
            field=models.FileField(blank=True, null=True, upload_to='uploads/'),
        ),
        migrations.AddField(
            model_name='teamim',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tssite.Classes'),
        ),
    ]
