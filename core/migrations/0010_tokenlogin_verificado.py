# Generated by Django 4.0.4 on 2022-09-03 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_alter_tokenalumno_alumno_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tokenlogin',
            name='verificado',
            field=models.BooleanField(default=False),
        ),
    ]