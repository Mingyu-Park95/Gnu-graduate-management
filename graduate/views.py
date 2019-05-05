from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

# 모듈 가져오기
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
            studentId = request.user.studentId
            studentMajor = request.user.studentMajor

            filename = userName
            fp = open('%s/%s' % ('a', filename) , 'wb')
            for chunk in file.chunks():
                fp.write(chunk)
            fp.close()

            makeTakeList(request)
            notTakeList, takeList =checkBasic(userName, studentId, studentMajor)

            return ready_upload(request)
    return HttpResponse('Failed to Upload File')

