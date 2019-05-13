from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from accounts.models import TakeList, CustomUser
# 모듈 가져오기
from graduate.models import LectureList
from graduate.modules.checkDoubleMajor import checkMajor
from graduate.modules.checkpioneer import checkDream, checkPioneer
from graduate.modules.judgeData import Integration_Judge
from graduate.modules.makeTakeList import makeTakeList
from graduate.modules.checkBasic import checkBasic

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
            filename = userName
            fp = open('%s/%s' % ('a', filename) , 'wb')
            for chunk in file.chunks():
                fp.write(chunk)
            fp.close()

            makeTakeList(request)
            # 내가 테스트하는 부분
            # BasicnotTakeList, BasicTakeList = checkBasic(userName, eduYear, studentMajor)
            # a = checkDream(userName, eduYear, studentMajor)
            # b = checkPioneer(userName, eduYear, studentMajor, studentDoubleMajor)
            # c = checkMajor(userName, eduYear, studentMajor, studentDoubleMajor, studentSubMajor)

            # 현우가 테스트하는 부분
            # return_value = Capability_Judge(user_name,user_num,user_major)
            # return_value = Integration_Judge(userName, eduYear, studentMajor)

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






def result(request):
    pass
    # return(lectureList)
    # return render(request, 'graduate/result.html', {'lectureList':lectureList})

@csrf_exempt
def resultTest(request):
    if request.method == 'POST':
        check_ = request.POST['check_name']
        return HttpResponse(check_)
