from django.db import models
from tinymce.models import HTMLField
from autoslug import AutoSlugField
from django.contrib.auth.models import User

class Courses(models.Model):
    course_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True,default=None)
    course_title = models.CharField(max_length=100)
    course_price = models.DecimalField(max_digits=6, decimal_places=2,null=True)
    course_des = HTMLField()
    course_level = models.CharField(choices=(('Beginner', ("Beginner")),
                                        ('Intermediate', ("Intermediate")),
                                        ('Advance', ("Advance"))),
                                default='Beginner',max_length=50)
    course_duration = models.CharField(max_length=100)
    course_image = models.ImageField(upload_to="corse/",null=True,default="course/courses-1.jpg")
    course_slug = AutoSlugField(populate_from = 'course_title',unique=True,null=True,default=None)

    def __str__(self):
        return self.course_title