from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from uploads.models import Profile
from jobs.models import Job
from courses.models import Courses
from tinymce.widgets import TinyMCE

# class ADDJOB(forms.ModelForm):
#     class Meta:
#         model = Job
#         fields = ['category','job_title','job_type','exp_required','skills_req','job_des','min_salary','max_salary','location','company','company_desc','url','job_image','is_published','is_closed']
#         widgets = {'content':TinyMCE(attrs={'cols':80, 'rows':30})}

#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop('user', None)
#         super(ADDJOB, self).__init__(*args, **kwargs)
#         self.fields['skills_req'].widget.attrs = {'class':'js-select2','required':'required'}
        
#         if user:
#             self.user = user 

class ADDJOB_DESC(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['job_des', 'company_desc']
        widgets = {'content':TinyMCE(attrs={'cols':80, 'rows':30})}


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ADDJOB_DESC, self).__init__(*args, **kwargs)
        # self.fields['skills_req'].widget.attrs = {'class':'js-select2','required':'required'}
        self.fields['job_des'].label = "Job Description"
        self.fields['company_desc'].label = "Course Description"
        
        if user:
            self.user = user 
        
class ADDCOURSE_DESC(forms.ModelForm):
    class Meta:
        model = Courses
        fields = ['course_des']
        widgets = {'content':TinyMCE(attrs={'cols':80, 'rows':30})}


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ADDCOURSE_DESC, self).__init__(*args, **kwargs)
        # self.fields['skills_req'].widget.attrs = {'class':'js-select2','required':'required'}
        self.fields['course_des'].label = "Course Description"
        
        if user:
            self.user = user 
    
    
class EDITJOB(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['category','job_title','job_type','exp_required','skills_req','job_des','min_salary','max_salary','location','company','company_desc','url','job_image','is_published','is_closed']
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(EDITJOB, self).__init__(*args, **kwargs)
        self.fields['skills_req'].widget.attrs = {'class':'js-select2'}
        if user:
            self.user = user 



class EDIT_DESC(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['job_des', 'company_desc']
        widgets = {'content':TinyMCE(attrs={'cols':80, 'rows':30})}


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(EDIT_DESC, self).__init__(*args, **kwargs)
        self.fields['job_des'].label = "Job Description"
        self.fields['company_desc'].label = "Course Description"
        
        if user:
            self.user = user 


# class ADDCOURSE(forms.ModelForm):
#     class Meta:
#         model = Courses
#         fields = ['course_title','course_price','course_des','course_level','course_duration','course_image']

class CreateUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password1','password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = [
#             'username', 
#             'first_name', 
#             'last_name', 
#             'email', 
#         ]

# GENDER_CHOICES = [
#     ('Male','Male'),('Female','Female'),('Other','Other'),('Prefer not to say','Prefer not to say')
# ]
# SKILL_CHOICES = [
#     ('Python','Python'),('Django','Django'),('HTML','HTML'),('CSS','CSS'),('Bootstrap','Bootstrap'),('Wordpress','Wordpress'),('Java','Java'),('Shopify','Shopify')
# ]

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