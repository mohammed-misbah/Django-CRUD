# Generated by Django 4.1.2 on 2022-11-18 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_regstr', '0006_alter_employee_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='Place',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='email',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='mobile',
            field=models.CharField(max_length=15, null=True),
        ),
    ]
