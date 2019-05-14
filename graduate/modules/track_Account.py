from graduate.models import *
from accounts.models import *
from django.db.models import Q

def accountTrack_Judge(userName, eduYear, studentMajor):
    user_Take_list = []
    db_Basic_list = []
    db_Advance_list = []

    user_takeBasic_point = 0
    user_takeAdvance_point = 0
    resultValue = []

    total_track_Basic = 27
    total_track_Advance = 9

    for takeList in TakeList.objects.filter(
            Q(takeListUserName=userName) & (Q(classification="전선") | Q(classification="전필") | Q(classification="이필") | Q(classification="이선"))):
        user_Take_list.append(takeList.lectureNumber)

    for trackBasic in Track.objects.filter(Q(trackName="세무전문트랙") & Q(seperate="트랙기본")):
        db_Basic_list.append(trackBasic.lectureNum)

    for trackAdvance in Track.objects.filter(Q(trackName="세무전문트랙") & Q(seperate="트랙심화")):
        db_Advance_list.append(trackAdvance.lectureNum)

    # 트랙기본 이수 개수 확인
    for db_Basic in db_Basic_list:
        if db_Basic in user_Take_list:
            user_takeBasic_point += Track.objects.get(
                Q(lectureNum=db_Basic) & Q(trackName="세무전문트랙") & Q(seperate="트랙기본")).lecturePoint

    if user_takeBasic_point >= total_track_Basic:
        resultValue.append("트랙기본 이수 / ")
    else:
        resultValue.append("트랙기본 {0}학점이 부족합니다./ ".format(total_track_Basic - user_takeBasic_point))

    # 트랙심화 이수 개수 확인
    for db_Advance in db_Advance_list:
        if db_Advance in user_Take_list:
            user_takeAdvance_point += Track.objects.get(
                Q(lectureNum=db_Advance)& Q(trackName="세무전문트랙") & Q(seperate="트랙심화")).lecturePoint

    if user_takeAdvance_point >= total_track_Advance:
        resultValue.append("트랙심화 이수")
    else:
        resultValue.append("트랙심화 {0}학점이 부족합니다.".format(total_track_Advance - user_takeAdvance_point))

    return resultValue