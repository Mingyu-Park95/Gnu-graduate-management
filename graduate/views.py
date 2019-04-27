from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render


from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt


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
            filename = file._name

            fp = open('%s/%s' % ('a', filename) , 'wb')
            for chunk in file.chunks():
                fp.write(chunk)
            fp.close()
            return ready_upload(request)
    return HttpResponse('Failed to Upload File')

