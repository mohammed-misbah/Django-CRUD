# Generated by Django 4.1.2 on 2022-11-16 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_regstr', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]