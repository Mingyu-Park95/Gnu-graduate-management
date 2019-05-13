from django.urls import path
from . import views

app_name = 'graduate'
urlpatterns = [
    path('', views.ready_upload, name='ready_upload'),
    path('upload', views.upload_file, name='upload_file'),
    path('result', views.result, name='result'),
    path('resultTest', views.resultTest, name='resultTest'),
    path('change', views.change,name='change'),
    path('changeResult', views.changeResult,name='changeResult'),
]