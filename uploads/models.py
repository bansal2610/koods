from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField

class Industry(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

class skil(models.Model):
    data = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.data

class Profile(models.Model):
    profile_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to="profile/",null=True,default = "profile/profile-default.jpg")
    profile_desc = models.TextField(max_length=250,blank=True)
    institution = models.CharField(max_length=50,blank=True)
    resume = models.FileField(upload_to="resume/",null=True,default="resume/resume.pdf")
    resume_data = models.TextField(max_length=3000,null=True,default="RESUME")
    skills = models.ManyToManyField(skil)
    phone = PhoneNumberField(region="IN",null=True, blank=True,unique=True)
    gender = models.CharField(max_length=100)
    work_at = models.CharField(max_length=100, default=None, null=True, blank=True)
    position = models.ForeignKey(Industry, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    is_job = models.BooleanField(default=False)
    is_course = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

    