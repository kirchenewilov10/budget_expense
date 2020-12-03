# Generated by Django 2.2.6 on 2020-07-21 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orm', '0002_guard_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='attendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guard_id', models.IntegerField(blank=True, default=0)),
                ('location_id', models.IntegerField(blank=True, default=0)),
                ('attended_date', models.DateField(blank=True)),
                ('attended_hour', models.IntegerField(blank=True, default=0)),
            ],
        ),
    ]
