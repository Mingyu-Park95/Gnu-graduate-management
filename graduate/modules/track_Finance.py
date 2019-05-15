from graduate.models import *
from accounts.models import *
from django.db.models import Q


def financeTrack_Judge(userName, eduYear, studentMajor):
    user_Take_list = []
    db_Track_list = []

    user_Track_point = 0
    user_noTake_str = ''
    resultValue = []
    user_takeTrack_list =[]

    for takeList in TakeList.objects.filter(
            Q(takeListUserName=userName) & (Q(classification="전선") | Q(classification="전필") | Q(classification="이필") | Q(classification="이선"))):
        user_Take_list.append(takeList.lectureNumber)

    if eduYear < 2018:
        total_Track_point = 21

        for trackBasic in Track.objects.filter(Q(eduYear__lt=2019) & Q(trackName="재무금융트랙")):
            db_Track_list.append(trackBasic.lectureNum)

        # 트랙기본 이수 개수 확인
        for db_Basic in db_Track_list:
            if db_Basic in user_Take_list:
                user_Track_point += Track.objects.get(
                    Q(lectureNum=db_Basic) & Q(eduYear__lt=2019) & Q(trackName="재무금융트랙")).lecturePoint
                user_takeTrack_list.append(
                    TakeList.objects.get(Q(lectureNumber=db_Basic) & Q(takeListUserName=userName)))

            else:
                user_noTake_str += Track.objects.get(
                    Q(lectureNum=db_Basic) & Q(eduYear__lt=2019) & Q(trackName="재무금융트랙")).lectureName
                user_noTake_str += "/"

        if user_Track_point >= total_Track_point:
            resultValue.append("트랙기본 이수")
        else:
            resultValue.append(
                "트랙기본 {0}학점이 부족합니다.".format(total_Track_point - user_Track_point) + "들어야하는 과목 : " + user_noTake_str)

        return resultValue, user_takeTrack_list

    else:
        total_Track_point = 24

        for takeList in TakeList.objects.filter(
                Q(takeListUserName=userName) & (Q(classification="전선") | Q(classification="전필"))):
            user_Take_list.append(takeList.lectureNumber)

        for trackBasic in Track.objects.filter(Q(eduYear=2019) & Q(trackName="재무금융트랙")):
            db_Track_list.append(trackBasic.lectureNum)

        # 트랙기본 이수 개수 확인
        for db_Basic in db_Track_list:
            if db_Basic in user_Take_list:
                user_Track_point += Track.objects.get(
                    Q(lectureNum=db_Basic) & Q(eduYear=2019) & Q(trackName="재무금융트랙")).lecturePoint
                user_takeTrack_list.append(
                    TakeList.objects.get(Q(lectureNumber=db_Basic) & Q(takeListUserName=userName)))

            else:
                user_noTake_str += Track.objects.get(
                    Q(lectureNum=db_Basic) & Q(eduYear=2019) & Q(trackName="재무금융트랙")).lectureName
                user_noTake_str += "/"

        if user_Track_point >= total_Track_point:
            resultValue.append("트랙기본 이수")
        else:
            resultValue.append(
                "트랙기본 {0}학점이 부족합니다.".format(total_Track_point - user_Track_point) + "들어야하는 과목 : " + user_noTake_str)

        return resultValue, user_takeTrack_list