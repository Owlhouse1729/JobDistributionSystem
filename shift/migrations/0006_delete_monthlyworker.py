# Generated by Django 4.1.1 on 2022-09-20 06:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shift', '0005_rename_month_monthlyworker_table'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MonthlyWorker',
        ),
    ]
