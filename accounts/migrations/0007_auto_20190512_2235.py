# Generated by Django 2.2 on 2019-05-12 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_gradebyperiod'),
    ]

    operations = [
        migrations.AlterField(
            model_name='takelist',
            name='lectureName',
            field=models.CharField(max_length=40),
        ),
    ]