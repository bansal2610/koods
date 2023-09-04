from django.db import models
from tinymce.models import HTMLField
from autoslug import AutoSlugField
from django.contrib.auth.models import User
# from ckeditor.fields import RichTextField

JOB_TYPE = [
    ("1","Full Time"),
    ("2","Part Time"),
    ("3","Internship")
]

class Category(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name

class Job(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True,default=None)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null = True)
    job_title = models.CharField(max_length=100)
    job_type = models.CharField(choices=JOB_TYPE,default=None, null = True,max_length=1)
    job_des = HTMLField(blank=True, null=True)
    salary = models.CharField(max_length=20)
    company = models.CharField(max_length=100,null=False,default=None)
    company_desc = HTMLField(blank=True, null=True)
    url = models.URLField(max_length=200)
    last_update = models.DateField()
    timestamp = models.DateTimeField(auto_now=True)
    job_image = models.ImageField(upload_to='job/', default = "job/jobs-1.jpg")
    job_slug = AutoSlugField(populate_from = 'job_title',unique=True,null=True,default=None)
    is_published = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)

    def __str__(self):
        return self.job_title

class Applicant(models.Model):
    user = models.ForeignKey(User, null=True,blank=True, default=None,on_delete=models.CASCADE)
    job = models.ForeignKey(Job, null=True,blank=True, default=None, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.job.job_title
