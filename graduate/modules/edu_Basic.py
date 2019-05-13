from graduate.models import *

from accounts.models import *
from django.db.models import Q

# 교직 기본 이수과목 21학점(7과목이상)
def edu_Basic_Judge(userName, eduYear, studentMajor):
    user_Take_list = []
    user_noTake_str = ''

    db_list = []
    resultValue = []
    user_Take_point = 0

    # 유저가 들은 데이터 가져옴
    for takeList in TakeList.objects.filter(Q(takeListUserName=userName) & (
            Q(classification="전선") | Q(classification="전필") | Q(classification="이필") | Q(classification="이선"))):
        user_Take_list.append(takeList.lectureNumber)

    # 경영학과 교직 기본 비교
    if studentMajor =="경영학과":
        if eduYear <2016:
            for basic in EduBasic.objects.filter(Q(major="경영학과") & Q(eduYear="2014")):
                db_list.append(basic.lectureNum)

            for db in db_list:
                if db in user_Take_list:
                    user_Take_point += EduBasic.objects.get(Q(major="경영학과") & Q(lectureNum=db) & Q(eduYear="2014")).lecturePoint

                else:
                    user_noTake_str += EduBasic.objects.get(Q(major="경영학과") & Q(lectureNum=db) & Q(eduYear="2014")).lectureName
                    user_noTake_str += " / "

            resultValue.append("교직 기본 이수학점 : {0}/21, 남은과목 : {1}".format(user_Take_point,user_noTake_str))

            return resultValue

        elif eduYear == 2016:
            for basic in EduBasic.objects.filter(Q(major="경영학과") & Q(eduYear="2016")):
                db_list.append(basic.lectureNum)

            for db in db_list:
                if db in user_Take_list:
                    user_Take_point += EduBasic.objects.get(Q(major="경영학과") & Q(lectureNum=db) & Q(eduYear="2016")).lecturePoint

                else:
                    user_noTake_str += EduBasic.objects.get(Q(major="경영학과") & Q(lectureNum=db) & Q(eduYear="2016")).lectureName
                    user_noTake_str += " / "

            resultValue.append("교직 기본 이수학점 : {0}/21, 남은과목 : {1}".format(user_Take_point,user_noTake_str))

            return resultValue

        else: # 신청연도가 2016 이후 일때

            for basic in EduBasic.objects.filter(Q(major="경영학과") & Q(eduYear="2017")):
                db_list.append(basic.lectureNum)

            for db in db_list:
                if db in user_Take_list:
                    user_Take_point += EduBasic.objects.get(Q(major="경영학과") & Q(lectureNum=db) & Q(eduYear="2017")).lecturePoint

                else:
                    user_noTake_str += EduBasic.objects.get(Q(major="경영학과") & Q(lectureNum=db) & Q(eduYear="2017")).lectureName
                    user_noTake_str += " / "

            resultValue.append("교직 기본 이수학점 : {0}/21, 남은과목 : {1}".format(user_Take_point,user_noTake_str))

            return resultValue

        # 경영학과 교직 기본 비교
    elif studentMajor == "회계학과":
        if eduYear < 2016:
            for basic in EduBasic.objects.filter(Q(major="회계학과") & Q(eduYear="2014")):
                db_list.append(basic.lectureNum)

            for db in db_list:
                if db in user_Take_list:
                    user_Take_point += EduBasic.objects.get(Q(major="회계학과") & Q(lectureNum=db) & Q(eduYear="2014")).lecturePoint

                else:
                    user_noTake_str += EduBasic.objects.get(Q(major="회계학과") & Q(lectureNum=db) & Q(eduYear="2014")).lectureName
                    user_noTake_str += " / "

            resultValue.append("교직 기본 이수학점 : {0}/21, 남은과목 : {1}".format(user_Take_point, user_noTake_str))

            return resultValue

        elif eduYear==2016:
            for basic in EduBasic.objects.filter(Q(major="회계학과") & Q(eduYear="2016")):
                db_list.append(basic.lectureNum)

            for db in db_list:
                if db in user_Take_list:
                    user_Take_point += EduBasic.objects.get(Q(major="회계학과") & Q(lectureNum=db) & Q(eduYear="2016")).lecturePoint

                else:
                    user_noTake_str += EduBasic.objects.get(Q(major="회계학과") & Q(lectureNum=db) & Q(eduYear="2016")).lectureName
                    user_noTake_str += " / "

            resultValue.append("교직 기본 이수학점 : {0}/21, 남은과목 : {1}".format(user_Take_point, user_noTake_str))

            return resultValue

        else: # 2016년 이후 신청자라면
            for basic in EduBasic.objects.filter(Q(major="회계학과") & Q(eduYear="2017")):
                db_list.append(basic.lectureNum)

            for db in db_list:
                if db in user_Take_list:
                    user_Take_point += EduBasic.objects.get(Q(major="회계학과") & Q(lectureNum=db) & Q(eduYear="2017")).lecturePoint

                else:
                    user_noTake_str += EduBasic.objects.get(Q(major="회계학과") & Q(lectureNum=db) & Q(eduYear="2017")).lectureName
                    user_noTake_str += " / "

            resultValue.append("교직 기본 이수학점 : {0}/21, 남은과목 : {1}".format(user_Take_point, user_noTake_str))

            return resultValue

    # 국제통상학과 교직 기본 비교
    elif studentMajor =="국제통상학과":
        if eduYear <=2014:
            for basic in EduBasic.objects.filter(Q(major="국제통상학과") & Q(eduYear="2014")):
                db_list.append(basic.lectureNum)

            for db in db_list:
                if db in user_Take_list:
                    user_Take_point += EduBasic.objects.get(Q(major="국제통상학과") & Q(lectureNum=db) & Q(eduYear="2014")).lecturePoint

                else:
                    user_noTake_str += EduBasic.objects.get(Q(major="국제통상학과") & Q(lectureNum=db) & Q(eduYear="2014")).lectureName
                    user_noTake_str += " / "

            resultValue.append("교직 기본 이수학점 : {0}/21, 남은과목 : {1}".format(user_Take_point,user_noTake_str))

            return resultValue

        elif eduYear ==2015:
            for basic in EduBasic.objects.filter(Q(major="국제통상학과") & Q(eduYear="2015")):
                db_list.append(basic.lectureNum)

            for db in db_list:
                if db in user_Take_list:
                    user_Take_point += EduBasic.objects.get(
                        Q(major="국제통상학과") & Q(lectureNum=db) & Q(eduYear="2015")).lecturePoint

                else:
                    user_noTake_str += EduBasic.objects.get(
                        Q(major="국제통상학과") & Q(lectureNum=db) & Q(eduYear="2015")).lectureName
                    user_noTake_str += " / "

            resultValue.append("교직 기본 이수학점 : {0}/21, 남은과목 : {1}".format(user_Take_point, user_noTake_str))

            return resultValue

        elif eduYear ==2016:
            for basic in EduBasic.objects.filter(Q(major="국제통상학과") & Q(eduYear="2016")):
                db_list.append(basic.lectureNum)

            for db in db_list:
                if db in user_Take_list:
                    user_Take_point += EduBasic.objects.get(
                        Q(major="국제통상학과") & Q(lectureNum=db) & Q(eduYear="2016")).lecturePoint

                else:
                    user_noTake_str += EduBasic.objects.get(
                        Q(major="국제통상학과") & Q(lectureNum=db) & Q(eduYear="2016")).lectureName
                    user_noTake_str += " / "

            resultValue.append("교직 기본 이수학점 : {0}/21, 남은과목 : {1}".format(user_Take_point, user_noTake_str))

            return resultValue

        else: # 2017년 이후 신청자
            for basic in EduBasic.objects.filter(Q(major="국제통상학과") & Q(eduYear="2017")):
                db_list.append(basic.lectureNum)

            for db in db_list:
                if db in user_Take_list:
                    user_Take_point += EduBasic.objects.get(
                        Q(major="국제통상학과") & Q(lectureNum=db) & Q(eduYear="2017")).lecturePoint

                else:
                    user_noTake_str += EduBasic.objects.get(
                        Q(major="국제통상학과") & Q(lectureNum=db) & Q(eduYear="2017")).lectureName
                    user_noTake_str += " / "

            resultValue.append("교직 기본 이수학점 : {0}/21, 남은과목 : {1}".format(user_Take_point, user_noTake_str))

            return resultValue