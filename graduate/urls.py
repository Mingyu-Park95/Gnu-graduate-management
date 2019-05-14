from django.urls import path
from . import views

app_name = 'graduate'
urlpatterns = [
    # 기존


    path('result', views.result, name='result'),
    path('resultTest', views.resultTest, name='resultTest'),
    path('change', views.change,name='change'),
    path('changeResult', views.changeResult,name='changeResult'),

    # 지흠
    path('report', views.report, name='report'),
    path('ready_upload', views.ready_upload, name='ready_upload'),
    path('upload', views.upload_file, name='upload_file'),
]
# path('', views.ready_upload, name='ready_upload'),
# path('upload', views.upload_file, name='upload_file'),