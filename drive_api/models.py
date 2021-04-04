from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class FileUpload(models.Model):
	file=models.FileField()

class UserHash(models.Model):
	hash_instance = models.CharField(max_length=20,default="")
	user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)

class FileInstance(models.Model):
	link = models.URLField(default="")
	hash_active = models.ManyToManyField(UserHash,blank=True)
	delete_it = models.BooleanField(default=False)
	user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)

class FilePart(models.Model):
	name=models.TextField()
	filIns=models.ManyToManyField(FileInstance,blank=True)
	number=models.IntegerField(default=0)
	size=models.FloatField(default=0)
	user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)

class OriginalFile(models.Model):
	file_name=models.TextField()
	file_parts=models.ManyToManyField(FilePart,blank=True)
	number_of_parts=models.IntegerField(default=0)

class folder(models.Model):
	folder_id=models.CharField(max_length=30)
	parts=models.ManyToManyField(FilePart,blank=True)

class UserProfile(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='user_profile')
	coins=models.FloatField(default=0.0)
	banned=models.BooleanField(default=False)
	filename=models.CharField(max_length=20,blank=True)
	folder=models.ForeignKey(folder,on_delete=models.CASCADE,blank=True,null=True)
	space=models.FloatField(default=0.0)
	space_used=models.FloatField(default=0.0)
	full=models.BooleanField(default=False)