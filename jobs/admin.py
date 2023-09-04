from django.contrib import admin
from jobs.models import Job,Category,Applicant

class JobAdmin(admin.ModelAdmin):
    list_display = ('company','job_title','job_des','job_image')

admin.site.register(Job,JobAdmin)
admin.site.register(Category)
admin.site.register(Applicant)
