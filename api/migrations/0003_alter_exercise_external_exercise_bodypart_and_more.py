# Generated by Django 4.2.7 on 2023-11-07 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_exercise_external_exercise_bodypart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='external_exercise_bodypart',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='exercise',
            name='external_exercise_id',
            field=models.CharField(max_length=4),
        ),
    ]