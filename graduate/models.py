from django.db import models

# Create your models here.


class basic(models.Model): # 기초교양

    Edu_Year = models.IntegerField()  # 교육과정
    Department = models.CharField(max_length=20) # 학과
    Lecture_Name = models.CharField(max_length=20) # 과목명
    Lecture_Num = models.CharField(max_length=10) # 학수번호
    Lecture_Point = models.IntegerField()  # 학점