from django.db.models import Q
from graduate.models import BasicList
from accounts.models import TakeList
# 기초과정 확인
# 외국어 영역 =>ZGA1 번으로 시작
# 고정과목 경영정보 기준 모두 동일


def checkBasic(userName, studentId, studentMajor):
    compareBasicNameList = []
    userBasicNameList = []
    notTakeList = []
    takeList = []

    foreign = 0 #외국어 영역 체크
    humanAndSocial = 0 # 인문사회영역 체크 for 경영대

    # 사용자의 기초교양 수강리스트 과목명만 저장. filter는 쿼리셋, get은 오브젝트 get은 하나만 리턴.
    for userBasic in TakeList.objects.filter(Q(takeListUserName=userName) & Q(classification='기초')):
        userBasicNameList.append(userBasic.lectureName)
        # 외국어 영역을 위해 체크, elif의 경우 경영학과를 위해서 체크
        if userBasic.lectureNumber[3:4] == '1':
            foreign += 1
        elif userBasic.lectureNumber[3:4] == '2':
            humanAndSocial += 1

    # 고정과목 = 외국여영역중 택1이 아닌 과목명으로 제한된 과목
    # 고정 과목리스트 받기 / 학과의 전공에따라 DB에서 가져온다. 고로 if문이 필요없고
    # 기초교양의 고정과목이 바뀌어도 로직은 그대로, DB만 수정해주면 된다.
    for compareBasic in BasicList.objects.filter(Department=studentMajor):
        compareBasicNameList.append(compareBasic.Lecture_Name)


    for userBasicName in userBasicNameList:
        if userBasicName in compareBasicNameList:
            takeList.append(userBasicName)
    for compareBasicName in compareBasicNameList:
        if compareBasicName not in userBasicNameList:
            notTakeList.append(compareBasicName)

    # 외국어 영역 처리 경영학과 따로 구분하기 얘는 DB에서 처리 못해
    if foreign == 0:
        if studentMajor == '경영학과':
            notTakeList.append('외국어 영역 2과목 부족')
        else:
            notTakeList.append('외국어 영역 1과목 부족')
    elif foreign ==1:
        if studentMajor == '경영학과':
            notTakeList.append('외국어 영역 1과목 부족')
        else:
            takeList.append('외국어 영역 완료')
    elif foreign >= 2:
            takeList.append('외국어 영역 완료')

    # 경영학과 인문사회 영역 처리
    if studentMajor == '경영학과':
        if humanAndSocial == 0:
            notTakeList.append('인문사회영역 5과목 부족')
        elif humanAndSocial == 1:
            notTakeList.append('인문사회영역 4과목 부족')
        elif humanAndSocial == 2:
            notTakeList.append('인문사회영역 3과목 부족')
        elif humanAndSocial == 3:
            notTakeList.append('인문사회영역 2과목 부족')
        elif humanAndSocial == 4:
            notTakeList.append('인문사회영역 1과목 부족')
        elif humanAndSocial >= 5:
            takeList.append('인문사회영역 5과목 이수')
    # 다중 리턴
    return notTakeList, takeList

    # 외국어 영역 처리만 따로 해줘야 할 듯
    # elif studentMajor == '경영학과':
    # elif studentMajor == '국제통상학과':
    # elif studentMajor == '회계학과':