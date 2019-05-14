from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from accounts.models import TakeList, CustomUser, TakeListPoint
from graduate.models import LectureList, MajorPoint
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
            eduYear = request.user.eduYear
            studentMajor = request.user.studentMajor
            studentSubMajor = request.user.studentSubMajor
            studentDoubleMajor = request.user.studentDoubleMajor
            studentConvergence =request.user.studentConvergenceMajor
            studentTrack = request.user.studentTrack
            studentTeaching = request.user.studentTeaching

            filename = userName
            fp = open('%s/%s' % ('a', filename) , 'wb')
            for chunk in file.chunks():
                fp.write(chunk)
            fp.close()
            makeTakeList(request)


            # 내가 테스트하는 부분
            basicNotTakeList, basicTakeList = checkBasic(userName, eduYear, studentMajor)
            dream = checkDream(userName, eduYear, studentMajor)
            pioneer = checkPioneer(userName, eduYear, studentMajor)

            # 단일전공, 복수전공 if
            if studentDoubleMajor!='해당없음':
                majorResult, MustTakeList, userMustTakeList = checkDobuleMajor(userName, eduYear, studentMajor, studentDoubleMajor, studentSubMajor)
            else:
                soloMajor = checkMajor(userName, eduYear, studentMajor, studentDoubleMajor, studentSubMajor)

            Capability = Capability_Judge(userName,eduYear,studentMajor)
            Integration = Integration_Judge(userName, eduYear, studentMajor)

            if studentConvergence =='산업경영지원학':
                convergenceMajor = convergenceMajor_Judge(userName, eduYear, studentMajor)

            if studentTrack =='재무금융트랙':
                financeTrack = financeTrack_Judge(userName, eduYear, studentMajor)
            elif studentTrack =='세무전문트랙':
                accountTrack = accountTrack_Judge(userName, eduYear, studentMajor)
            elif studentTrack =='유통서비스트랙':
                channelTrack = channelTrack_Judge(userName, eduYear, studentMajor)
            elif studentTrack == 'IT융합시스템개발':
                ITtrack = ITtrack_Judge(userName, eduYear, studentMajor)

            if studentTeaching =='해당':
                edu_Basic = edu_Basic_Judge(userName, eduYear, studentMajor)
                edu_Teach = edu_Teach_Judge(userName, eduYear, studentMajor)
                edu_Career = edu_Career_Judge(userName, eduYear, studentMajor)

            print(basicNotTakeList)
            print(basicTakeList)
            print(dream)
            print('개척'+pioneer)
            print('복수전공')
            print(majorResult)
            print('반드시들어야하는과목')
            print(MustTakeList)
            print('유저가 들은 과목')
            print(userMustTakeList)
            print('단일전공')
            # print(soloMajor)
            print(Capability)
            print(Integration)
            print(convergenceMajor)
            #print(financeTrack)
            #print(accountTrack)
            #print(channelTrack)
            print(ITtrack)
            #print(edu_Basic)
            #print(edu_Teach)
            #print(edu_Career)


            return render(request, 'graduate/result.html')
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

        #return render(request,'graduate/changeResult.html', {'customs':customs})



def report(request):
    studentMajor=request.user.studentMajor
    studentDoubleMajor = request.user.studentDoubleMajor
    studentConvergenceMajor = request.user.studentConvergenceMajor
    userTakePoint = TakeListPoint.objects.get(takeListPointUserName=request.user.username)
    mustTakePoint = MajorPoint.objects.get(Q(eduYear=request.user.eduYear)&Q(major=studentMajor))

    # 단일 전공인 경우
    if studentDoubleMajor =='해당없음' and studentConvergenceMajor=='해당없음':
        majorPoint = mustTakePoint.majorPoint
        majorSelectPoint = mustTakePoint.majorSelectPoint
    # 경영대학 내 복수전공인 경우
    elif studentDoubleMajor !='해당없음' and studentConvergenceMajor =='해당없음':
        majorPoint = mustTakePoint.dmajorPoint
        majorSelectPoint = mustTakePoint.dmajorSelectPoint
        doubleMajorPoint = mu

    return render(request, 'graduate/report.html')
















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
