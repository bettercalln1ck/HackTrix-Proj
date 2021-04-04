from .models import *
from .final import g_auth
from .divide import split_number


def upload_drive(content_file,cred_file):
	cred=g_auth('media/cred/'+cred_file)
	return cred.upload_file(content_file'media/'+content_file)

def upload_file(id):
	file_obj=get_object_or_404(FileUpload,id=id)
	filename=file_obj.file.name
	name_list=filename.split('.')
	parts=ceil(split_number(file_obj.file.path,size=1024000))
	total=UserProfile.objects.filter(user.is_superuser=True).count()
	users=UserProfile.objects.filter(user.is_superuser=True).order_by('space_used')[:parts]
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

def job_init():
	while True:
		for som in FileUpload.all():
			upload_file(som.id)
		for filepart in FilePart.all():
			for filinstanc in filepart.all():
				if fileinstanc.delete_it and filinstanc.hash_active.count==0:
					filinstanc.delete_it=False
					filinstanc.save()