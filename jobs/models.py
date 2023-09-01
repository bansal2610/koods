from django.db import models
from tinymce.models import HTMLField
from autoslug import AutoSlugField

class Job(models.Model):
    company = models.CharField(max_length=100,null=False,default=None)
    job_title = models.CharField(max_length=100)
    job_des = HTMLField()
    job_image = models.ImageField(upload_to="job/",null=True,default = "job/jobs-1.jpg")
    job_slug = AutoSlugField(populate_from = 'job_title',unique=True,null=True,default=None)