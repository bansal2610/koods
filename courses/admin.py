from django.contrib import admin
from courses.models import Courses

class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_title','course_price','course_level','course_duration','course_image')

admin.site.register(Courses,CourseAdmin)