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

