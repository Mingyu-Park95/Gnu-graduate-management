# Generated by Django 2.2 on 2019-05-12 13:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_customuser_studentteaching'),
    ]

    operations = [
        migrations.CreateModel(
            name='GradeByPeriod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('period', models.CharField(max_length=30)),
                ('grade', models.FloatField()),
                ('gradeByPeriodName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
