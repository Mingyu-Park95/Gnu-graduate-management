from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from accounts.models import TakeList, CustomUser, TakeListPoint, GradeByPeriod
from graduate.models import LectureList, MajorPoint, RefinementPoint
# 모듈 가져오기
from graduate.modules.checkMajor import checkMajor

from graduate.modules.makeTakeList import makeTakeList
from graduate.modules.checkBasic import checkBasic
from graduate.modules.checkDoubleMajor import checkDobuleMajor
from graduate.modules.checkpioneer import checkDream, checkPioneer
from graduate.modules.judgeData import Integration_Judge
from graduate.modules.judgeData import Integration_Judge
from graduate.modules.judgeData import Capability_Judge
from graduate.modules.judgeConvergence import convergenceMajor_Judge
from graduate.modules.track_IT import ITtrack_Judge
from graduate.modules.track_Finance import financeTrack_Judge
from graduate.modules.track_Account import accountTrack_Judge
from graduate.modules.track_Channel import channelTrack_Judge
from graduate.modules.edu_Career import edu_Career_Judge
from graduate.modules.edu_Teach import edu_Teach_Judge
from graduate.modules.edu_Basic import edu_Basic_Judge

def ready_upload(request):
    if request.user.is_authenticated:
        return render(request, 'graduate/ready_upload.html')
    else:
        return HttpResponseRedirect(reverse('login'))


@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        if 'file' in request.FILES:
            file = request.FILES['file']

            # 처리에 필요한 회원 정보
            userName = request.user.username
            filename = userName
            fp = open('%s/%s' % ('a', filename) , 'wb')
            for chunk in file.chunks():
                fp.write(chunk)
            fp.close()

            makeTakeList(request)

            return report(request)
    return HttpResponse('Failed to Upload File')


@csrf_exempt
def change(request):
    AddedList = TakeList.objects.filter(Q(addedCustom=True) & Q(takeListUserName=request.user.username))
    if request.method =='GET':
        return render(request, 'graduate/change.html', {'AddedList':AddedList})

    if request.method == 'POST':
        # 검색할 때
        if 'searchText' in request.POST:
            searchText = request.POST['searchText']
            if searchText !='':
                lectureList = LectureList.objects.filter(Q(lectureName__contains=searchText))
                return render(request, 'graduate/change.html', {'lectureList': lectureList, 'AddedList':AddedList})
            return render(request, 'graduate/change.html', {'AddedList': AddedList})

        # 등록할 때
        elif 'check_name' in request.POST:
            customs = request.POST.getlist('check_name')
            for custom in customs:
                customObject = LectureList.objects.get(id=custom)
                takeList = TakeList()
                takeList.lectureNumber = customObject.lectureNumber
                takeList.lecturePoint = customObject.lecturePoint
                takeList.classification = customObject.classification
                takeList.grade = 'B+'
                takeList.takeListUserName = CustomUser.objects.get(username=request.user.username)
                takeList.lectureName = customObject.lectureName
                takeList.addedCustom = True
                takeList.save()
            return HttpResponseRedirect('change', {'AddedList': AddedList})

        elif 'delete' in request.POST:
            deleteList = request.POST.getlist('delete')
            for delete in deleteList:
                # 삭제할 때는 아이디 값을 삭제한다, 학수번호로 삭제하면 꿈미래 같이 중복으로 한 것들 한번에 다 사라짐
                deleteObject = TakeList.objects.get(Q(addedCustom=True) & Q(id=delete))
                deleteObject.delete()
        return HttpResponseRedirect('change', {'AddedList': AddedList})
    return render(request, 'graduate/change.html')


@csrf_exempt
def changeResult(request):
    if request.method == 'POST':
        customs = request.POST.getlist('check_name')
    return render(request, 'graduate/changeResult.html', {'customs':customs})


