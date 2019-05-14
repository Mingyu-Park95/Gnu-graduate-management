import xlrd
import xlwt
from collections import OrderedDict  # 중첩된 값 제거
from accounts.models import TakeList, CustomUser, TakeListPoint, GradeByPeriod


# 불러오는 과정


def makeTakeList(request):

    # 같은 아이디에 수강 정보가 계속 쌓이는 것을 막기 위해 파일 업로드시 해당 아이디의 수강 리스트 초기화
    fordel = TakeList.objects.filter(takeListUserName=request.user.username)
    fordel.delete()
    # 수강 기록에 대한 학점을 DB에서 삭제
    fordel = TakeListPoint.objects.filter(takeListPointUserName=request.user.username)
    fordel.delete()
    fordel = GradeByPeriod.objects.filter(gradeByPeriodName=request.user.username)
    fordel.delete()

    wb = xlrd.open_workbook('a/%s' % request.user.username)
    ws = wb.sheet_by_index(0)
    ncol = ws.ncols
    nlow = ws.nrows
    rowStart = 6


    i = rowStart
    j = 1
    low = []
    tmpStr = ''
    forTimeList = []
    list2 = []
    while i < nlow:
        while j <= 12:
            # 각 문자열의 모든 공백 제거
            a = str(ws.row_values(i)[j])
            a = a.replace(" ", "")
            a = a.strip()
            low.append(a)
            j += 1
        # low = " ".join(low)

        low = list(OrderedDict.fromkeys(low))  # list의 중복값 제거 (")제거

        low.remove("")  # (")을 위의 방법으로 제거하면 1개의 (")는 남는데 그것을 제거

        # 2개의 열을 병합한 셀의 경우 길이가 1인 공백리스트가 포함됨. 이를 제거
        if len(low) > 2 and low[0] != '신청' and low[0] != '구분':
            low[3] = float(low[3])  # 학점을 스트링에서 float 형으로 변환
            list2.append(low)

        elif len(low) > 0 and low[0] != '구분' and low[0] != '신청' and len(low[0]) < 60:
            if len(low[0]) >= 20:
                tmpStr = low[0][0:7] + " " + low[0][10:13] + " " + low[0][7:10]
                # print(tmpStr)
                forTimeList.append(tmpStr)
            if len(low[0]) < 20:
                tmpStr = low[0][0:7] + " " + low[0][7:13]
                # print(tmpStr)
                forTimeList.append(tmpStr)
        elif len(low) > 0 and low[0] == '신청':
            # print(low[6])
            forTimeList.append(low[6])

        low = []
        i += 1
        j = 1

    i = 6
    j = 13


    while i < nlow:
        while j <= 25:
            # 각 문자열의 모든 공백 제거
            a = str(ws.row_values(i)[j])
            a = a.replace(" ", "")
            a = a.strip()
            low.append(a)
            j += 1

        low = list(OrderedDict.fromkeys(low))

        low.remove("")

        if len(low) > 2 and low[0] != '신청' and low[0] != '구분':
            low[3] = float(low[3])  # 학점을 스트링에서 float 형으로 변환
            list2.append(low)

        elif len(low) > 0 and low[0] != '구분' and low[0] != '신청' and len(low[0]) < 60:
            if len(low[0]) >= 20:
                tmpStr = low[0][0:7] + " " + low[0][10:13] + " " + low[0][7:10]
                # print(tmpStr)
                forTimeList.append(tmpStr)
            if len(low[0]) < 20:
                tmpStr = low[0][0:7] + " " + low[0][7:13]
                # print(tmpStr)
                forTimeList.append(tmpStr)
        elif len(low) > 0 and low[0] == '신청':
            # print(low[6])
            forTimeList.append(low[6])
        low = []
        i += 1
        j = 13

    i = 6
    j = 26
    while i < nlow:
        while j <= 31:
            # 각 문자열의 모든 공백 제거
            a = str(ws.row_values(i)[j])

            a = a.replace(" ", "")
            a = a.strip()

            low.append(a)

            j += 1

        low = list(OrderedDict.fromkeys(low))
        # print(low)
        low.remove("")

        if len(low) > 2 and low[0] != '신청' and low[0] != '구분':
            low[3] = float(low[3])  # 학점을 스트링에서 float 형으로 변환
            list2.append(low)

        elif len(low) > 0 and low[0] != '구분' and low[0] != '신청' and len(low[0]) < 60:
            if len(low[0]) >= 20:
                tmpStr = low[0][0:7] + " " + low[0][10:13] + " " + low[0][7:10]
                # print(tmpStr)
                forTimeList.append(tmpStr)
            if len(low[0]) < 20:
                tmpStr = low[0][0:7] + " " + low[0][7:13]
                # print(tmpStr)
                forTimeList.append(tmpStr)
        elif len(low) > 0 and low[0] == '신청':
            # print(low[6])
            forTimeList.append(low[6])
        low = []
        i += 1
        j = 26
    forTimeList.pop()
    print(forTimeList)

    iter = len(forTimeList)//2
    for i in range(iter):
        gradeByPeriod = GradeByPeriod()
        gradeByPeriod.gradeByPeriodName = CustomUser.objects.get(pk=request.user.username)
        gradeByPeriod.period = forTimeList[2*i]
        gradeByPeriod.grade = forTimeList[2*i+1]
        gradeByPeriod.save()

    # 새로운 엑셀 파일 생성
    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet("test")

    # 과목 학점 카운트
    capability = 0  # 역량
    integration = 0  # 통합

    basic = 0  # 기초
    general = 0  # 일반
    pioneer = 0  # 개척
    majorSelect = 0  # 전선
    major = 0  # 전필

    dmajorSelect = 0  # 이선
    dmajor = 0  # 이필

    total = 0  # 전체

    for i in range(0, len(list2)):
        if list2[i][0] == '공교' or list2[i][0] == '역교':
            capability += list2[i][3]

        elif list2[i][0] == '통교' or list2[i][0] == '핵심':
            integration += list2[i][3]
        elif list2[i][0] == '기초':
            basic += list2[i][3]

        elif list2[i][0] == '일교':
            general += list2[i][3]
        elif list2[i][0] == '개교':
            pioneer += list2[i][3]
        elif list2[i][0] == '전선':
            majorSelect += list2[i][3]
        elif list2[i][0] == '전필':
            major += list2[i][3]
        elif list2[i][0] == '이선':
            dmajorSelect += list2[i][3]
        elif list2[i][0] == '이필':
            dmajor += list2[i][3]
        total += list2[i][3]

        takelist = TakeList()
        takelist.takeListUserName = CustomUser.objects.get(pk=request.user.username)
        takelist.classification = list2[i][0]
        takelist.lectureNumber = list2[i][1]
        takelist.lectureName = list2[i][2]
        takelist.lecturePoint = float(list2[i][3])
        takelist.grade = list2[i][4]
        takelist.save()

    takelistpoint = TakeListPoint()
    takelistpoint.takeListPointUserName = CustomUser.objects.get(pk=request.user.username)
    takelistpoint.capability = capability
    takelistpoint.integration = integration
    takelistpoint.basic = basic
    takelistpoint.general = general
    takelistpoint.pioneer = pioneer
    takelistpoint.majorSelect = majorSelect
    takelistpoint.major = major
    takelistpoint.dmajorSelect = dmajorSelect
    takelistpoint.dmajor = dmajor
    takelistpoint.total = total
    takelistpoint.save()

    # 하... 배열이나 리스트 써서 다시 작성하기 위에 로직도.
    # worksheet.write(0, 7, '역량')
    # worksheet.write(0, 8, capability)
    #
    # worksheet.write(1, 7, '통합')
    # worksheet.write(1, 8, integration)
    #
    # worksheet.write(2, 7, '일반')
    # worksheet.write(2, 8, general)
    #
    # worksheet.write(3, 7, '개척')
    # worksheet.write(3, 8, pioneer)
    #
    # worksheet.write(4, 7, '전선')
    # worksheet.write(4, 8, majorSelect)
    #
    # worksheet.write(5, 7, '전필')
    # worksheet.write(5, 8, major)
    #
    # worksheet.write(6, 7, '이선')
    # worksheet.write(6, 8, dmajorSelect)
    #
    # worksheet.write(7, 7, '이필')
    # worksheet.write(7, 8, dmajor)
    #
    # worksheet.write(8, 7, '기초')
    # worksheet.write(8, 8, basic)
    #
    # worksheet.write(9, 7, '전체')
    # worksheet.write(9, 8, total)
    #
    # workbook.save('test.xls')