# Generated by Django 2.2 on 2019-05-11 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graduate', '0006_track'),
    ]

    operations = [
        migrations.CreateModel(
            name='EduBasic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('major', models.CharField(max_length=20)),
                ('lectureNum', models.CharField(max_length=10)),
                ('lectureName', models.CharField(max_length=20)),
                ('lecturePoint', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='EduCareer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classification', models.CharField(max_length=10)),
                ('lectureNum', models.CharField(max_length=10)),
                ('lectureName', models.CharField(max_length=20)),
                ('lecturePoint', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='EduTeach',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('major', models.CharField(max_length=20)),
                ('lectureNum', models.CharField(max_length=10)),
                ('lectureName', models.CharField(max_length=20)),
                ('lecturePoint', models.IntegerField()),
            ],
        ),
    ]
