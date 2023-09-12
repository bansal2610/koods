from django.db import models
from tinymce.models import HTMLField
from autoslug import AutoSlugField
from django.contrib.auth.models import User
from uploads.models import skil
# from ckeditor.fields import RichTextField

JOB_TYPE = [
    ("Full Time","Full Time"),
    ("Part Time","Part Time"),
    ("Internship","Internship")
]

class Category(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name

class Job(models.Model):
    job_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True,default=None)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null = True)
    job_title = models.CharField(max_length=100)
    job_type = models.CharField(choices=JOB_TYPE,default=None, null = True,max_length=50)
    exp_required = models.CharField(max_length=100)
    skills_req =  models.ManyToManyField(skil)
    job_des = HTMLField(blank=True, null=True)
    salary = models.CharField(max_length=20)
    min_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Minimum Salary",
        help_text="Enter the minimum salary for this job (e.g., 50000.00)",
    )
    max_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Maximum Salary",
        help_text="Enter the maximum salary for this job (e.g., 80000.00)",
    )
    company = models.CharField(max_length=100,null=False,default=None)
    location = models.CharField(max_length=250)
    company_desc = HTMLField(blank=True, null=True)
    url = models.URLField(max_length=200)
    last_update = models.DateField()
    timestamp = models.DateTimeField(auto_now=True)
    job_image = models.ImageField(upload_to='job/', default = "job/jobs-1.jpg")
    job_slug = AutoSlugField(populate_from = 'get_full_slug',unique=True,null=True,default=None)
    is_published = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)

    def get_full_slug(self):
        return f"{self.job_title} at {self.company}"

    def __str__(self):
        return self.job_title

class Applicant(models.Model):
    user = models.ForeignKey(User, null=True,blank=True, default=None,on_delete=models.CASCADE)
    job = models.ForeignKey(Job, null=True,blank=True, default=None, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.job.job_title


# front==============
# location 
# exp. required
# skills required xxxxxxxxxxxxxxxxxxxxxx
# back===============
# job details>>>>>
# must have skills
# good to have skills
# industry type
# education

# similar jobs