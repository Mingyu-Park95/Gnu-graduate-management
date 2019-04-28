from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class CustomUser(AbstractUser):
    username = models.CharField(max_length=20, unique=True, primary_key=True, validators=[RegexValidator(regex='^[a-zA-Z0-9]+$')])
    studentId = models.IntegerField(default=2014)
    studentMajor = models.CharField(max_length=30)
#  RegexValidator=['a-zA-Z0-9']


class TakeList(models.Model):
    takeListUserName = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    classification = models.CharField(max_length=10)
    lectureNumber = models.CharField(max_length=10)
    lectureName = models.CharField(max_length=20)
    lecturePoint = models.IntegerField(default=0)
    grade = models.CharField(max_length=2)


class TakeListPoint(models.Model):
    TakeListPointUserName = models.OneToOneField(CustomUser,  on_delete=models.CASCADE)
    capability = models.FloatField(verbose_name='역량학점')
    integration = models.FloatField(verbose_name='통합학점')
    basic = models.FloatField(verbose_name='기초학점')
    general = models.FloatField(verbose_name='일반학점')
    pioneer = models.FloatField(verbose_name='개척학점')
    majorSelect = models.FloatField(verbose_name='전선학점')
    major = models.FloatField(verbose_name='전필학점')
    dmajorSelect = models.FloatField(verbose_name='이선학점')
    dmajor = models.FloatField(verbose_name='이필')
    total = models.FloatField(verbose_name='전체학점')


