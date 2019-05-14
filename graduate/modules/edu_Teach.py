from graduate.models import *

from accounts.models import *
from django.db.models import Q

# 교과교육 영역 8학점 (3과목)
def edu_Teach_Judge(userName, eduYear, studentMajor):

    user_Take_list = []
    user_noTake_str = ''

    db_Teach_list =[]

    resultValue = []
    user_noTake_point =0

    # 유저가 들은 데이터 가져옴
    for take in TakeList.objects.filter(Q(takeListUserName=userName) & (Q(lectureName="상업교과교육론") | Q(lectureName="상업교과평가방법") | Q(lectureName="상업논리및논술교육"))):
        user_Take_list.append(take.lectureName)

    # db에서 데이터 가져옴
    for teach in EduTeach.objects.all():
        db_Teach_list.append(teach.lectureName)

    # 안들은 과목 추출
    for db_Teach in db_Teach_list:
        if db_Teach not in user_Take_list:
            user_noTake_point += EduTeach.objects.get(lectureName=db_Teach).lecturePoint
            user_noTake_str += db_Teach
            user_noTake_str += " / "

    resultValue.append("교과교육 영역 이수학점 {0}/8, 남은 과목 : {1}".format(int(8-user_noTake_point), user_noTake_str))

    return resultValue
