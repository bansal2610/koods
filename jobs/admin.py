from django.contrib import admin
from jobs.models import Job,Category,Applicant

class JobAdmin(admin.ModelAdmin):
    list_display = ('company','job_title','job_des','timestamp')

admin.site.register(Job,JobAdmin)
admin.site.register(Category)
admin.site.register(Applicant)
