from graduate.models import *

from accounts.models import *
from django.db.models import Q

from django.http import HttpResponse

def convergenceMajor_Judge(userName,eduYear,studentMajor):
    totalEssential_point = 15 # 융합전공 전필 채워야하는 학점
    totalSelect_point = 21 # 융합전공 전선 채워야하는 학점

    db_essentialName_list = []  # 전필 과목명 담을 리스트
    db_selectNum_list = []  # 전선 학수번호 담을 리스트

    user_essentialMajorNum_list =[] # 사용자가 들은 전필 학수번호
    user_selectNum_list = []  # 사용자가 들은 전선 학수번호 담을 리스트
    user_essentialDmajorName_list =[] # 사용자가 들은 이필 과목명 담을 리스트 -> db_essentialName_list 와 비교

    mulitiApprove_list =[] # 복수인정 해당되는 과목
    noTake_list = [] # 사용자가 듣지 않은 이필 담을 리스트
    noTake_str ='' # 마지막 str 값으로 전필 미이수 과목 반환
    user_essential_point =0 # 사용자가 들은 이필학점
    user_select_point =0 # 사용자가 들은 이선 학점

    potenital_select =0 # 복수인정 초과 과목 개수
    resultValue =[] # return 해주는 변수

    for user_essentialMajorNum in TakeList.objects.all().filter(Q(classification="전필") & Q(takeListUserName=userName)): # 사용자가 들은 전필
        user_essentialMajorNum_list.append(user_essentialMajorNum.lectureNumber)

    for user_essentialDmajor in TakeList.objects.all().filter(Q(classification="이필") & Q(takeListUserName=userName)): # 사용자가 들은 이필
        user_essentialDmajorName_list.append(user_essentialDmajor.lectureName)

    for user_select in TakeList.objects.all().filter((Q(classification="이선") | Q(classification="전선")) & Q(takeListUserName=userName)): # 사용자가 들은 전선
        user_selectNum_list.append(user_select.lectureNumber)

    if int(eduYear) <2019:

        for db_essential in ConvergenceMajor.objects.all().filter(Q(seperate="전필") & Q(eduYear=2018)): # 융합전공 전필 과목명 리스트에
            db_essentialName_list.append(db_essential.dmajorName)

        for db_select in ConvergenceMajor.objects.all().filter(Q(seperate="전선") & Q(eduYear=2018)): # 융합전공 전선 학수번호 리스트에
            db_selectNum_list.append(db_select.dmajornum)

        # 이필 15학점 이수 여부 확인
        for db_essentialName in db_essentialName_list:
            if db_essentialName not in user_essentialDmajorName_list:
                noTake_list.append(db_essentialName)
                noTake_str += db_essentialName
                noTake_str += " / "

        if len(noTake_list) ==0: # 이필 전부 이수시 리스트 길이 0
            user_essential_point = 15
        else: # 남은 학점 계산
            user_essential_point = 15- (len(noTake_list) * 3) # 들은 이필 학점 계산

        # 이선 21학점 이수 여부 확인 / 복수 인정 과목 확인
        for user_essentialMajorNum in user_essentialMajorNum_list:
            if user_essentialMajorNum in db_selectNum_list:
               mulitiApprove_list.append(user_essentialMajorNum)

        if len(mulitiApprove_list) >4: # 복수인정과목을 4개 이상 들었을 때 판별
            user_select_point = 12
            potenital_select = len(mulitiApprove_list) - 4
        else:
            user_select_point = len(mulitiApprove_list) * 3

        for db_selectNum in db_selectNum_list:  # 이수해야할 이선 과목들이 사용자 전선 과목에 다 있다면 들은 학점 계산 (이선과목을 다 이수 했다면)
            if db_selectNum in user_selectNum_list:
                user_select_point += ConvergenceMajor.objects.get(Q(dmajornum=db_selectNum) & Q(eduYear=2018)).dmajorPoint

        resultValue.append("융합전공 이필 이수 학점 : {0}/{1}, 이선 인정학점 : {2}/{3}, 전필 미이수 과목 : {4}, 이선으로 옮길 수 있는 과목 수 {5}".format(user_essential_point,
                                                                                                       totalEssential_point,
                                                                                                       user_select_point,
                                                                                                       totalSelect_point,noTake_str,
                                                                                                       potenital_select))
        return resultValue

    else: # 교육과정 19년 이후
        for db_essential in ConvergenceMajor.objects.all().filter(
                Q(seperate="전필") & Q(eduYear=2019)):  # 융합전공 전필 과목명 리스트에
            db_essentialName_list.append(db_essential.dmajorName)

        for db_select in ConvergenceMajor.objects.all().filter(Q(seperate="전선") & Q(eduYear=2019)):  # 융합전공 전선 학수번호 리스트에
            db_selectNum_list.append(db_select.dmajornum)

            # 이필 15학점 이수 여부 확인
            for db_essentialName in db_essentialName_list:
                if db_essentialName not in user_essentialDmajorName_list:
                    noTake_list.append(db_essentialName)
                    noTake_str += db_essentialName
                    noTake_str += " / "

        if len(noTake_list) == 0:  # 이필 전부 이수시 리스트 길이 0
            user_essential_point = 15
        else:  # 남은 학점 계산
            user_essential_point = 15 - (len(noTake_list) * 3)  # 들은 이필 학점 계산

        # 이선 21학점 이수 여부 확인 / 복수 인정 과목 확인
        for user_essentialMajorNum in user_essentialMajorNum_list:
            if user_essentialMajorNum in db_selectNum_list:
                mulitiApprove_list.append(user_essentialMajorNum)

        if len(mulitiApprove_list) > 4:  # 복수인정과목을 4개 이상 들었을 때 판별
            user_select_point = 12
            potenital_select = len(mulitiApprove_list) - 4
        else:
            user_select_point = len(mulitiApprove_list) * 3

        for db_selectNum in db_selectNum_list:  # 이수해야할 이선 과목들이 사용자 전선 과목에 다 있다면 들은 학점 계산 (이선과목을 다 이수 했다면)
            if db_selectNum in user_selectNum_list:
                user_select_point += ConvergenceMajor.objects.get(
                    Q(dmajornum=db_selectNum) & Q(eduYear=2019)).dmajorPoint

        resultValue.append("융합전공 이필 이수 학점 : {0}/{1}, 이선 인정학점 : {2}/{3}, 전필 미이수 과목 : {4}, 이선으로 옮길 수 있는 과목 수 {5}".format(user_essential_point,
                                                                                       totalEssential_point,
                                                                                       user_select_point,
                                                                                       totalSelect_point,noTake_str,
                                                                                       potenital_select))
        return resultValue