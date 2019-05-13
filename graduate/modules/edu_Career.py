from graduate.models import *

from accounts.models import *
from django.db.models import Q

def edu_Career_Judge(userName, eduYear, studentMajor):
    user_Take_list = []
    user_noTake_str =''

    db_careertheory_list =[]
    db_careerknowledge_list =[]
    db_careerpractice_list =[]

    user_theory_point =0
    user_knowledge_point = 0
    user_practice_point = 0

    resultValue = []

    # DB에 있는 교직이론 과목
    for theory in EduCareer.objects.filter(classification="교직이론"):
        db_careertheory_list.append(theory.lectureNum)

    # DB에 있는 교직소양 과목
    for knowledge in EduCareer.objects.filter(classification="교직소양"):
        db_careerknowledge_list.append(knowledge.lectureNum)

    # DB에 있는 교직실습 과목
    for practice in EduCareer.objects.filter(classification="교직실습"):
        db_careerpractice_list.append(practice.lectureNum)

    # 유저가 들은 데이터 가져옴
    for take in TakeList.objects.filter(takeListUserName=userName):
        user_Take_list.append(take.lectureNumber)

    # 교직이론
    for db_careertheory in db_careertheory_list:
        if db_careertheory in user_Take_list:
            user_theory_point += EduCareer.objects.get(lectureNum=db_careertheory).lecturePoint
        else:
            user_noTake_str += EduCareer.objects.get(lectureNum=db_careertheory).lectureName
            user_noTake_str += ' / '

    resultValue.append("교직이론 이수학점 : {0}/12, 남은 과목 : {1}".format(user_theory_point,user_noTake_str))

    user_noTake_str ='' # 남은과목  초기화

    # 교직소양
    for db_careerknowledge in db_careerknowledge_list:
        if db_careerknowledge in user_Take_list:
            user_knowledge_point += EduCareer.objects.get(lectureNum=db_careerknowledge).lecturePoint
        else:
            user_noTake_str += EduCareer.objects.get(lectureNum=db_careerknowledge).lectureName
            user_noTake_str += ' / '

    resultValue.append("교직소양 이수학점 : {0}/6, 남은 과목 : {1}".format(user_knowledge_point,user_noTake_str))

    # 교직실무
    for db_careerpractice in db_careerpractice_list:
        if db_careerpractice in user_Take_list:
            user_practice_point += EduCareer.objects.get(lectureNum=db_careerpractice).lecturePoint
        else:
            user_noTake_str += EduCareer.objects.get(lectureNum=db_careerpractice).lectureName

    resultValue.append("교직실습 이수학점 : {0}/6, 남은 과목 : {1}".format(user_practice_point,user_noTake_str))
    user_noTake_str += ' / '

    return resultValue