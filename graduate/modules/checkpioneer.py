
# 꿈미래
# 14년도 1학기 꿈미래 ZDA90117 1학점
# 그 이후            ZDA90127 0.5학점
# 17년도 이후 ZPA10001
# 학점 => ZDA90117 가진 경우 3학점인정 그 이후 모두 0.5학점 인정
# 횟수 => 14학번은 3번, 그 이후 4번

# 17학번 이전인 경우 꿈미래 개척만
# 17학번 이후인 경우 꿈미래 개척,
from django.db.models import Q

from accounts.models import TakeList


def checkDream(userName, studentId, studentMajor):
    max = 0
    point = 0
    dreamCnt = 0

    dreamlist = TakeList.objects.filter(Q(takeListUserName=userName) & Q(lectureName='꿈·미래개척'))
    # 14년도 1학기에 들었는지 체크, 인정학점 계산.
    for dream in dreamlist:
        if dream.lectureNumber == 'ZDA90117':
            max = 3
            point = 0.5      # 14학년도 1학기 1학점, 0.5로 계산하는 이유 밑의 for문에서 다시 계산하기 때문
            break            # if문을 사용하기 싫어서
        else:
            max = 2

    # 모든 학년 통틀어서 사용자가들은 꿈미래 개척 카운트
    for dream in dreamlist:
        if dream.lectureName == '꿈·미래개척':
            point += 0.5
            dreamCnt += 1
    print(point)
    print(dreamCnt)

    #14년도 1학기 꿈미래들은 경우
    if max == 3 and point >= max:
        return '꿈미래 상담 이수완료, 들은학점 = %s, 인정 학점 = %s, 차감해야하는 학점 = %s' % (point, max, (point-max))
    elif max == 3 and point < max and dreamCnt >= 3:
        return '꿈미래 상담 이수완료, 들은학점 = %s, 인정 학점 = %s,' % (point, point)
    elif max == 3 and dreamCnt < 3:
        return '꿈미래 상담 이수필요 %s번 더 이수 필요' % (3-dreamCnt)

    # 14학년도 1학기 안들은 경우 2학점 인정, 3번 들어야됨
    # elif max == 2 and studentId == 2014 and dreamCnt == 3:
    #     return '꿈미래 상담 이수완료, 들은학점 = %s, 인정 학점 = %s, 차감해야하는 학점 = %s' % (point, max, 0)
    # elif max == 2 and studentId == 2014 and dreamCnt > 3:
    #     return '꿈미래 상담 이수완료, 들은학점 = %s, 인정 학점 = %s, 차감해야하는 학점 = %s' % (point, max, (point - max))
    # elif max == 2 and studentId == 2014 and dreamCnt < 3:
    #     return '꿈미래 상담 이수필요 %s번 더 이수 필요' % (3 - dreamCnt)

    # 15학번부터 4번 들어야한다.
    elif max == 2 and dreamCnt >= 4:
        return '꿈미래 상담 이수완료, 들은학점 = %s, 인정 학점 = %s, 차감해야하는 학점 = %s' % (point, max, (point - max))
    elif max == 2 and dreamCnt < 4:
        return '꿈미래 상담 이수필요 %s번 더 이수 필요' % (4 - dreamCnt)

# 17학번 이전 개척 교양 => 존재하지 않는다.
# 17학번 이후 개척 교양 => 과목2개 학점 4학점 채워야 됨
# 나중에 생각하자

def checkPioneer(userName, studentId, studentMajor):

    userPioneerList = []
    requiredPoint = 4
    point = 0
    if studentId < 2017:
        return '2017년도 교육과정 이전 대상자는 해당 되지 않습니다.'

    # Q(takeListUserName=userName) & Q(classification='개교')
    # DB에서 꿈미래 빼고 개척교양 받아오기
    for userPioneer in TakeList.objects.filter(Q(takeListUserName=userName) & Q(classification='개교')):
        if userPioneer.lectureName != '꿈·미래개척':
            point += userPioneer.lecturePoint

    # userPioneerList.append(userPioneer)
    if point >= requiredPoint:
        return '꿈 미래 개척을 제외한 개척교양을 모두 채웠습니다 수강학점 %s' % point
    elif point < requiredPoint:
        return '꿈 미래 개척을 제외한 개척교양을 더 수강 해야 합니다. 추가로 필요한 학점 %s' % (requiredPoint-point)





#    for userPioneer in TakeList.objects.filter(Q(takeListUserName=userName) & Q(classification='개척')):
# for userPioneer in TakeList.objects.filter(classification='개교'):
















