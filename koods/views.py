from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login,logout
from courses.models import Courses
from jobs.models import Job
from koods.forms import ADDCOURSE, CreateUserForm, ProfileForm, UserForm, ADDJOB
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib import messages
from django.urls import reverse_lazy
from PyPDF2 import PdfReader
from koods.settings import EMAIL_HOST_USER
from uploads.models import Profile, skil
import ast
from django.conf import settings
from django.core.mail import BadHeaderError, send_mail
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
import random
from uploads.views import data

def Home(request):
    data={
        'title':'Learnkoods'
    }
    return render(request,"home.html",data)

def Add_jobs(request):
    if not request.user.is_staff:
        return redirect("/")
    form = ADDJOB()
    if request.method == "POST":
        form = ADDJOB(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/jobs/')
        else:
            print("Form Error: ",form.errors)
    data={
        'form':form
    }
    return render(request,"add_jobs.html",data)

def Add_course(request):
    if not request.user.is_staff:
        return redirect("/")
    form = ADDCOURSE()
    if request.method == "POST":
        form = ADDCOURSE(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/courses/')
        else:
            print("Form Error: ",form.errors)
    data={
        'form':form
    }
    return render(request,"add_course.html",data)

def Course(request):
    courseData = Courses.objects.all()
    data={
        'title':'Courses',
        'courseData':courseData
    }
    return render(request,"courses.html",data)

def CourseDetails(request,slug):
    coursedetail = Courses.objects.get(course_slug=slug)
    data={
        'coursedetail':coursedetail
    }
    return render(request,"course-details.html",data)

def Jobs(request):
    jobData = Job.objects.all()
    data={
        'title':'Jobs',
        'jobData':jobData
    }
    return render(request,"jobs.html",data)

def jobDetails(request,slug):
    jobdetail = Job.objects.get(job_slug=slug)
    data={
        'jobdetail':jobdetail
    }
    return render(request,"job-details.html",data)

def signUp(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST, request.FILES)
        
        if form.is_valid():  
            form.save()        
            messages.success(request,"Registered Successfully")
            return redirect("/sign-in")
        else:
            print("error")
            messages.error(request,"User Already Exists")
       
            
    data={
        'title':'Sign Up',
        'form':form
    }
    return render(request,"signup.html",data)

def signIn(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)
        try:
            if user is not None:
                login(request,user)
                messages.success(request, f'Login Succesfull, Welcome {username}')
                return redirect('/user-profile')
        except:
            messages.error(request, 'Invalid User')
    data={
        'title':'Sign In'
    }
    return render(request,"signin.html",data)

def logOut(request):
    logout(request)
    print("Logout Successfull")
    return redirect('/')

class ProfileUpdateView(LoginRequiredMixin, TemplateView):
    user_form = UserForm
    profile_form = ProfileForm
    template_name = 'profile.html'
    login_url="/sign-in/"
    

    def post(self, request):
        post_data = request.POST or None
        file_data = request.FILES or None
        usr = request.user
        p = Profile.objects.get(user= usr)
        sk = p.skills.all()

        user_form = UserForm(post_data, instance=request.user)
        profile_form = ProfileForm(post_data, file_data, instance=request.user.profile)
        try:
            if user_form.is_valid() and profile_form.is_valid():
                sample= request.FILES['resume']
                if sample:
                    reader = PdfReader(sample)
                    num_pages = len(reader.pages)
                    for i in range(num_pages):
                        page = reader.pages[i]  
                        text = page.extract_text()
                    profile_form.instance.resume_data = text
                
                
                user_form.save()
                profile_form.save()
                messages.error(request, 'Your profile is updated successfully!')
                return HttpResponseRedirect(reverse_lazy('profile'))
        except Exception as e:
            messages.error(request, "Not found")

        context = self.get_context_data(
                                        user_form=user_form,
                                        profile_form=profile_form,
                                        skill = sk
                                    )

        return self.render_to_response(context)     

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


random = random.randint(999,9999)
def password_reset_request(request):
    global random
    request.session["otp"] = random
    if request.method == "POST":
        email = request.POST.get('email')
        if User.objects.filter(email = email).exists():
            user = User.objects.get(email = email)
        else:
            messages.error(request,"User Not Found!")
            return redirect("/sign-up")
        if user:
            request.session["username"] = user.email
            send_mail("Forgot Password",
                f"Your OTP :{random}",
                EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
                )
            return redirect("/verify-otp/")
        else:
            messages.error(request, "User Not Found!")
            return redirect("/sign-up")
    return render(request,"forgot_pass.html")

def verify_otp(request):
    print("----------------------in otp function")
    if request.method  == 'POST':
        otp1 = request.POST.get('otp')
        otp = int(otp1)
        if otp == request.session['otp']:
            return redirect("/change_password/")
        else :
            messages.error(request, "Invalid OTP")
            return redirect("/verify-otp")


    return render(request,"verify_otp.html")

def change_pass(request):
    if request.method == "POST":
        Pass1 = request.POST.get('password1')
        Pass2 = request.POST.get('password2')
        if Pass1 == Pass2:
            usr = request.session['username']
            user = User.objects.get(email=usr)
            user.username = user.username
            user.email=usr
            user.set_password(Pass2)
            user.save()
            del request.session["username"]
            del request.session["otp"]
            messages.success(request, "Password Changed Successfully")
            return redirect("/sign-in")
        else:
            messages.error(request, "Password Doesn't Match")
            return redirect('/change_password')

    return render(request, 'change_pass.html')

# def insert_skill(request):
#     skil.objects.all().delete()
#     d = data()
#     for i in range(len(d)):
#         skil.objects.create(data = d[i])
#     return HttpResponse("skill Created")

def update_profile(request,id):
    skills = skil.objects.all()
    profile = Profile.objects.get(id=id)
    user = User.objects.get(id=id)
    combined_text = ""
    print(profile.id,"==========",user.id,"================User Id, Profile")
    if request.method == "POST":
        username = request.POST.get("username")
        first_name = request.POST.get('first_name')
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        about = request.POST.get("about")
        gender = request.POST.get("gender")
        phone = request.POST.get("phone")
        inst = request.POST.get("inst")
        skill = request.POST.getlist("skills")
        resume = request.FILES.get("resume", None)
        image = request.FILES.get("image", None)
        
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        profile.gender = gender
        profile.phone = phone
        profile.profile_desc = about
        profile.institution = inst
        if image or resume:
            profile.profile_image = image
            profile.resume = resume
        # try:
        #     p = Profile.objects.get(id = id)
        #     print(p.user)
        # except:
        #     raise ValueError
        if skill:
            profile.skills.clear()
            for i in range(len(skill)):
                print(skill[i])
                profile.skills.add(int(skill[i]))
        
        sample= request.FILES.get('resume',None)
        if sample:
            reader = PdfReader(sample)
            num_pages = len(reader.pages)
            for i in range(num_pages):
                page = reader.pages[i]  
                text = page.extract_text()
                combined_text += text
        else:
            if request.user:
                user = request.user
                if user:
                    p = Profile.objects.get(user=user)
                    data = p.resume_data
                    print(data, "-------------------data")  
                    print(type(data), "-------------------data-Type")          
                    combined_text += data
                else:
                    combined_text = "Unable to add"
                    messages.error(request,"User Not Found")
        
        profile.resume_data = combined_text
        profile.save()
        user.save()
        print("success")
        return redirect("/user-profile/")
    

    context={
        "skill":skills,
        "profile":profile
    }

    return render(request,'update_profile.html',context)