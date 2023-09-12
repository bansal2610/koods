from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from uploads.models import Profile
from jobs.models import Job
from courses.models import Courses

class ADDJOB(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['category','job_title','job_type','exp_required','skills_req','job_des','salary','min_salary','max_salary','location','company','company_desc','url','last_update','job_image','is_published','is_closed']
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ADDJOB, self).__init__(*args, **kwargs)
        if user:
            self.user = user 


class ADDCOURSE(forms.ModelForm):
    class Meta:
        model = Courses
        fields = ['course_title','course_price','course_des','course_level','course_duration','course_image']

class CreateUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password1','password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username', 
            'first_name', 
            'last_name', 
            'email', 
        ]

GENDER_CHOICES = [
    ('Male','Male'),('Female','Female'),('Other','Other'),('Prefer not to say','Prefer not to say')
]
SKILL_CHOICES = [
    ('Python','Python'),('Django','Django'),('HTML','HTML'),('CSS','CSS'),('Bootstrap','Bootstrap'),('Wordpress','Wordpress'),('Java','Java'),('Shopify','Shopify')
]

# class ProfileForm(forms.ModelForm):
#     gender = forms.ChoiceField(choices=GENDER_CHOICES,widget=forms.RadioSelect)
#     skills = forms.MultipleChoiceField(choices=SKILL_CHOICES,widget=forms.CheckboxSelectMultiple)
#     class Meta:
#         model = Profile
#         fields = [
#             'profile_image',
#             'profile_desc',
#             'resume',
#             'resume_data',
#             'skills',
#             'gender',
#             'phone',
#             'institution',
#         ]
#         labels = {'institution':'Institution/Organization','profile_desc':'About','profile_image':'Profile Image','resume':'Resume'}