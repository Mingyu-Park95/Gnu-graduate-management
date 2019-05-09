
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

# 2.전공 필수 과목
#

# 국제 통상 학과 학생이 복수전공하는 경우 우선 전공 적용 필요
# 그외 학생들은 해당 교육과정의 해당 학과 복수전공 학점을 확인하면 된다.
#
#
from django.db.models import Q

from accounts.models import TakeListPoint, TakeList
from graduate.models import MajorPoint


def checkMajor(userName, eduYear, studentMajor, studentDoubleMajor, studentSubMajor):
    majorResult = ''
    majorChecker = MajorPoint.objects.get(Q(major=studentMajor) & Q(eduYear=eduYear))
    userMajor = TakeListPoint.objects.get(TakeListPointUserName=userName)

    # 단일 전공자
    if studentDoubleMajor=='해당없음'and studentSubMajor =='해당없음':
        if majorChecker.majorPoint > userMajor.major:
            majorResult = '전필을 %s학점 더 들어야 합니다.' % (majorChecker.majorPoint - userMajor.major)
        else:
            majorResult = '전필을 모두 이수하였습니다. 이수학점 = %s' % userMajor.major

        #####
        if majorChecker.majorSelectPoint > userMajor.majorSelect:
            majorResult += '전선을 %s학점 더 들어야 합니다.' % (majorChecker.majorSelectPoint - userMajor.majorSelect)
        else:
            majorResult += '전선을 모두 이수하였습니다. 이수학점 = %s' % userMajor.majorSelect

    # 사용자가 들은 전필,전선과 해당하는 복수전공 모든 과목을 비교하여 학점을 더하고 9학점이 넘으면
    # 이필, 이선 학점에서 해당과목 제외




    # 국제통상학과 학생이 복수 전공하는 경우
    elif studentMajor == '국제통상학과' and studentDoubleMajor !='해당없음' and studentSubMajor =='해당없음':
        # 2017년 기준으로 국제통상학과는 "우선전공"과"복수전공"이 나뉜다.
        if eduYear < 2017:
            majorChecker = MajorPoint.objects.get(Q(major=studentMajor) & Q(eduYear=eduYear))
        else:
            majorChecker = MajorPoint.objects.get(Q(major='국제통상학과-우선') & Q(eduYear=eduYear))
        doubleMajorChecker = MajorPoint.objects.get(Q(major=studentDoubleMajor) & Q(eduYear=eduYear))

        # 전필
        if majorChecker.dmajorPoint > userMajor.dmajor:
            majorResult = '전필을 %s학점 더 들어야 합니다.' % (majorChecker.dmajorPoint - userMajor.dmajor)
        else:
            majorResult = '전필을 모두 이수하였습니다. 이수학점 = %s' % userMajor.dmajor
        # 전선
        if majorChecker.dmajorSelectPoint > userMajor.dmajorSelect:
            majorResult += '전선을 %s학점 더 들어야 합니다.' % (majorChecker.dmajorSelectPoint - userMajor.dmajorSelect)
        else:
            majorResult += '전선을 모두 이수하였습니다. 이수학점 = %s' % userMajor.dmajorSelect
        # 이필
        if doubleMajorChecker.dmajorPoint > userMajor.dmajor:
            majorResult += '이필을 %s학점 더 들어야 합니다.' % (doubleMajorChecker.dmajorPoint - userMajor.dmajor)
        else:
            majorResult += '이필을 모두 이수하였습니다. 이수학점 = %s' % userMajor.dmajor
        # 이선
        if doubleMajorChecker.dmajorSelectPoint > userMajor.dmajorSelect:
            majorResult += '이선을 %s학점 더 들어야 합니다.' % (doubleMajorChecker.dmajorSelectPoint - userMajor.dmajorSelect)
        else:
            majorResult += '이선을 모두 이수하였습니다. 이수학점 = %s' % userMajor.dmajorSelect

    # 복수 전공 하되, 국제통상 아닌 경우
    elif studentDoubleMajor !='해당없음' and studentSubMajor =='해당없음':
        # 복수전공 학점확인
        doubleMajorChecker = MajorPoint.objects.get(Q(major=studentDoubleMajor) & Q(eduYear=eduYear))

        userTakeList = TakeList.objects.filter(Q(takeListUserName=userName) & Q(classification='전필') | Q(classification='전선'))



        # 전필
        if majorChecker.dmajorPoint > userMajor.dmajor:
            majorResult = '전필을 %s학점 더 들어야 합니다.' % (majorChecker.dmajorPoint - userMajor.dmajor)
        else:
            majorResult = '전필을 모두 이수하였습니다. 이수학점 = %s' % userMajor.dmajor
        # 전선
        if majorChecker.dmajorSelectPoint > userMajor.dmajorSelect:
            majorResult += '전선을 %s학점 더 들어야 합니다.' % (majorChecker.dmajorSelectPoint - userMajor.dmajorSelect)
        else:
            majorResult += '전선을 모두 이수하였습니다. 이수학점 = %s' % userMajor.dmajorSelect
        # 이필
        if doubleMajorChecker.dmajorPoint > userMajor.dmajor:
            majorResult += '이필을 %s학점 더 들어야 합니다.' % (doubleMajorChecker.dmajorPoint - userMajor.dmajor)
        else:
            majorResult += '이필을 모두 이수하였습니다. 이수학점 = %s' % userMajor.dmajor
        # 이선
        if doubleMajorChecker.dmajorSelectPoint > userMajor.dmajorSelect:
            majorResult += '이선을 %s학점 더 들어야 합니다.' % (doubleMajorChecker.dmajorSelectPoint - userMajor.dmajorSelect)
        else:
            majorResult += '이선을 모두 이수하였습니다. 이수학점 = %s' % userMajor.dmajorSelect
        # 필수 과목




    # return majorResult

            #
            # class MajorPoint(models.Model):
            #     eduYear = models.IntegerField()  # 교육과정
            #     major = models.CharField(max_length=20)  # 학과
            #     majorPoint = models.FloatField()  # 전필
            #     majorSelectPoint = models.FloatField()  # 전선
            #     dmajorPoint = models.FloatField()  # 이필
            #     dmajorSelectPoint = models.FloatField()  # 이선
            #     subMajorPoint = models.FloatField()  # 부전공

            # class TakeListPoint(models.Model):
            #     TakeListPointUserName = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
            #     capability = models.FloatField(verbose_name='역량학점')
            #     integration = models.FloatField(verbose_name='통합학점')
            #     basic = models.FloatField(verbose_name='기초학점')
            #     general = models.FloatField(verbose_name='일반학점')
            #     pioneer = models.FloatField(verbose_name='개척학점')
            #     majorSelect = models.FloatField(verbose_name='전선학점')
            #     major = models.FloatField(verbose_name='전필학점')
            #     dmajorSelect = models.FloatField(verbose_name='이선학점')
            #     dmajor = models.FloatField(verbose_name='이필')
            #     total = models.FloatField(verbose_name='전체학점')