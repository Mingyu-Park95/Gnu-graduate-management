from graduate.models import *
from accounts.models import *
from django.db.models import Q

def channelTrack_Judge(userName, eduYear, studentMajor):
    user_Take_list = [] # 사용자가 들은 과목 리스트
    db_Basic_list = [] # 트랙기초 리스트
    db_Advance_list = [] # 트랙심화 리스트
    db_Common_list = [] # 트랙공통 리스트

    # 사용자가 들은 각각의 트랙 학점
    user_Basic_point =0
    user_Advance_point =0
    user_common_point= 0

    # 필요 학점
    total_Basic_point = 12
    total_Advance_point =9
    total_common_point  = 9

    user_noTake_str = '' # 듣지 않은 과목 표시해줄 str
    resultValue = [] # return 해주는 변수

    # 사용자가 들은 전선, 전필 과목들 저장
    for takeList in TakeList.objects.filter(
            Q(takeListUserName=userName) & (Q(classification="전선") | Q(classification="전필") | Q(classification="이필") | Q(classification="이선"))):
        user_Take_list.append(takeList.lectureNumber)

    if eduYear < 2018: # 교육과정이 2018 미만이라면

        for trackBasic in Track.objects.filter(Q(eduYear__lt=2018) & Q(trackName="유통서비스트랙") & Q(seperate="트랙기본")):
            db_Basic_list.append(trackBasic.lectureNum)

        # 트랙기본 이수 개수 확인
        for db_Basic in db_Basic_list:
            if db_Basic in user_Take_list:
                user_Basic_point += Track.objects.get(
                    Q(lectureNum=db_Basic) & Q(eduYear__lt=2018) & Q(trackName="유통서비스트랙")).lecturePoint
            else: # 듣지 않은 과목명 저장
                user_noTake_str += Track.objects.get(
                    Q(lectureNum=db_Basic) & Q(eduYear__lt=2018) & Q(trackName="유통서비스트랙")).lectureName
                user_noTake_str += "/"

        if user_Basic_point >= total_Basic_point:
            resultValue.append("트랙기본 이수")
        else:
            resultValue.append(
                "트랙기본 {0}학점이 부족합니다.".format(total_Basic_point - user_Basic_point) + "남은 과목 : " + user_noTake_str)

        user_noTake_str = '' #  남은 과목들 초기화

        # 트랙심화 이수 개수 확인
        for trackAdvance in Track.objects.filter(Q(eduYear__lt=2018) & Q(trackName="유통서비스트랙") & Q(seperate="트랙심화")):
            db_Advance_list.append(trackAdvance.lectureNum)

        for db_Advance in db_Advance_list:
            if db_Advance in user_Take_list:
                user_Advance_point += Track.objects.get(
                    Q(lectureNum=db_Advance) & Q(eduYear__lt=2018) & Q(trackName="유통서비스트랙")).lecturePoint
            else:
                user_noTake_str += Track.objects.get(
                    Q(lectureNum=db_Advance) & Q(eduYear__lt=2018) & Q(trackName="유통서비스트랙")).lectureName
                user_noTake_str += "/"

        if user_Advance_point >= total_Advance_point:
            resultValue.append("트랙심화 이수")
        else:
            resultValue.append(
                "트랙심화 {0}학점이 부족합니다.".format(total_Advance_point - user_Advance_point) + "남은 과목 : " + user_noTake_str)

        user_noTake_str = ''  # 남은 과목들 초기화

        # 트랙공통 이수 개수 확인
        for trackCommon in Track.objects.filter(Q(eduYear__lt=2018) & Q(trackName="유통서비스트랙") & Q(seperate="트랙공통")):
            db_Common_list.append(trackCommon.lectureNum)

        for db_Common in db_Common_list:
            if db_Common in user_Take_list:
                user_common_point += Track.objects.get(
                    Q(lectureNum=db_Common) & Q(eduYear__lt=2018) & Q(trackName="유통서비스트랙")).lecturePoint
            else:
                user_noTake_str += Track.objects.get(
                    Q(lectureNum=db_Common) & Q(eduYear__lt=2018) & Q(trackName="유통서비스트랙")).lectureName
                user_noTake_str += "/"

        if user_common_point >= total_common_point:
            resultValue.append("트랙공통 이수")
        else:
            resultValue.append(
                "트랙공통 {0}학점이 부족합니다.".format(total_common_point - user_common_point) + "남은 과목 : " + user_noTake_str)

        return resultValue

    else:  # 교육과정이 2018 이후 라면

        for trackBasic in Track.objects.filter(Q(eduYear__gte=2018) & Q(trackName="유통서비스트랙") & Q(seperate="트랙기본")):
            db_Basic_list.append(trackBasic.lectureNum)

        # 트랙기본 이수 개수 확인
        for db_Basic in db_Basic_list:
            if db_Basic in user_Take_list:
                user_Basic_point += Track.objects.get(
                    Q(lectureNum=db_Basic) & Q(eduYear__gte=2018) & Q(trackName="유통서비스트랙")).lecturePoint
            else:  # 듣지 않은 과목명 저장
                user_noTake_str += Track.objects.get(
                    Q(lectureNum=db_Basic) & Q(eduYear__gte=2018) & Q(trackName="유통서비스트랙")).lectureName
                user_noTake_str += "/"

        if user_Basic_point >= total_Basic_point:
            resultValue.append("트랙기본 이수")
        else:
            resultValue.append(
                "트랙기본 {0}학점이 부족합니다.".format(total_Basic_point - user_Basic_point) + "남은 과목 : " + user_noTake_str)

        user_noTake_str = ''  # 남은 과목들 초기화

        # 트랙심화 이수 개수 확인
        for trackAdvance in Track.objects.filter(Q(eduYear__gte=2018) & Q(trackName="유통서비스트랙") & Q(seperate="트랙심화")):
            db_Advance_list.append(trackAdvance.lectureNum)

        for db_Advance in db_Advance_list:
            if db_Advance in user_Take_list:
                user_Advance_point += Track.objects.get(
                    Q(lectureNum=db_Advance) & Q(eduYear__gte=2018) & Q(trackName="유통서비스트랙")).lecturePoint
            else:
                user_noTake_str += Track.objects.get(
                    Q(lectureNum=db_Advance) & Q(eduYear__gte=2018) & Q(trackName="유통서비스트랙")).lectureName
                user_noTake_str += "/"

        if user_Advance_point >= total_Advance_point:
            resultValue.append("트랙심화 이수")
        else:
            resultValue.append(
                "트랙심화 {0}학점이 부족합니다.".format(
                    total_Advance_point - user_Advance_point) + "남은 과목 : " + user_noTake_str)

        user_noTake_str = ''  # 남은 과목들 초기화

        # 트랙공통 이수 개수 확인
        for trackCommon in Track.objects.filter(Q(eduYear__gte=2018) & Q(trackName="유통서비스트랙") & Q(seperate="트랙공통")):
            db_Common_list.append(trackCommon.lectureNum)

        for db_Common in db_Common_list:
            if db_Common in user_Take_list:
                user_common_point += Track.objects.get(
                    Q(lectureNum=db_Common) & Q(eduYear__gte=2018) & Q(trackName="유통서비스트랙")).lecturePoint
            else:
                user_noTake_str += Track.objects.get(
                    Q(lectureNum=db_Common) & Q(eduYear__gte=2018) & Q(trackName="유통서비스트랙")).lectureName
                user_noTake_str += "/"

        if user_common_point >= total_common_point:
            resultValue.append("트랙공통 이수")
        else:
            resultValue.append(
                "트랙공통 {0}학점이 부족합니다.".format(total_common_point - user_common_point) + "남은 과목 : " + user_noTake_str)

        return resultValue