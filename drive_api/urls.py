from django.urls import path,include
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
	path('',views.index,name='index'),
    path('activate/',views.forUploading,name='activate'),
	path('upload_file/<id>/',views.upload_file),
    path('logout/',views.log_me_out,name='logout'),
    path('register/',views.Register.as_view(),name='register'),
    path('profile/',views.ViewProfile.as_view(),name='view_profile'),
    path('edit/',views.EditProfile.as_view(),name='edit_profile'),
    path('upload/',views.UploadFile,name='upload'),
    path('admin/myfiles/',views.MyFiles,name='myfiles'),
    path('admin/drive/<id>/',views.drivequery,name='drivequery'),
    path('login/',views.loginP,name='login'),
    path('distribute/<id>/',views.distribute,name='distribute'),
    path('login_google_drive/',views.login_google_drive,name='login_google_drive'),# DownloadFile
    path('oauthcalback/',views.oauthcalback,name='oauth2callback'),
    path('regisFile/<authFile>/',views.registerFile,name='regisFile'),
    path('download/<id>/',views.DownloadFile,name='DownloadFile'),
    path('downloadAPI/<id>/',views.downloadAPI,name='downloadAPI'),
]
