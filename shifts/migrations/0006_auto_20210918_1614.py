# Generated by Django 3.2.5 on 2021-09-18 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shifts', '0005_stamp_duplicatetimestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slice',
            name='end',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='slice',
            name='stampGroup',
            field=models.CharField(max_length=3),
        ),
        migrations.AlterField(
            model_name='slice',
            name='start',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='stamp',
            name='stampGroup',
            field=models.CharField(max_length=3),
        ),
        migrations.AlterField(
            model_name='stamp',
            name='stampType',
            field=models.CharField(max_length=2),
        ),
    ]
