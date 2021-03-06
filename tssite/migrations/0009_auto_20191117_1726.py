# Generated by Django 2.2.7 on 2019-11-17 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tssite', '0008_auto_20191117_1719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='uploads/'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='image_url',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='mname',
            field=models.CharField(blank=True, default=None, max_length=10, null=True),
        ),
    ]
