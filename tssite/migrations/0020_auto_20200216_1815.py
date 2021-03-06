# Generated by Django 2.2.9 on 2020-02-16 18:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tssite', '0019_auto_20191209_0636'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='class',
            options={'ordering': ['series_sequence', 'division_sequence', 'segment_sequence', 'section_sequence', 'unit_sequence', 'part_sequence']},
        ),
        migrations.AlterField(
            model_name='teamim',
            name='post',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='tssite.Class'),
        ),
        migrations.AlterField(
            model_name='teamim',
            name='reader',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='tssite.Teacher'),
        ),
    ]
