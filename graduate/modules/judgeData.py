from graduate.models import *

from accounts.models import *
from django.db.models import Q

from django.http import HttpResponse

def Integration_Judge(user_name,user_num,user_major): #이수여부 판단

    db_integrat = IntegrationList.objects.all()  # 이수해야할 통합교양
    user_integrat = TakeList.objects.all().filter(Q(classification="핵심") | Q(classification="통교"))  # 사용자가 들은 통합교양

    integrate_Name_list = [] # 통합교양 이름

    db_lectureNum_list =[] # 1~7 까지 핵심교양 학수번호를 리스트에
    user_lectureNum_list = [] # 사용자가 들은 핵심교양 학수번호를 리스트에

    noTake_Num_list = [] # 듣지 않은 통합교양 학수번호 리스트
    resultToView = []

    for db in db_integrat: # db에 있는 통합교양 학수번호와 과목명을 리스트에 삽입

        integrate_Name_list.append(db.lectureName)
        db_lectureNum_list.append(db.lectureName)

    for user in user_integrat: # 사용자가 들은 통합교양 리스트에 삽입
        user_lectureNum_list.append(user.lectureNumber[3:4])


    for db_lectureNum in db_lectureNum_list: # db와 사용자 통합교양 비교를 통해 듣지 않은 수강과목 학수번호 추출
        if db_lectureNum not in user_lectureNum_list:
            noTake_Num_list.append(db_lectureNum)

    if len(noTake_Num_list) > 2: # 듣지 않은 수강과목 수가 2개보다 많다면 듣지 않은 영역 표시
        for noTake in noTake_Num_list:
            resultToView.append(IntegrationList.objects.get(lectureNum=noTake).lectureName)
        return resultToView
    else:
        resultToView.append("통합교양을 이수하셨습니다.")
        return resultToView


