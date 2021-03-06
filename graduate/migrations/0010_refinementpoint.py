# Generated by Django 2.2 on 2019-05-14 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graduate', '0009_lecturelist'),
    ]

    operations = [
        migrations.CreateModel(
            name='RefinementPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('major', models.CharField(max_length=20)),
                ('eduYear', models.IntegerField()),
                ('capabilityPoint', models.FloatField(verbose_name='역량학점')),
                ('integrationPoint', models.FloatField(verbose_name='통합학점')),
                ('basicPoint', models.FloatField(verbose_name='기초학점')),
                ('pioneerPoint', models.FloatField(verbose_name='개척학점')),
            ],
        ),
    ]
