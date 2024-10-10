# Generated by Django 5.1.1 on 2024-10-01 08:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Destination',
            fields=[
                ('date_created', models.DateTimeField(editable=False)),
                ('date_modified', models.DateTimeField()),
                ('data_source', models.CharField(max_length=100)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('candy', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Gate',
            fields=[
                ('date_created', models.DateTimeField(editable=False)),
                ('date_modified', models.DateTimeField()),
                ('data_source', models.CharField(max_length=100)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('order', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('date_created', models.DateTimeField(editable=False)),
                ('date_modified', models.DateTimeField()),
                ('data_source', models.CharField(max_length=100)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('scheduled_departure', models.DateTimeField(blank=True, null=True)),
                ('scheduled_arrival', models.DateTimeField(blank=True, null=True)),
                ('delay_minutes', models.IntegerField(blank=True, null=True)),
                ('actual_departure', models.DateTimeField(blank=True, null=True)),
                ('actual_arrival', models.DateTimeField(blank=True, null=True)),
                ('capacity', models.IntegerField()),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.destination')),
                ('gate', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.gate')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('date_created', models.DateTimeField(editable=False)),
                ('date_modified', models.DateTimeField()),
                ('data_source', models.CharField(max_length=100)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=100)),
                ('costume', models.CharField(max_length=100)),
                ('tsa_precheck', models.BooleanField()),
                ('boarding_group', models.CharField(max_length=1)),
                ('boarding_position', models.IntegerField()),
                ('has_boarded', models.BooleanField()),
                ('flight', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.flight')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
