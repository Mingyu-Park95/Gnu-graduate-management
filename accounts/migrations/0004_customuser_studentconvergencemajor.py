# Generated by Django 2.2 on 2019-05-08 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_customuser_studentsubmajor'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='studentConvergenceMajor',
            field=models.CharField(default=None, max_length=30, null=True),
        ),
    ]