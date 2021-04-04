from django.shortcuts import render,get_object_or_404,redirect
from django.http import JsonResponse,HttpResponse
# Create your views here.
from .models import *
from .final import g_auth
from .divide import split_number
from math import ceil
import os
from .forms import *
from django.http import Http404
from django.contrib.auth import authenticate,logout
from django.contrib.auth import login as djangologin
from django.contrib.auth.forms import UserCreationForm
from django.views import View
import random
from .forms import LoginForm
import time
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import Count

WEBSITE_NAME = 'http://127.0.0.1:8000/'
MAX_LIM = 7

def index(request):
	if request.user.is_authenticated:
		context = {'files':OriginalFile.objects.all(),'web_link':WEBSITE_NAME.rstrip('/')}
		return render(request,'index.html',context)
	else:
		return redirect('login')

def forUploading(request):
	if request.user.is_superuser:
		context = {'files':FileUpload.objects.all()}
		return render(request,'activate.html',context)

def UploadFile(request):
	if request.method=='POST':
		fil=file_upload_form(request.POST,request.FILES)
		if fil.is_valid():
			fil.save()
			return render(request,'confirm.html')
	form=file_upload_form()
	context={'form':form}
	return render(request,'upload.html',context)

def upload_drive(content_file,cred_file):
	cred=g_auth('media/cred/'+cred_file)
	return cred.upload_file(content_file,'media/'+content_file)
	
def upload_file(request,id):
	file_obj=get_object_or_404(FileUpload,id=id)
	filename=file_obj.file.name
	name_list=filename.split('.')
	parts=ceil(split_number(file_obj.file.path,size=1024000))
	total=UserProfile.objects.filter(user__is_superuser=True).count()
	users=UserProfile.objects.filter(user__is_superuser=True).order_by('space_used')[:parts]
	uploaded_file=OriginalFile(file_name=filename,number_of_parts=parts)
	uploaded_file.save()
	print(os.getcwd())
	for i in range(parts):
		upload_name=filename+'_'+str(i+1)
		part_uploaded=users[i%total].folder.parts
		link=upload_drive(upload_name,users[i%total].filename)
		file_size=os.path.getsize('media/'+filename)
		users[i%total].space_used+=file_size
		filIns = FileInstance(link = link,user = users[i%total].user)
		filIns.save()
		sc=FilePart(name=upload_name,user=users[i%total].user,number=i,size=file_size)
		sc.save()
		somCop = sc.filIns
		somCop.add(filIns)
		sc.save()
		part_uploaded.add(sc)
		d=uploaded_file.file_parts
		d.add(sc)
		users[i%total].save()
	uploaded_file.save()
	for fname in os.listdir('.'):
		if fname.startswith(filename.split('.')[0]):
			os.remove(os.path.join('.', fname))
	file_obj.delete()
	return render(request,'succesful.html')



class Register(View):
	def __init__(self):
		self.template_name='register/register.html'
	def get(self,request):
		form=LoginForm()
		profile_form=ProfileForm()
		context={'form':form,'profile_form':profile_form}
		return render(request,self.template_name,context)
	def post(self,request):
		form=LoginForm(request.POST)
		profile=ProfileForm(request.POST)
		if form.is_valid():
			somF = form.save()
			username=form['username'].value()
			password=form['password'].value()
			print(username)
			print(password)
			user=authenticate(username=username,password=password)
			djangologin(request,somF)
			profile = profile.save(commit=False)
			profile.user=somF
			profile.save()
			return redirect('view_profile')
		return redirect('register')

class ViewProfile(View):
	def __init__(self):
		self.template_name='login/profile.html'
	def get(self,request):
		profile=request.user.user_profile
		context={'profile':profile}
		return render(request,self.template_name,context)

class EditProfile(View):
	def __init__(self):
		self.template_name='login/editprofile.html'
	def get(self,request):
		form=ProfileForm(instance=request.user.user_profile)
		context={'form':form}
		return render(request,self.template_name,context)
	def post(self,request):
		form=ProfileForm(request.POST,instance=request.user.user_profile)
		if form.is_valid():
			form.save()
			return redirect('edit_profile')

def log_me_out(request):
	logout(request)
	return redirect('login')

def loginP(request):
    if request.method=='POST':
        form=LoginForm(request.POST)
        print(request.POST)
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        if user:
            djangologin(request,user)
            return redirect('index')
    form=LoginForm()
    context={'form':form,}
    return render(request,'login/login.html',context)

def share_drive(file_id,cred_file,to_user,user_cred_file):
	cred=g_auth('media/cred/'+cred_file)
	cred.share_file(file_id,to_user)
	f=g_auth('media/cred/'+user_cred_file)
	return f.copy_file(file_id,'aaa')
	
