
# 전공과목 50학점 이상
# 표시과목별 기본이수 과목 21학점 (7과목)이상
# 표시과목별 교과교육영역 8학점(3과목)이상

# 교직과목 22학점 이상
# 교직이론 12학점 이상(6과목 이상)
# 교직소양 6학점 이상
    # 특수교육학개론 2학점
    # 교직 실무 2학점
    # 학교폭력예방 및 학생의 이해 2학점
# 교육실습 4학점 이상
from django.db.models import Q

from accounts.models import TakeList
from graduate.models import EduCareer


def checkEdu(userName, eduYear, studentMajor, studentDoubleMajor, studentSubMajor):

# 모델에 추가 필요
    teach = '교직'
    teachTheory = '교직이론'
    teachCultivated ='교직소양'
    teachPractice = '교육실습'


# 교직 과목
    userteachList = TakeList.objects.filter(Q(userName=userName)&Q(classification=teach))

    # 교직이론 / 들은 학점, 안들은 과목
    teachTheoryList = EduCareer.objects.filter(classification='교직이론')
    teachTheoryPoint = 0
    notTakeTeackTheoryList = []
    for userteach in userteachList:
        for teachTheory in teachTheoryList:
            if userteach.lectureNumber == teachTheory.lectureNumber:
                teachTheoryPoint += 2
            else:
                notTakeTeackTheoryList.append(teachTheory.lectureName)

    # 교직 소양







