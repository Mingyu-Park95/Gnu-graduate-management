
# 단일전공자의 경우 그냥 체크해주면 끝

# 복수전공 교육과정, 입학년도의 교육과정, 즉 기존의 교육과정을 받는다.

# 복수전공 학점 인정 범위
# 이미 이수한 전공 교과목이 우선이수전공 이외의 전공에서 개설한 교과목과 동일한 경우
# 그 이수학점을 다른 전공의 이수학점으로 9학점까지 중복인정 가능. 다만 연계전공의 경우는 12학점 까지 중복인정 가능


# 경영대 내의 복수 전공자.
# 1.우선 전공 복수전공 공통 9학점,
#   - 공통된 과목이 9학점인경우 => 전공인정, 복수전공 인정
#   - 공통된 과목이 12학점인경우 => 전공12인정, 복수전공 9학점 인정
#   =>중복된 과목 체크 => 사용자 수강목록에서 "전필,전선"으로 분류된 과목이 "복수전공과목"에 몇 학점 있는지
#       =>우선전공에 포함된 경우 "전필,전선"으로 표기될 것이다.
#   =>이필,이선과목    => 사용자 수강목록에서 학점 카운트
#
#   복수전공과목명단과 수강목록의 전필,전선 비교 9학점 이상이면 말해주기

# 2.복수 전공 필수 과목
#

# 3. 국제 통상 학과 학생이 복수전공하는 경우 우선 전공 적용 필요
# 그외 학생들은 해당 교육과정의 해당 학과 복수전공 학점을 확인하면 된다.
#
#
from django.db.models import Q

from accounts.models import TakeListPoint, TakeList
from graduate.models import MajorPoint, MajorList


