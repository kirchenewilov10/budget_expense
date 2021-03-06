# Generated by Django 2.2.6 on 2020-07-30 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orm', '0008_auto_20200728_2315'),
    ]

    operations = [
        migrations.CreateModel(
            name='incident',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guard_id', models.IntegerField(blank=True, default=0)),
                ('location_id', models.IntegerField(blank=True, default=0)),
                ('event_time', models.DateTimeField(blank=True)),
                ('event_type', models.CharField(blank=True, max_length=255)),
                ('event_desp', models.CharField(blank=True, max_length=255)),
            ],
        ),
    ]
