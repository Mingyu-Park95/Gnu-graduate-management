from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

# 모듈 가져오기
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
            return HttpResponse('완료')
    return HttpResponse('Failed to Upload File')




