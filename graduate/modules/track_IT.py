from graduate.models import *
from accounts.models import *
from django.db.models import Q

def ITtrack_Judge(userName, eduYear, studentMajor):
    user_Take_list = []
    db_Basic_list = []
    db_Advance_list = []

    user_takeBasic_point = 0
    user_takeAdvance_point = 0
    resultValue_str =''
    user_takeTrack_list =[]
    if eduYear <2019:
        total_track_Basic = 18
        total_track_Advance = 9

        for takeList in TakeList.objects.filter(Q(takeListUserName=userName) & (Q(classification="전선") | Q(classification="전필") | Q(classification="이필") | Q(classification="이선"))):
            user_Take_list.append(takeList.lectureNumber)

        for trackBasic in Track.objects.filter(Q(eduYear__lt=2019) & Q(trackName ="IT융합시스템개발") & Q(seperate="트랙기본")):
            db_Basic_list.append(trackBasic.lectureNum)

        for trackAdvance in Track.objects.filter(Q(eduYear__lt=2019) & Q(trackName ="IT융합시스템개발") & Q(seperate="트랙심화")):
            db_Advance_list.append(trackAdvance.lectureNum)

        # 트랙기본 이수 개수 확인
        for db_Basic in db_Basic_list:
            if db_Basic in user_Take_list:
                user_takeBasic_point += Track.objects.get(Q(lectureNum=db_Basic) & Q(eduYear=2018) & Q(trackName ="IT융합시스템개발") & Q(seperate="트랙기본")).lecturePoint
                user_takeTrack_list.append(TakeList.objects.get(Q(lectureNumber=db_Basic) & Q(takeListUserName=userName)))

        if user_takeBasic_point >= total_track_Basic:
            resultValue_str +="트랙기본 이수 / "
        else:
            resultValue_str+="트랙기본 {0}학점이 부족합니다./ ".format(total_track_Basic - user_takeBasic_point)

        #트랙심화 이수 개수 확인
        for db_Advance in db_Advance_list:
            if db_Advance in user_Take_list:
                user_takeAdvance_point += Track.objects.get(Q(lectureNum=db_Advance) & Q(eduYear=2018) & Q(trackName ="IT융합시스템개발") & Q(seperate="트랙심화")).lecturePoint
                user_takeTrack_list.append(TakeList.objects.get(Q(lectureNumber=db_Advance) & Q(takeListUserName=userName)))

        if user_takeAdvance_point >= total_track_Advance:
            resultValue_str +="트랙심화 이수"
        else:
            resultValue_str+="트랙심화 {0}학점이 부족합니다.".format(total_track_Advance - user_takeAdvance_point)

        return resultValue_str, user_takeTrack_list

    else: # 2019교육과정부터
        total_track_Basic = 12
        total_track_Advance = 24

        for takeList in TakeList.objects.filter(Q(takeListUserName=userName) & (Q(classification="전선") | Q(classification="전필"))):
            user_Take_list.append(takeList.lectureNumber)

        for trackBasic in Track.objects.filter(Q(eduYear=2019) & Q(trackName="IT융합시스템개발") & Q(seperate="트랙기본")):
            db_Basic_list.append(trackBasic.lectureNum)

        for trackAdvance in Track.objects.filter(Q(eduYear=2019) & Q(trackName="IT융합시스템개발") & Q(seperate="트랙심화")):
            db_Advance_list.append(trackAdvance.lectureNum)

        # 트랙기본 이수 개수 확인
        for db_Basic in db_Basic_list:
            if db_Basic in user_Take_list:
                user_takeBasic_point += Track.objects.get(Q(lectureNum=db_Basic) & Q(eduYear=2019) & Q(trackName="IT융합시스템개발") & Q(seperate="트랙기본")).lecturePoint
                user_takeTrack_list.append(TakeList.objects.get(Q(lectureNumber=db_Basic) & Q(takeListUserName=userName)))

        if user_takeBasic_point >= total_track_Basic:
            resultValue_str+="트랙기본 이수 / "
        else:
            resultValue_str+="트랙기본 {0}학점이 부족합니다./ ".format(total_track_Basic - user_takeBasic_point)

        # 트랙심화 이수 개수 확인
        for db_Advance in db_Advance_list:
            if db_Advance in user_Take_list:
                user_takeAdvance_point += Track.objects.get(Q(lectureNum=db_Advance) & Q(eduYear=2019) & Q(trackName="IT융합시스템개발") & Q(seperate="트랙심화")).lecturePoint
                user_takeTrack_list.append(TakeList.objects.get(Q(lectureNumber=db_Advance) & Q(takeListUserName=userName)))

        if user_takeAdvance_point >= total_track_Advance:
            resultValue_str+="트랙심화 이수"
        else:
            resultValue_str+="트랙심화 {0}학점이 부족합니다.".format(total_track_Advance - user_takeAdvance_point)

        return resultValue_str, user_takeTrack_list