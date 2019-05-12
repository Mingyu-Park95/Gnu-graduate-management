from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class CustomUser(AbstractUser):
    username = models.CharField(max_length=20, unique=True, primary_key=True, validators=[RegexValidator(regex='^[a-zA-Z0-9]+$')], help_text='알파벳과 숫자만 입력 가능합니다.')
    eduYear = models.IntegerField(default=2014)
    studentMajor = models.CharField(max_length=30)
    studentDoubleMajor = models.CharField(max_length=30, default=None, null=True)
    studentTrack = models.CharField(max_length=30, default=None, null=True)
    studentSubMajor = models.CharField(max_length=30, default=None, null=True)
    studentConvergenceMajor = models.CharField(max_length=30, default=None, null=True)
    studentTeaching = models.CharField(max_length=30, default=None, null=True) # 교직이수
    # 융합전공 추가하기
#  RegexValidator=['a-zA-Z0-9']


class TakeList(models.Model):
    takeListUserName = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    classification = models.CharField(max_length=10)
    lectureNumber = models.CharField(max_length=10)
    lectureName = models.CharField(max_length=40)
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

class GradeByPeriod(models.Model):
    gradeByPeriodName =models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    period = models.CharField(max_length=30)
    grade = models.FloatField()
