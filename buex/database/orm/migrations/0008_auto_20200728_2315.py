# Generated by Django 2.2.6 on 2020-07-28 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orm', '0007_equipmentcost'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='locations_attendance',
        ),
        migrations.AddField(
            model_name='attendance',
            name='attented_hour',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='attendance',
            name='location_id',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