def checkMajor(userName, eduYear, studentMajor, studentDoubleMajor, studentSubMajor):
    majorResult = ''
    majorPointChecker = MajorPoint.objects.get(Q(major=studentMajor) & Q(eduYear=eduYear))
    userMajorPoint = TakeListPoint.objects.get(TakeListPointUserName=userName)


    # 사용자가 들은 전필,전선과 해당하는 복수전공 모든 과목을 비교하여 학점을 더하고 9학점이 넘으면
    # 이필, 이선 학점에서 해당과목 제외

    # 국제통상학과 학생이 복수 전공하는 경우
    if studentMajor == '국제통상학과' and studentDoubleMajor != '해당없음' and studentSubMajor =='해당없음':

        # 2017년 기준으로 국제통상학과는 "우선전공"과"복수전공"이 나뉜다.
        if eduYear < 2017:
            majorPointChecker = MajorPoint.objects.get(Q(major=studentMajor) & Q(eduYear=eduYear))
        else:
            majorPointChecker = MajorPoint.objects.get(Q(major='국제통상학과-우선') & Q(eduYear=eduYear))

        # 사용자가 들은 전필, 전선
        userMajorList = TakeList.objects.filter(
            Q(TakeListUserName=userName) & Q(classification='전필') | Q(classification='전선'))

        # 복수전공자가 들어야하는 과목 = 복수전공하는 학과의 전필, 전선
        doubleMajorList = MajorList.get.filter(Q(major=studentDoubleMajor))  # 경영대 전공에서 사용자의 복수전공에 해당하는 강의들 받기

        # 복수전공 학점확인
        doubleMajorChecker = MajorPoint.objects.get(Q(major=studentDoubleMajor) & Q(eduYear=eduYear))

        diffMajorPoint = 0  # 이필 학점
        diffMajorSelectPoint = 0  # 이선 학점
        overlap = 0  # 주전공과 부전공이 겹치는 학점, 9학점을 넘으면 안된다.

        # 사용자가 들은 전공에서 복수전공의 과목이 몇 학점 있는지
        for userMajor in userMajorList:  # 사용자가 들은거.
            for doubleMajor in doubleMajorList:  # 복수전공 하는 과의 전필,전선
                if userMajor.lectureNumber == doubleMajor.lectureNum and doubleMajor.classification == '전필':  # 주전공 복수전공 겹치는 경우, 복수전공하는 학과에서 전필인 경우 이필학점 증가
                    diffMajorPoint += userMajor.lecturePoint
                    overlap += userMajor.lecturePoint
                    break  # 사용자가 들은 전필은 복수전공 전필들중 딱하나이다.
                elif userMajor.lectureNumber == doubleMajor.lectureNum and doubleMajor.classification == '전선':  # 주전공 복수전공 겹치는 경우,
                    diffMajorSelectPoint += userMajor.lecturePoint
                    overlap += userMajor.lecturePoint
                    break

        # 학수번호 같고, 전선 전필 달라진 과목 체크, 회계학과의 3과목이 유일
        if eduYear >= 2017 and studentDoubleMajor == '회계학과':
            for userMajor in userMajorList:
                if userMajor.lectureNumber == 'BIA20024' or 'BBA30017':  # 경정시,인적자원관리 학수번호
                    diffMajorPoint -= 3
                    diffMajorSelectPoint += 3

        if eduYear > 2014 and studentDoubleMajor == '회계학과':
            for userMajor in userMajorList:
                if userMajor.lectureNumber == 'BAA40040':
                    diffMajorPoint += 3
                    diffMajorSelectPoint -= 3
                    break



        # 전필
        if majorPointChecker.dmajorPoint > userMajorPoint.dmajor:
            majorResult = '전필 요구학점 %s, 수강한 학점 %s, 남은학점 %s' % (
                majorPointChecker.dmajorPoint, userMajorPoint.dmajor, majorPointChecker.dmajorPoint - userMajorPoint.dmajor)
        else:
            majorResult = '전필을 모두 이수 했습니다. 전필 요구학점 %s, 수강한 학점 %s, 남은학점 %s' % (
                majorPointChecker.dmajorPoint, userMajorPoint.dmajor, majorPointChecker.dmajorPoint - userMajorPoint.dmajor)
        # 전선
        if majorPointChecker.dmajorSelectPoint > userMajorPoint.dmajorSelect:
            majorResult += '전선 요구학점 %s, 수강한 학점 %s, 남은학점 %s' % (
                majorPointChecker.dmajorSelectPoint, userMajorPoint.dmajorSelect,
                majorPointChecker.dmajorSelectPoint - userMajorPoint.dmajorSelect)
        else:
            majorResult += '전선을 모두 이수 했습니다. 전선 요구학점 %s, 수강한 학점 %s, 남은학점 %s' % (
                majorPointChecker.dmajorSelectPoint, userMajorPoint.dmajorSelect,
                majorPointChecker.dmajorSelectPoint - userMajorPoint.dmajorSelect)

        userDmajorPoint = userMajorPoint.dmajor + diffMajorPoint
        userDselectPoint = userMajorPoint.dmajorSelect + diffMajorSelectPoint
        if overlap <= 9:
            if doubleMajorChecker.dmajorPoint > userDmajorPoint:
                majorResult += '이필 요구학점 %s, 수강한 학점 %s, 남은학점 %s, 주전공과 겹치는 학점 %s' % (
                    doubleMajorChecker.dmajorPoint, userDmajorPoint, doubleMajorChecker.dmajorPoint - userDmajorPoint,
                    diffMajorPoint)
            else:
                majorResult += '이필을 모두 이수하였습니다. 이필 요구학점 %s, 수강한 학점 %s, 남은학점 %s, 주전공과 겹치는 학점 %s' % (
                    doubleMajorChecker.dmajorPoint, userDmajorPoint, doubleMajorChecker.dmajorPoint - userDmajorPoint,
                    diffMajorPoint)
            # 이선
            if doubleMajorChecker.dmajorSelectPoint > userDselectPoint:
                majorResult += '이선 요구학점 %s, 수강한 학점 %s, 남은학점 %s, 주전공과 겹치는 학점 %s' % (
                    doubleMajorChecker.dmajorSelectPoint, userDselectPoint,
                    doubleMajorChecker.dmajorPoint - userDselectPoint, diffMajorSelectPoint)
            else:
                majorResult += '이선을 모두 이수하였습니다. 이선 요구학점 %s, 수강한 학점 %s, 남은학점 %s, 주전공과 겹치는 학점 %s' % (
                    doubleMajorChecker.dmajorSelectPoint, userDselectPoint,
                    doubleMajorChecker.dmajorPoint - userDselectPoint, diffMajorSelectPoint)
        else:  # 중복되는 학점이 9학점 초과시.
            # 이필
            majorResult += '주의 주전공과 복수전공 동시인정 학점은 "9학점까지" 입니다. 현재 중복학점 = %s' % overlap
            majorResult += '이필 요구학점 %s, 수강한 학점 %s, 주전공과 겹치는 학점 %s' % (
                doubleMajorChecker.dmajorPoint, userDmajorPoint, diffMajorPoint)
            # 이선
            majorResult += '이선 요구학점 %s, 수강한 학점 %s, 주전공과 겹치는 학점 %s' % (
                doubleMajorChecker.dmajorSelectPoint, userDselectPoint, diffMajorSelectPoint)

        # 사용자가 들은 이필, 이선 필수 과목 확인
        userDoubleMajorList = TakeList.objects.filter(
            Q(TakeListUserName=userName) & Q(classification='이필') | Q(classification='이선'))
        doubleMajorMustList = MajorList.get.filter(Q(major=studentDoubleMajor) | Q(checkDoubleMajor=1))
        MustTakeList = []
        for doubleMajor in doubleMajorMustList:
            MustTakeList.append(doubleMajor.lectureName)

        userMustTakeList = []

        for doubleMajorMust in doubleMajorMustList:
            for userDoubleMajor in userDoubleMajorList:
                if userDoubleMajor.lectureNumber == userDoubleMajor.lectureNum:
                    userMustTakeList.append(doubleMajorList.lectureName)
                    break
        return majorResult, MustTakeList, userMustTakeList


    # 복수 전공 하되, 국제통상 아닌 경우
    #   1.필수 과목 다 들었는지
    #   2.9학점 초과하는 지
    elif studentDoubleMajor !='해당없음' and studentSubMajor =='해당없음':
        # 사용자가 들은 전필, 전선
        userMajorList = TakeList.objects.filter(
            Q(TakeListUserName=userName) & Q(classification='전필') | Q(classification='전선'))

        # 복수전공자가 들어야하는 과목 = 복수전공하는 학과의 전필, 전선
        doubleMajorList = MajorList.get.filter(Q(major=studentDoubleMajor))  # 경영대 전공에서 사용자의 복수전공에 해당하는 강의들 받기

        # 복수전공 학점확인
        doubleMajorChecker = MajorPoint.objects.get(Q(major=studentDoubleMajor) & Q(eduYear=eduYear))

        diffMajorPoint = 0 # 이필 학점
        diffMajorSelectPoint =0 # 이선 학점
        overlap = 0  # 주전공과 부전공이 겹치는 학점, 9학점을 넘으면 안된다.

        # 사용자가 들은 전공에서 복수전공의 과목이 몇 학점 있는지
        for userMajor in userMajorList:  # 사용자가 들은거.
            for doubleMajor in doubleMajorList:  # 복수전공 하는 과의 전필,전선
                if userMajor.lectureNumber == doubleMajor.lectureNum and doubleMajor.classification=='전필': # 주전공 복수전공 겹치는 경우, 복수전공하는 학과에서 전필인 경우 이필학점 증가
                    diffMajorPoint += userMajor.lecturePoint
                    overlap += userMajor.lecturePoint
                    break # 사용자가 들은 전필은 복수전공 전필들중 딱하나이다.
                elif userMajor.lectureNumber == doubleMajor.lectureNum and doubleMajor.classification=='전선': # 주전공 복수전공 겹치는 경우,
                    diffMajorSelectPoint += userMajor.lecturePoint
                    overlap += userMajor.lecturePoint
                    break

        if eduYear >= 2017 and studentDoubleMajor == '회계학과':
            for userMajor in userMajorList:
                if userMajor.lectureNumber == 'BIA20024' or 'BBA30017': # 경정시,인적자원관리 학수번호
                    diffMajorPoint -= 3
                    diffMajorSelectPoint += 3

        if eduYear > 2014 and studentDoubleMajor == '회계학과':
            for userMajor in userMajorList:
                if userMajor.lectureNumber == 'BAA40040':
                    diffMajorPoint += 3
                    diffMajorSelectPoint -= 3
                    break

        # 전필
        if majorPointChecker.dmajorPoint > userMajorPoint.dmajor:
            majorResult = '전필 요구학점 %s, 수강한 학점 %s, 남은학점 %s' % (majorPointChecker.dmajorPoint, userMajorPoint.dmajor, majorPointChecker.dmajorPoint-userMajorPoint.dmajor)
        else:
            majorResult = '전필을 모두 이수 했습니다. 전필 요구학점 %s, 수강한 학점 %s, 남은학점 %s' % (majorPointChecker.dmajorPoint, userMajorPoint.dmajor, majorPointChecker.dmajorPoint-userMajorPoint.dmajor)
        # 전선
        if majorPointChecker.dmajorSelectPoint > userMajorPoint.dmajorSelect:
            majorResult += '전선 요구학점 %s, 수강한 학점 %s, 남은학점 %s' % (majorPointChecker.dmajorSelectPoint, userMajorPoint.dmajorSelect, majorPointChecker.dmajorSelectPoint-userMajorPoint.dmajorSelect)
        else:
            majorResult += '전선을 모두 이수 했습니다. 전선 요구학점 %s, 수강한 학점 %s, 남은학점 %s' % (majorPointChecker.dmajorSelectPoint, userMajorPoint.dmajorSelect, majorPointChecker.dmajorSelectPoint-userMajorPoint.dmajorSelect)

        userDmajorPoint = userMajorPoint.dmajor+diffMajorPoint
        userDselectPoint = userMajorPoint.dmajorSelect+diffMajorSelectPoint
        if overlap <= 9:
            if doubleMajorChecker.dmajorPoint > userDmajorPoint:
                majorResult += '이필 요구학점 %s, 수강한 학점 %s, 남은학점 %s, 주전공과 겹치는 학점 %s' % (doubleMajorChecker.dmajorPoint, userDmajorPoint, doubleMajorChecker.dmajorPoint-userDmajorPoint, diffMajorPoint)
            else:
                majorResult += '이필을 모두 이수하였습니다. 이필 요구학점 %s, 수강한 학점 %s, 남은학점 %s, 주전공과 겹치는 학점 %s' % (doubleMajorChecker.dmajorPoint, userDmajorPoint, doubleMajorChecker.dmajorPoint-userDmajorPoint, diffMajorPoint)
            # 이선
            if doubleMajorChecker.dmajorSelectPoint > userDselectPoint:
                majorResult += '이선 요구학점 %s, 수강한 학점 %s, 남은학점 %s, 주전공과 겹치는 학점 %s' % (doubleMajorChecker.dmajorSelectPoint, userDselectPoint, doubleMajorChecker.dmajorPoint-userDselectPoint, diffMajorSelectPoint)
            else:
                majorResult += '이선을 모두 이수하였습니다. 이선 요구학점 %s, 수강한 학점 %s, 남은학점 %s, 주전공과 겹치는 학점 %s' % (doubleMajorChecker.dmajorSelectPoint, userDselectPoint, doubleMajorChecker.dmajorPoint-userDselectPoint, diffMajorSelectPoint)
        else: # 중복되는 학점이 9학점 초과시.
            #이필
            majorResult += '주의 주전공과 복수전공 동시인정 학점은 "9학점까지" 입니다. 현재 중복학점 = %s' % overlap
            majorResult += '이필 요구학점 %s, 수강한 학점 %s, 주전공과 겹치는 학점 %s' % (
                doubleMajorChecker.dmajorPoint, userDmajorPoint, diffMajorPoint)
            # 이선
            majorResult += '이선 요구학점 %s, 수강한 학점 %s, 주전공과 겹치는 학점 %s' % (
                doubleMajorChecker.dmajorSelectPoint, userDselectPoint, diffMajorSelectPoint)

        # 사용자가 들은 이필, 이선 필수 과목 확인
        userDoubleMajorList = TakeList.objects.filter(
            Q(TakeListUserName=userName) & Q(classification='이필') | Q(classification='이선'))
        doubleMajorMustList = MajorList.get.filter(Q(major=studentDoubleMajor)|Q(checkDoubleMajor=1))
        MustTakeList = []
        userMustTakeList = []
        for doubleMajor in doubleMajorMustList:
            MustTakeList.append(doubleMajor.lectureName)



        for doubleMajorMust in doubleMajorMustList:
            for userDoubleMajor in userDoubleMajorList:
                if userDoubleMajor.lectureNumber == userDoubleMajor.lectureNum:
                    userMustTakeList.append(doubleMajorList.lectureName)
                    break

        return majorResult, MustTakeList, userMustTakeList
