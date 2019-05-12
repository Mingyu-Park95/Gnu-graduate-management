
from django.db.models import Q

from accounts.models import TakeListPoint, TakeList
from graduate.models import MajorPoint, MajorList


def checkMajor(userName, eduYear, studentMajor, studentDoubleMajor, studentSubMajor):
    majorResult = ''
    majorPointChecker = MajorPoint.objects.get(Q(major=studentMajor) & Q(eduYear=eduYear))
    userMajorPoint = TakeListPoint.objects.get(TakeListPointUserName=userName)

    # 단일 전공자
    if studentDoubleMajor=='해당없음'and studentSubMajor =='해당없음':
        if majorPointChecker.majorPoint > userMajorPoint.major:
            majorResult = '전필을 %s학점 더 들어야 합니다.' % (majorPointChecker.majorPoint - userMajorPoint.major)
        else:
            majorResult = '전필을 모두 이수하였습니다. 이수학점 = %s' % userMajorPoint.major

        #####
        if majorPointChecker.majorSelectPoint > userMajorPoint.majorSelect:
            majorResult += '전선을 %s학점 더 들어야 합니다.' % (majorPointChecker.majorSelectPoint - userMajorPoint.majorSelect)
        else:
            majorResult += '전선을 모두 이수하였습니다. 이수학점 = %s' % userMajorPoint.majorSelect

    return majorResult