def distribute(request,id):
	file_obj=get_object_or_404(OriginalFile,id=id)
	total=UserProfile.objects.filter(user__is_superuser=False).count()
	fileparts=file_obj.file_parts.all()
	parts=file_obj.number_of_parts
	users=UserProfile.objects.filter(user__is_superuser=False).order_by('space_used')[:parts]
	print(os.getcwd())
	for i,somp in enumerate(fileparts):
		filLink = somp.filIns.all()[0]
		userIns = users[i%total]
		link=share_drive(filLink.link,filLink.user.user_profile.filename,userIns.user.email,userIns.filename).get('id')
		userIns.space_used+=somp.size
		userIns.save()
		sc=FileInstance(link=link,user = users[i%total].user)
		sc.save()
		somp.filIns.add(sc)
		somp.save()
		part_uploaded=userIns.folder.parts
		part_uploaded.add(somp)
		userIns.folder.save()
	context={'file_detail':file_obj}
	return render(request,'succesful.html',context)

def distributeIns(id):
	file_obj=get_object_or_404(FilePart,id=id)
	filLink = file_obj.filIns.all()[0]
	users=UserProfile.objects.filter(user__is_superuser=False).order_by('space_used')[0]
	link=share_drive(filLink.link,filLink.user.user_profile.filename,users.user.email,users.filename).get('id')
	users.space_used+=file_obj.size
	users.save()
	sc=FileInstance(link=link,user = users.user)
	sc.save()
	file_obj.filIns.add(sc)
	file_obj.save()
	part_uploaded=users.folder.parts
	part_uploaded.add(file_obj)
	users.folder.save()
	return sc


from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import google_auth_oauthlib
SCOPES = ['https://www.googleapis.com/auth/drive']
def login_google_drive(request):
	flow = InstalledAppFlow.from_client_secrets_file('media/client_secrets.json', SCOPES)
	flow.redirect_uri = WEBSITE_NAME+'api/oauthcalback'
	authorization_url, state = flow.authorization_url(access_type='offline',include_granted_scopes='true')
	request.session['state']=state
	return redirect(authorization_url)

import random
import string
import pickle
def randFileName():
	return ''.join(random.choice(string.ascii_letters) for _ in range(16))

from urllib.parse import unquote
def oauthcalback(request):
	state=request.GET.get('state')
	flow = InstalledAppFlow.from_client_secrets_file('media/client_secrets.json',
		scopes=SCOPES,
		state=state,
		redirect_uri=WEBSITE_NAME+'api/oauthcalback')
	authorization_response =request.build_absolute_uri()
	flow.fetch_token(code=unquote(request.GET['code']))
	authFile = randFileName()
	with open('media/cred/'+authFile,'ab') as filR:
		pickle.dump(flow.credentials, filR)
	cred=flow.credentials
	print(authFile)
	return HttpResponse("successfully got creds<script>window.location = \""+WEBSITE_NAME+"api/regisFile/"+authFile+"\";</script>")

def registerFile(request,authFile):
	request.user.user_profile.filename = authFile
	request.user.user_profile.save()
	newFolder = folder()
	newFolder.save()
	request.user.user_profile.folder = newFolder
	request.user.user_profile.save()
	return redirect('index')


def create_link(somLink):
	insLink = somLink.filIns.annotate(q_count=Count('hash_active')).filter(delete_it=False).filter(q_count__lte=MAX_LIM).order_by('-q_count')
	if insLink.exists() :
		insLink = insLink[0]
		hashins = UserHash(hash_instance=randFileName())
		hashins.save()
		insLink.hash_active.add(hashins)
		insLink.save()
		return hashins.hash_instance
	else:
		for som in somLink.filIns.all():
			som.delete_it = True
		insLink = distributeIns(somLink.id)
		hashins = UserHash(hash_instance=randFileName())
		hashins.save()
		insLink.hash_active.add(hashins)
		insLink.save()
		return hashins.hash_instance


def DownloadFile(request,id):
	hasIns=get_object_or_404(UserHash,hash_instance=id)
	some=FileInstance.objects.filter(hash_active__hash_instance = id)[0]
	data={'link':some.link}
	hasIns.delete()
	return JsonResponse(data)

def downloadAPI(request,id):
	file_obj=get_object_or_404(OriginalFile,id=id)
	some=[]
	number_of_parts=file_obj.number_of_parts
	for fil_link in file_obj.file_parts.all():
		some.append(create_link(fil_link))
	data={'filename':file_obj.file_name,'hash':some}
	return JsonResponse(data)

def MyFiles(request):
	if request.user.is_superuser:
		context={"gtorrent":OriginalFile.objects.all()}
		return render(request,'admin.html',context)
	else:
		raise Http404

def drivequery(request,id):
	if request.user.is_superuser:
		obj=get_object_or_404(OriginalFile,id=id)
		context={"org_file":obj}
		return render(request,'graph.html',context)
	else:
		raise Http404












