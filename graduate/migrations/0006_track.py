# Generated by Django 2.2 on 2019-05-10 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graduate', '0005_majorlist'),
    ]

    operations = [
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eduYear', models.IntegerField()),
                ('trackName', models.CharField(max_length=20)),
                ('seperate', models.CharField(max_length=20)),
                ('lectureName', models.CharField(max_length=20)),
                ('lectureNum', models.CharField(max_length=20)),
                ('lecturePoint', models.FloatField()),
            ],
        ),
    ]
