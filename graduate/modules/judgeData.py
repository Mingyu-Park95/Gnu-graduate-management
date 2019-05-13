from graduate.models import *

from accounts.models import *
from django.db.models import Q

from django.http import HttpResponse

def Integration_Judge(userName,eduYear,studentMajor): #이수여부 판단

    integrate_Name_list = [] # 통합교양 이름

    db_lectureNum_list =[] # 1~7 까지 핵심교양 학수번호를 리스트에
    user_lectureNum_list = [] # 사용자가 들은 핵심교양 학수번호를 리스트에

    noTake_Num_list = [] # 듣지 않은 통합교양 학수번호 리스트
    resultValue = []

    for db in IntegrationList.objects.all(): # db에 있는 통합교양 학수번호와 과목명을 리스트에 삽입

        integrate_Name_list.append(db.lectureName)
        db_lectureNum_list.append(db.lectureNum)

    for user in TakeList.objects.all().filter((Q(classification="핵심") | Q(classification="통교")) & Q(takeListUserName=userName)): # 사용자가 들은 통합교양 리스트에 삽입
        user_lectureNum_list.append(user.lectureNumber[3:4])


    for db_lectureNum in db_lectureNum_list: # db와 사용자 통합교양 비교를 통해 듣지 않은 수강과목 학수번호 추출
        if db_lectureNum not in user_lectureNum_list:
            noTake_Num_list.append(db_lectureNum)

    if len(noTake_Num_list) > 2: # 듣지 않은 수강과목 수가 2개보다 많다면 듣지 않은 영역 표시
        for noTake in noTake_Num_list:
            resultValue.append(IntegrationList.objects.get(lectureNum=noTake).lectureName)
        return resultValue
    else:
        resultValue.append("통합교양을 이수하셨습니다.")
        return resultValue