def Capability_Judge(user_name,user_num,user_major): #역량교양 판별(14 경정만)
    user_list = []
    db_list = []
    noTake_list = []  # 사용자가 듣지 않은 과목 추출
    select_list = []  # 선택과목만 따로 담음
    count = 0  # 핵심교양 선택과목 이수 개수 확인
    resultToView =[]

    if int(user_num) <= 2016 and int(user_num) >=13: # 교육과정 17 이전
        db_capable = CapabilityList.objects.filter(Edu_Year=13)  # 들어야할 공통 교양
        user_capable = TakeList.objects.all().filter(Q(classification="공교") | Q(classification="역교"))  # 사용자가 들은 공통교양

        for capable in db_capable:  # db_list에 들어야할 공통교양 삽입
            db_list.append(capable.lectureName)

        for capable2 in user_capable:  # user_list에 사용자가 들은 공통교양 삽입
            user_list.append(capable2.lectureName)

        for i in db_list:  # db_list 과 user_list 비교를 통해 듣지 않은 수강과목 추출
            if i not in user_list:
                noTake_list.append(i)

        if db_list[1] not in noTake_list and db_list[2] not in noTake_list:  # 대학영어를 다 들었고, English존 안들었을때
            if (db_list[3] not in noTake_list):  # 인사글을 들었다면
                if db_list[4] not in noTake_list or db_list[5] not in noTake_list or db_list[6] not in noTake_list:  # 비사, 인성, 수통 중 하나라도 들었다면
                    return HttpResponse("공통(역량)교양을 이수 하셨습니다")
                else:
                    return HttpResponse("{0} / {1} / {2} 중 1개를 이수 하셔야 합니다.".format(db_list[4], db_list[5], db_list[6]))
            else:  # 인사글 안들었다면
                if db_list[4] not in noTake_list or db_list[5] not in noTake_list or db_list[6] not in noTake_list:  # 비사, 인성, 수통 중 하나라도 들었다면
                    return HttpResponse("{0}을 이수하셔야 합니다".format(db_list[3]))
                else:
                    return HttpResponse("{0}을 이수하셔야 하고 {1} / {2} / {3} 중 1개를 이수 하셔야 합니다.".format(db_list[3],db_list[4], db_list[5], db_list[6]))

        elif db_list[0] not in noTake_list:  # English존 들었을때
            if (db_list[3] not in noTake_list):  # 인사글을 들었다면
                if db_list[4] not in noTake_list or db_list[5] not in noTake_list or db_list[6] not in noTake_list:  # 비사, 인성, 수통 중 하나라도 들었다면
                    return HttpResponse("공통(역량)교양을 이수 하셨습니다")
                else:
                    return HttpResponse("/{0} / {1} / {2} 중 1개를 이수 하셔야 합니다.".format(db_list[4], db_list[5], db_list[6]))
            else:  # 인사글 안들었다면
                if db_list[4] not in noTake_list or db_list[5] not in noTake_list or db_list[6] not in noTake_list:  # 비사, 인성, 수통 중 하나라도 들었다면
                    return HttpResponse("{0}을 이수하셔야 합니다".format(db_list[3]))
                else:
                    return HttpResponse("{0}을 이수하셔야 하고 {1}/ {2}/ {3} 중 1개를 이수 하셔야 합니다.".format(db_list[3], db_list[4], db_list[5],db_list[6]))

        #elif db_list[1] in str and db_list[2] not in str:
        #elif db_list[1] not in str and db_list[2] in str:


        else:  # 대학영어, 잉글리시존 둘다 만족 못했을 시
            if (db_list[3] not in noTake_list):  # 인사글을 들었다면
                if db_list[4] not in noTake_list or db_list[5] not in noTake_list or db_list[6] not in noTake_list:  # 비사, 인성, 수통 중 하나라도 들었다면
                    return HttpResponse("{0} 혹은 {1}, {2} 과목을 이수 하셔야 합니다.".format(db_list[0], db_list[1], db_list[2]))
                else:
                    return HttpResponse("{0} 혹은 {1}, {2} 과목을 이수 하셔야 하고 /{3} / {4} / {5} 중 1개를 이수 하셔야 합니다.".format(db_list[1], db_list[2],db_list[3], db_list[4],db_list[5], db_list[6]))
            else:  # 인사글 안들었다면
                if db_list[4] not in noTake_list or db_list[5] not in noTake_list or db_list[6] not in noTake_list:  # 비사, 인성, 수통 중 하나라도 들었다면
                    return HttpResponse("{0} 혹은 {1} {2} 과목을 이수 하셔야 하고 {3} 과목을 수강하셔야 합니다.".format(db_list[0],db_list[1],db_list[2],db_list[3]))
                else:
                    return HttpResponse("{0} 혹은 {1} {2} 과목을 이수, {3}과목 이수,  {4}/ {5}/ {6} 중 1개를 이수 하셔야 합니다.".format(db_list[0],db_list[1],db_list[2], db_list[3], db_list[4], db_list[5],db_list[6],))


    else:  # 17학번부터
        db_capable = CapabilityList.objects.filter(Edu_Year=17)  # 들어야할 공통 교양
        user_capable = TakeList.objects.all().filter(Q(classification="공교") | Q(classification="역교"))  # 사용자가 들은 공통교양

        for capable in db_capable:  # db_list에 들어야할 공통교양 삽입
            db_list.append(capable.lectureName)

        for capable2 in user_capable:  # user_list에 사용자가 들은 공통교양 삽입
            user_list.append(capable2.lectureName)

        for i in db_list:  # db_list 과 user_list 비교를 통해 듣지 않은 수강과목 추출
            if i not in user_list:
                noTake_list.append(i)

        for select in range(3,10): # 역량 선택과목 값들 저장
            select_list.append(db_list[select])

        for cnt in select_list:
            if cnt not in noTake_list:
                count +=1

        if db_list[0] not in noTake_list and db_list[1] not in noTake_list:  # 대학영어를 다 들었을 때
            if (db_list[2] not in noTake_list):  # 인사글을 들었다면
                if count >=2:  # 선택과목 요건 만족 했다면
                    return HttpResponse("공통(역량)교양을 이수 하셨습니다")
                else:
                    return HttpResponse("핵심선택과목 2개 이상 이수 하셔야 합니다")
            else:  # 인사글 안들었다면
                if count >=2:  # 선택과목 요건 만족 했다면
                    return HttpResponse("{0}을 이수하셔야 합니다".format(db_list[2]))
                else:
                    return HttpResponse("글쓰기 기초를 듣고 핵심선택과목 2개 이상 이수 하셔야 합니다")

        # 잉글리시 존 추가

        elif db_list[0] not in noTake_list or db_list[1] not in noTake_list :  # 대영 1,2 둘 중 하나 안들었을 때
            if (db_list[2] not in noTake_list):  # 인사글을 들었다면
                if count >=2:  # 선택과목 요건 만족 했다면
                    return HttpResponse("{0} 혹은 {1}을 이수하셔야 합니다. ".format(db_list[0],db_list[1]))
                else:
                    return HttpResponse("{0}혹은 {1}을 이수하시고 /{2} / {3} / {4} / {5} / {6} / {7} / {8} 중 2개를 이수 하셔야 합니다.".format(db_list[0],db_list[1],db_list[3], db_list[4], db_list[5],db_list[6],db_list[7],db_list[8],db_list[9]))
            else:  # 인사글 안들었다면
                if count >=2:  # 선택과목 요건 만족 했다면
                    return HttpResponse("{0}혹은 {1}을 이수하시고 {2}을 이수하셔야 합니다".format(db_list[0],db_list[1],db_list[2]))
                else:
                    return HttpResponse("{0}혹은 {1}을 이수하시고 {2}을 이수하시고 /{3} / {4} / {4} / {5} / {6} / {7} / {8} 중 2개를 이수 하셔야 합니다.".format(db_list[0],db_list[1],db_list[2],db_list[3], db_list[4], db_list[5],db_list[6],db_list[7],db_list[8],db_list[9]))

        else:  # 대학영어 둘다 안들었을 때
            if (db_list[2] not in noTake_list):  # 인사글을 들었다면
                if count >=2:  # 선택과목 요건 만족 했다면
                    return HttpResponse("대영 들어야 합니다")
                else:
                    return HttpResponse("대영과 선택과목 2개 이상 이수해야 합니다")
            else:  # 인사글 안들었다면
                if count >=2:  # 선택과목 요건 만족 했다면
                    return HttpResponse("대영, 글쓰기 기초 들어야 합니다")
                else:
                    return HttpResponse("대영,글쓰기 기초, 선택과목 2개 이상 이수해야 합니다.")
