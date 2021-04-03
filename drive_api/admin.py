from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(FileInstance)
admin.site.register(FileUpload)
admin.site.register(FilePart)
admin.site.register(OriginalFile)
admin.site.register(folder)
admin.site.register(UserProfile)
admin.site.register(UserHash)