# Generated by Django 4.0.4 on 2022-09-03 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_remove_tokenlogin_alumno_id_tokenlogin_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tokenlogin',
            name='usuario',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
