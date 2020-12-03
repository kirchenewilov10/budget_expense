# Generated by Django 2.2.6 on 2020-07-24 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orm', '0005_serivcecost'),
    ]

    operations = [
        migrations.CreateModel(
            name='equipmenttpl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('equipment_name', models.CharField(blank=True, max_length=255)),
                ('equipment_alias', models.CharField(blank=True, max_length=255)),
                ('equipment_desp', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.AlterField(
            model_name='serivcecost',
            name='service_cost',
            field=models.FloatField(blank=True, default=2),
        ),
    ]
