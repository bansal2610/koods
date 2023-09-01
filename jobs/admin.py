from django.contrib import admin
from jobs.models import Job

class JobAdmin(admin.ModelAdmin):
    list_display = ('company','job_title','job_des','job_image')

admin.site.register(Job,JobAdmin)