from django.urls import path
from . import views

app_name = 'graduate'
urlpatterns = [
    path('', views.ready_upload, name='ready_upload'),
    path('upload', views.upload_file, name='upload_file'),
]