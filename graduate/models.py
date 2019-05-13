from django.db import models

# Create your models here.
from accounts.models import CustomUser


class CapabilityList(models.Model): #  역량교양
    eduYear  = models.IntegerField() # 교육과정
    major = models.CharField(max_length=20) # 학과
    lectureName = models.CharField(max_length=20) # 과목명
    lectureNum = models.CharField(max_length=10) # 학수번호
    lecturePoint = models.IntegerField() # 학점


class BasicList(models.Model): # 기초교양
    eduYear = models.IntegerField()  # 교육과정
    major = models.CharField(max_length=20) # 학과
    lectureName = models.CharField(max_length=20) # 과목명
    lectureNum = models.CharField(max_length=10) # 학수번호
    lecturePoint = models.IntegerField()  # 학점


class IntegrationList(models.Model): # 통합교양
    major = models.CharField(max_length=20) # 학과
    lectureName = models.CharField(max_length=20) # 과목명
    lectureNum = models.CharField(max_length=10) # 학수번호


class PioneerList(models.Model):  # 개척교양
    eduYear = models.IntegerField()  # 교육과정
    major = models.CharField(max_length=20) # 학과
    lectureName = models.CharField(max_length=20) # 과목명
    lectureNum = models.CharField(max_length=10) # 학수번호
    lecturePoint = models.IntegerField()  # 학점


class MajorPoint(models.Model):
    eduYear = models.IntegerField()  # 교육과정
    major = models.CharField(max_length=20)  # 학과
    majorPoint = models.FloatField()        # 전필
    majorSelectPoint = models.FloatField()  # 전선
    dmajorPoint = models.FloatField()       # 이필
    dmajorSelectPoint = models.FloatField() # 이선
    subMajorPoint = models.FloatField()     # 부전공


class ConvergenceMajor(models.Model):
    eduYear = models.IntegerField()  # 교육과정
    major = models.CharField(max_length=20)  # 학과
    seperate = models.CharField(max_length=20) # 구분
    dmajorName = models.CharField(max_length=20)  # 과목명
    dmajornum = models.CharField(max_length=20)  # 학수번호
    dmajorPoint = models.FloatField()  # 과목 학점


class MajorList(models.Model):
    major = models.CharField(max_length=20) # 학과
    classification = models.CharField(max_length=10)
    lectureNum = models.CharField(max_length=10) # 학수번호
    lectureName = models.CharField(max_length=20)  # 과목명
    lecturePoint = models.IntegerField() # 학점
    checkSubMajor = models.IntegerField(default=0)
    checkDoubleMajor = models.IntegerField(default=0)

class Track(models.Model):
    eduYear = models.IntegerField()  # 교육과정
    trackName = models.CharField(max_length=20)
    seperate = models.CharField(max_length=20)  # 트랙구분
    lectureName = models.CharField(max_length=20)  # 과목명
    lectureNum = models.CharField(max_length=20)  # 트랙기본
    lecturePoint = models.FloatField()  # 과목 학점

class EduBasic(models.Model):

    major = models.CharField(max_length=20)  # 학과
    eduYear = models.IntegerField(default=1) #
    lectureNum = models.CharField(max_length=10)  # 학수번호

    lectureName = models.CharField(max_length=20)  # 과목명
    lecturePoint = models.IntegerField()  # 학점

class EduTeach(models.Model):
    major = models.CharField(max_length=20)  # 학과
    lectureNum = models.CharField(max_length=10)  # 학수번호
    lectureName = models.CharField(max_length=20)  # 과목명
    lecturePoint = models.IntegerField()  # 학점

class EduCareer(models.Model):
    classification = models.CharField(max_length=10) # 과목영역별 분류
    lectureNum = models.CharField(max_length=10)  # 학수번호
    lectureName = models.CharField(max_length=20)  # 과목명
    lecturePoint = models.IntegerField()  # 학점
# 필수로 들어야 하는 과목 음.......기초과정 고정과목처럼 처리하면 될 거 같은데

class LectureList(models.Model):
    classification = models.CharField(max_length=10)
    lectureNumber = models.CharField(max_length=10)
    lectureName = models.CharField(max_length=40)
    lecturePoint = models.IntegerField(default=0)
    grade = models.CharField(max_length=2)
