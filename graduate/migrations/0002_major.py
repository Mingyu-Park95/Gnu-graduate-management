# Generated by Django 2.2 on 2019-05-08 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graduate', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Major',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eduYear', models.IntegerField()),
                ('major', models.CharField(max_length=20)),
                ('majorPoint', models.FloatField()),
                ('majorSelectPoint', models.FloatField()),
                ('dmajorPoint', models.FloatField()),
                ('dmajorSelectPoint', models.FloatField()),
                ('subMajorPoint', models.FloatField()),
            ],
        ),
    ]