def report(request):
    studentMajor=request.user.studentMajor
    studentDoubleMajor = request.user.studentDoubleMajor
    studentConvergenceMajor = request.user.studentConvergenceMajor
    eduYear =request.user.eduYear
    userName =request.user.username

    studentConvergence = request.user.studentConvergenceMajor
    studentTrack = request.user.studentTrack
    studentTeaching = request.user.studentTeaching

    dreamCnt, mustDream, dreamString = checkDream(userName)
    dream = {'dreamCnt': dreamCnt,'mustDream': mustDream, 'dreamString': dreamString }


    userTakePoint = TakeListPoint.objects.get(takeListPointUserName=userName)
    userPioneerPoint = userTakePoint.pioneer + userTakePoint.general
    mustTakeRefinePoint = RefinementPoint.objects.get(Q(major=studentMajor)&Q(eduYear=eduYear))

    mustTakePoint = MajorPoint.objects.get(Q(eduYear=eduYear) & Q(major=studentMajor))

    MustDoubleMajorPoint=''
    MustDoubleMajorSelectPoint=''
    notTakeSting=''
    majorResult=''
    doubleOn = 'off'
    # 단일 전공인 경우
    if studentDoubleMajor =='해당없음' and studentConvergenceMajor == '해당없음':
        MustMajorPoint = mustTakePoint.majorPoint
        MustMajorSelectPoint = mustTakePoint.majorSelectPoint

    # 경영대학 내 복수전공인 경우
    if studentDoubleMajor !='해당없음':
        doubleOn ='on'
        mustDoubleTakePoint = MajorPoint.objects.get(Q(eduYear=eduYear) & Q(major=studentDoubleMajor))
        MustMajorPoint = mustTakePoint.dmajorPoint
        MustMajorSelectPoint = mustTakePoint.dmajorSelectPoint
        MustDoubleMajorPoint = mustDoubleTakePoint.dmajorPoint
        MustDoubleMajorSelectPoint = mustDoubleTakePoint.dmajorSelectPoint
        notTakeSting, majorResult =checkDobuleMajor(userName, eduYear, studentMajor, studentDoubleMajor)

    convergenceMajor_str=''
    edu_Basic=''
    edu_Teach=''
    edu_Career=''
    Track_str=''
    takeTrack_list = []
    convergence_list = []
    takeConvergence_list =[]
    dmajor_list=[]
    dmajor_select_list=[]

    # 교직이수
    if studentTeaching == '해당':
        edu_Basic = edu_Basic_Judge(userName, eduYear, studentMajor)
        edu_Teach = edu_Teach_Judge(userName, eduYear, studentMajor)
        edu_Career = edu_Career_Judge(userName, eduYear, studentMajor)

    # String 값 띄우기
    Capability_str = Capability_Judge(userName, eduYear, studentMajor)
    Integration_str = Integration_Judge(userName, eduYear, studentMajor)
    Basic_str = checkBasic(userName, eduYear, studentMajor)
    Pioneer_str = checkPioneer(userName, eduYear, studentMajor)

    # 산업경영지원학
    if studentConvergence == '산업경영지원학':
        convergenceMajor_str, takeConvergence_list = convergenceMajor_Judge(userName, eduYear, studentMajor)
        convergence_list = TakeList.objects.filter(Q(classification='이필') & Q(takeListUserName=userName))
        MustMajorPoint = mustTakePoint.dmajorPoint
        MustMajorSelectPoint = mustTakePoint.dmajorSelectPoint
    # 트랙제
    if studentTrack == '재무금융트랙':
        Track_str, takeTrack_list = financeTrack_Judge(userName, eduYear, studentMajor)
    elif studentTrack == '세무전문트랙':
        Track_str, takeTrack_list = accountTrack_Judge(userName, eduYear, studentMajor)
    elif studentTrack == '유통서비스트랙':
        Track_str, takeTrack_list = channelTrack_Judge(userName, eduYear, studentMajor)
    elif studentTrack == 'IT융합시스템개발':
        Track_str, takeTrack_list = ITtrack_Judge(userName, eduYear, studentMajor)

    if studentTeaching == '해당':
        edu_Basic = edu_Basic_Judge(userName, eduYear, studentMajor)
        edu_Teach = edu_Teach_Judge(userName, eduYear, studentMajor)
        edu_Career = edu_Career_Judge(userName, eduYear, studentMajor)


    # 테이블에 수강한 과목 화면에 띄우기
    integration_list = TakeList.objects.filter(
        Q(takeListUserName=userName) & (Q(classification='공교') | Q(classification='역교')))
    capability_list = TakeList.objects.filter(
        (Q(classification='핵심') | Q(classification='통교')) & Q(takeListUserName=userName))
    basic_list = TakeList.objects.filter(Q(classification='기초') & Q(takeListUserName=userName))
    pioneer_list = TakeList.objects.filter(Q(lectureName='꿈·미래개척') & Q(takeListUserName=userName))
    major_list = TakeList.objects.filter(Q(classification='전필') & Q(takeListUserName=userName))
    major_select_list = TakeList.objects.filter(Q(classification='전선') & Q(takeListUserName=userName))
    dmajor_list = TakeList.objects.filter(Q(classification='이필')& Q(takeListUserName=userName))
    dmajor_select_list = TakeList.objects.filter(Q(classification='이선') & Q(takeListUserName=userName))

    gradeList = []
    periodList = ''
    for grade in GradeByPeriod.objects.filter(gradeByPeriodName=userName):
        gradeList.append(grade.grade)
        periodList+=grade.period[8:]+'a'

    A =''
    B =''
    C =''
    D =''
    P =''

    A = TakeList.objects.filter(Q(takeListUserName=userName) & (Q(grade='A+') | Q(grade='A0')))
    B = TakeList.objects.filter(Q(takeListUserName=userName) & (Q(grade='B+') | Q(grade='B0')))
    C = TakeList.objects.filter(Q(takeListUserName=userName) & (Q(grade='C+') | Q(grade='C0')))
    D = TakeList.objects.filter(Q(takeListUserName=userName) & (Q(grade='D+') | Q(grade='D0')))
    P = TakeList.objects.filter(Q(takeListUserName=userName) & (Q(grade='P')))
    A = len(A)
    B = len(B)
    C = len(C)
    D = len(D)
    P = len(P)
    # for grade in TakeList.objects.filter(takeListUserName=userName):
    #     if grade.grade == 'A+' or grade.grade == 'A0':
    #         A +=1
    #     elif grade.grade == 'B+' or grade.grade == 'B0':
    #         B +=1
    #     elif grade.grade == 'C+' or grade.grade == 'C0':
    #         C +=1
    return render(request, 'graduate/report.html', {'Integration_str': Integration_str,
                                                    'Capability_str': Capability_str,
                                                    'Basic_str': Basic_str,
                                                    'Pioneer_str': Pioneer_str,
                                                    'convergenceMajor_str': convergenceMajor_str,
                                                    'Track_str': Track_str,
                                                    'edu_Basic': edu_Basic,
                                                    'edu_Teach': edu_Teach,
                                                    'edu_Career': edu_Career,
                                                    'integration_list': integration_list,
                                                    'capability_list': capability_list,
                                                    'basic_list': basic_list,
                                                    'pioneer_list': pioneer_list,
                                                    'major_list': major_list,
                                                    'major_select_list': major_select_list,
                                                    'dmajor_list': dmajor_list,
                                                    'dmajor_select_list': dmajor_select_list,
                                                    'convergence_list': convergence_list,
                                                    'takeConvergence_list': takeConvergence_list,
                                                    'takeTrack_list': takeTrack_list,

                                                    'userPioneerPoint': userPioneerPoint,
                                                    'mustTakeRefinePoint': mustTakeRefinePoint,
                                                    'eduYear': eduYear, # 교육과정 for 개척교양
                                                    'dream': dream,

                                                    'userTakePoint': userTakePoint, #사용자가 들은 학점 한 행.

                                                    'MustMajorPoint': MustMajorPoint,  # 전필 들어야 되는거
                                                    'MustMajorSelectPoint': MustMajorSelectPoint, #전선 들어야 되는거
                                                    'MustDoubleMajorPoint': MustDoubleMajorPoint, #이필 들어야 되는거
                                                    'MustDoubleMajorSelectPoint': MustDoubleMajorSelectPoint,# 이선 들어야되는거
                                                    'gradeList': gradeList,
                                                    'periodList': periodList,
                                                    'dmajor_list': dmajor_list,
                                                    'dmajor_select_list': dmajor_select_list,
                                                    'A': A,
                                                    'B': B,
                                                    'C': C,
                                                    'D': D,
                                                    'P': P,
                                                    'notTakeSting': notTakeSting,
                                                    'majorResult': majorResult,
                                                    'doubleOn': doubleOn,
                                                    })










# 약간필요없는거
def result(request):
    pass
    # return(lectureList)
    # return render(request, 'graduate/result.html', {'lectureList':lectureList})

@csrf_exempt
def resultTest(request):
    if request.method == 'POST':
        check_ = request.POST['check_name']
        return HttpResponse(check_)