def Capability_Judge(userName,eduYear,studentMajor): #역량교양 판별(14 경정만)
    user_list = []
    db_list = []
    noTake_list = []  # 사용자가 듣지 않은 과목 추출
    select_str = ''
    select_list = []  # 선택과목만 따로 담음
    count = 0  # 핵심교양 선택과목 이수 개수 확인

    result_value =[]

    for user in TakeList.objects.all().filter((Q(classification="공교") | Q(classification="역교")) & Q(
            takeListUserName=userName)):  # user_list에 사용자가 들은 공통교양 삽입
        user_list.append(user.lectureName)

    if int(eduYear) < 2017: # 교육과정 17 이전

        for db_capable in CapabilityList.objects.filter(eduYear=2014):  # db_list에 들어야할 공통교양 삽입
            db_list.append(db_capable.lectureName)

        for db in db_list:  # db_list 과 user_list 비교를 통해 듣지 않은 수강과목 추출
            if db not in user_list:
                noTake_list.append(db)

        for select_save in range(4, 7): # 역량 선택과목 값들 저장
            select_list.append(db_list[select_save])
            select_str += db_list[select_save] # 선택과목 값들 str 형으로 저장
            select_str += " / "

        for select in select_list: # 선택과목 들은 횟수 카운트
            if select not in noTake_list:
                count +=1

        if db_list[1] not in noTake_list and db_list[2] not in noTake_list:  # 대학영어 1,2 를 이수했을때
            if (db_list[3] not in noTake_list or db_list[6] not in noTake_list):  # 인사글을 들었고
                if count >=1:  # 비사, 인성, 수통 중 하나라도 들었다면
                    result_value.append("공통(역량) 교양을 이수 하셨습니다.")
                    return result_value
                else:
                    result_value.append("{0} 중 1개를 이수 하셔야 합니다.".format(select_str))
                    return result_value
            else:  # 인사글 안들었다면
                if count >=1:  # 비사, 인성, 수통 중 하나라도 들었다면
                    result_value.append("{0}을 이수하셔야 합니다".format(db_list[3]))
                    return result_value
                else:
                    result_value.append("{0}을 이수하셔야 하고 {1} 중 1개를 이수 하셔야 합니다.".format(db_list[3],select_str))
                    return result_value

        elif db_list[0] not in noTake_list:  # English존 들었을때
            if (db_list[3] not in noTake_list or db_list[6] not in noTake_list):  # 인사글을 들었고
                if count >=1:  # 비사, 인성, 수통 중 하나라도 들었다면
                    result_value.append("공통(역량)교양을 이수 하셨습니다")
                    return result_value
                else:
                    result_value.append("{0} 중 1개를 이수 하셔야 합니다.".format(select_str))
                    return result_value
            else:  # 인사글 안들었다면
                if count >=1:  # 비사, 인성, 수통 중 하나라도 들었다면
                    result_value.append("{0}을 이수하셔야 합니다".format(db_list[3]))
                    return result_value
                else:
                    result_value.append("{0}을 이수하셔야 하고 {1} 중 1개를 이수 하셔야 합니다.".format(db_list[3], select_str))
                    return result_value

        elif db_list[1] in noTake_list and db_list[2] not in noTake_list: # 대학영어 1을 안들었고 대학영어 2를 들었을 때
            if (db_list[3] not in noTake_list or db_list[6] not in noTake_list):  # 인사글을 들었고
                if count >=1:  # 비사, 인성, 수통 중 하나라도 들었다면
                    result_value.append("{0}을 이수하셔야 합니다.".format(db_list[1]))
                    return result_value
                else:
                    result_value.append("{0}을 이수하셔야 하고 {1} 중 1개를 이수 하셔야 합니다.".format(db_list[1],select_str))
                    return result_value
            else:  # 인사글 안들었다면
                if count >=1:  # 비사, 인성, 수통 중 하나라도 들었다면
                    result_value.append("{0}과 {1}을 이수하셔야 합니다".format(db_list[1],db_list[3]))
                    return result_value
                else:
                    result_value.append("{0}과 {1}을 이수하셔야 하고 {2} 중 1개를 이수 하셔야 합니다.".format(db_list[1],db_list[3], select_str))
                    return result_value

        elif db_list[1] not in noTake_list and db_list[2] in noTake_list: # 대학영어2 안들었을 때
            if (db_list[3] not in noTake_list or db_list[6] not in noTake_list):  # 인사글을 들었고
                if count >=1:  # 비사, 인성, 수통 중 하나라도 들었다면
                    result_value.append("{0}을 이수하셔야 합니다.".format(db_list[2]))
                    return result_value
                else:
                    result_value.append("{0}을 이수하셔야 하고 {1} 중 1개를 이수 하셔야 합니다.".format(db_list[2],select_str))
                    return result_value
            else:  # 인사글 안들었다면
                if count >=1:  # 비사, 인성, 수통 중 하나라도 들었다면
                    result_value.append("{0}과 {1}을 이수하셔야 합니다".format(db_list[2],db_list[3]))
                    return result_value
                else:
                    result_value.append("{0}과 {1}을 이수하셔야 하고 {2} 중 1개를 이수 하셔야 합니다.".format(db_list[2],db_list[3], select_str))
                    return result_value

        else:  # 대학영어, 잉글리시존 둘다 만족 못했을 시
            if (db_list[3] not in noTake_list or db_list[6] not in noTake_list):  # 인사글을 들었고
                if count >=1:  # 비사, 인성, 수통 중 하나라도 들었다면
                    result_value.append("{0} 혹은 {1}, {2} 과목을 이수 하셔야 합니다.".format(db_list[0], db_list[1], db_list[2]))
                    return result_value
                else:
                    result_value.append("{0} 혹은 {1}, {2} 과목을 이수 하셔야 하고 {3} 중 1개를 이수 하셔야 합니다.".format(db_list[1], db_list[2],db_list[3], select_str))
                    return result_value
            else:  # 인사글 안들었다면
                if count >=1:  # 비사, 인성, 수통 중 하나라도 들었다면
                    result_value.append("{0} 혹은 {1} {2} 과목을 이수 하셔야 하고 {3} 과목을 수강하셔야 합니다.".format(db_list[0],db_list[1],db_list[2],db_list[3]))
                    return result_value
                else:
                    result_value.append("{0} 혹은 {1} {2} 과목을 이수, {3}과목 이수, {4} 중 1개를 이수 하셔야 합니다.".format(db_list[0],db_list[1],db_list[2], db_list[3], select_str))
                    return result_value


    elif int(eduYear) >=2017 :  # 17학번부터

        for db_capable in CapabilityList.objects.filter(eduYear=2017):  # db_list에 들어야할 공통교양 삽입
            db_list.append(db_capable.lectureName)

        for db in db_list:  # db_list 과 user_list 비교를 통해 듣지 않은 수강과목 추출
            if db not in user_list:
                noTake_list.append(db)

        for select_save in range(4, 11): # 역량 선택과목 값들 저장
            select_list.append(db_list[select_save])
            select_str += db_list[select_save]  # 선택과목 값들 str 형으로 저장
            select_str += " / "

        for select in select_list:
            if select not in noTake_list:
                count +=1

        if db_list[1] not in noTake_list and db_list[2] not in noTake_list:  # 대학영어를 다 들었을 때
            if (db_list[3] not in noTake_list):  # 인사글을 들었다면
                if count >=2:  # 선택과목 요건 만족 했다면
                    result_value.append("공통(역량)교양을 이수 하셨습니다")
                    return result_value
                else:
                    result_value.append("{0} 중 2개를 이수 하셔야 합니다.".format(select_str))
                    return result_value
            else:  # 인사글 안들었다면
                if count >=2:  # 선택과목 요건 만족 했다면
                    result_value.append("{0}을 이수하셔야 합니다".format(db_list[3]))
                    return result_value
                else:
                    result_value.append("{0}을 이수하시고 {1} 중 2개를 이수하셔야 합니다.".format(db_list[3],select_str))
                    return result_value

        elif db_list[0] not in noTake_list:  # 잉글리시존 이수하였을때
            if (db_list[3] not in noTake_list):  # 인사글을 들었다면
                if count >=2:  # 선택과목 요건 만족 했다면
                    result_value.append("공통(역량)교양을 이수 하셨습니다")
                    return result_value
                else:
                    result_value.append("{0} 중 2개를 이수 하셔야 합니다.".format(select_str))
                    return result_value
            else:  # 인사글 안들었다면
                if count >=2:  # 선택과목 요건 만족 했다면
                    result_value.append("{0}을 이수하셔야 합니다".format(db_list[3]))
                    return result_value
                else:
                    result_value.append("{0}을 이수하시고 {1} 중 2개를 이수하셔야 합니다.".format(db_list[3],select_str))
                    return result_value

        elif db_list[1] in noTake_list and db_list[2] not in noTake_list :  # 대영 1 안들었을 때
            if (db_list[3] not in noTake_list):  # 인사글을 들었다면
                if count >=2:  # 선택과목 요건 만족 했다면
                    result_value.append("{0}을 이수하셔야 합니다. ".format(db_list[1]))
                    return result_value
                else:
                    result_value.append("{0}을 이수하시고 {1} 중 2개를 이수 하셔야 합니다.".format(db_list[1],select_str))
                    return result_value
            else:  # 인사글 안들었다면
                if count >=2:  # 선택과목 요건 만족 했다면
                    result_value.append("{0}과 {1}를 이수하셔야 합니다.".format(db_list[1],db_list[3]))
                    return result_value
                else:
                    result_value.append("{0}을 이수, {1}를 이수, {2} 중 2개를 이수 하셔야 합니다.".format(db_list[1],db_list[3],select_str))
                    return result_value

        elif db_list[1] not in noTake_list and db_list[2] in noTake_list :  # 대영 2 안들었을 때
            if (db_list[3] not in noTake_list):  # 인사글을 들었다면
                if count >=2:  # 선택과목 요건 만족 했다면
                    result_value.append("{0}을 이수하셔야 합니다. ".format(db_list[2]))
                    return result_value
                else:
                    result_value.append("{0}을 이수하시고 {1} 중 2개를 이수 하셔야 합니다.".format(db_list[2],select_str))
                    return result_value
            else:  # 인사글 안들었다면
                if count >=2:  # 선택과목 요건 만족 했다면
                    result_value.append("{0}과 {1}를 이수하셔야 합니다.".format(db_list[2],db_list[3]))
                    return result_value
                else:
                    result_value.append("{0}을 이수, {1}를 이수, {2} 중 2개를 이수 하셔야 합니다.".format(db_list[2],db_list[3],select_str))
                    return result_value

        else:  # 대학영어 잉글리시존 둘다 안들었을 때
            if (db_list[3] not in noTake_list):  # 인사글을 들었다면
                if count >=2:  # 선택과목 요건 만족 했다면
                    result_value.append("{0} 혹은 {1}, {2}을 이수하셔야 합니다.".format(db_list[0],db_list[1],db_list[2]))
                    return result_value
                else:
                    result_value.append("{0} 혹은 {1},{2}을 이수하고  {3} 중 2개를 이수 하셔야 합니다.".format(db_list[0],db_list[1],db_list[2],select_str))
                    return result_value
            else:  # 인사글 안들었다면
                if count >=2:  # 선택과목 요건 만족 했다면
                    result_value.append("{0} 혹은 {1}, {2}을 이수하시고 {3}를 이수하셔야 합니다.".format(db_list[0],db_list[1],db_list[2],db_list[3]))
                    return result_value
                else:
                    result_value.append("{0} 혹은 {1},{2}을 이수하고 {3} 이수 {4} 중 2개를 이수 하셔야 합니다.".format(db_list[0],db_list[1],db_list[2],db_list[3],select_str))
                    return result_value

    else:
        HttpResponse("해당되는 교육과정이 아닙니다 ! ")