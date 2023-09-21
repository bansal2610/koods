from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate,login,logout
from courses.models import Courses
from jobs.models import Category, Job
from koods.forms import ADDCOURSE, EDIT_DESC, EDITJOB, CreateUserForm
# from koods.forms import ProfileForm, UserForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib import messages
from django.urls import reverse_lazy
from PyPDF2 import PdfReader
from koods.settings import EMAIL_HOST_USER
from uploads.models import Industry, Profile, skil
import ast
from django.conf import settings
from django.core.mail import BadHeaderError, send_mail
from django.contrib.auth.models import User,Permission,Group
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user
import random
from uploads.views import data
from koods.forms import ADDJOB_DESC

def Test(request):
             
    data={
        'title':'Test'
    }
    return render(request,"test.html",data)

def Error(request):
    data={
        'title':'Error 404'
    }
    return render(request,"404.html",data)

def Home(request):
    data={
        'title':'Learnkoods'
    }
    return render(request,"home.html",data)

def Jobprofile(request):
    if not request.user.is_authenticated:
        return redirect("/")
    usr = request.user
    jobprofile = Job.objects.filter(user=usr)
    print(jobprofile,"===========jobdata")
    data={
        'title':'Learnkoods',
        'jobprofile':jobprofile
    }
    return render(request,"jobprofile.html",data)

def Jobs(request):  
    if request.user.is_authenticated:
        usr = request.user
        profile = Profile.objects.get(user= usr)
        if profile.is_job ==True:
            userr = User.objects.get(username = usr)
            userr.is_staff = True
            userr.save()
            group = Group.objects.filter(name='Add_Jobs').first()
            group.user_set.add(userr)
            permissions = Permission.objects.filter(content_type__app_label='jobs')
            for permission in permissions.all():
                group.permissions.add(permission)
        else:
            messages.error(request,"Not Permitted")
    jobData = Job.objects.all().order_by("-timestamp")
    data={
        'title':'Jobs',
        'jobData':jobData
    }
    return render(request,"jobs.html",data)

def jobDetails(request,slug):
    jobdetail = Job.objects.get(job_slug=slug)
    jb = jobdetail.skills_req.all()
    data={
        'jobdetail':jobdetail,
        'jb':jb
    }
    return render(request,"job-details.html",data)

def Add_jobs(request):
    if request.user.is_authenticated:
        if not request.user.profile.is_job == True:
            return redirect("/")    
    usr = request.user
    cat = Category.objects.all()
    skill = skil.objects.all()
    formss = ADDJOB_DESC() 
    if request.method == "POST":
        formss = ADDJOB_DESC(request.POST)
        if formss.is_valid():
            job_desc = formss.cleaned_data['job_des']
            comp_desc = formss.cleaned_data['company_desc']
            job_title = request.POST.get("job_title")
            company = request.POST.get('company')
            job_type = request.POST.get('job_type')
            category = request.POST.get('category')
            cat_id = Category.objects.get(id=category)
            exp_required = request.POST.get('exp_required')
            skills_required = request.POST.getlist('skills_req')
            # job_des = request.POST.get('job_des')
            min_salary = request.POST.get('min_salary')
            max_salary = request.POST.get('max_salary')
            location = request.POST.get('location')
            # company_desc = request.POST.get('company_desc')
            job_image = request.FILES.get("job_image", None)
            url = request.POST.get('url')
            print(skills_required,"======================Skill treq")

            jb = Job.objects.create(user=usr,job_title=job_title,company=company,job_type=job_type,category=cat_id,exp_required=exp_required,min_salary=min_salary,job_des=job_desc,max_salary=max_salary,location=location,company_desc=comp_desc,url=url)

            if job_image :
                jb.job_image = job_image
            
            if skills_required:
                for skk in range(len(skills_required)):
                    skill_data = skil.objects.get(data=skills_required[skk])
                    jb.skills_req.add(skill_data)

            print(jb,"+++++++++++jb")
            # print(usr,job_title,company,job_type,category,exp_required,skills_req,job_des,min_salary,max_salary,location,company_desc,job_image,url,"+==================title company")
            # jb.save()
            return redirect("/jobprofile/")
        else:
            formss = ADDJOB_DESC()
    data={
       'title':'Learnkoods',
       'cat':cat,
       'skill':skill,
       "form":formss,
    }
    # if request.user.is_authenticated:
    #     if not request.user.profile.is_job == True:
    #         return redirect("/")
    #     form = ADDJOB()
    #     if request.method == "POST":
    #         form = ADDJOB(request.POST, user=request.user)
    #         if form.is_valid():
    #             instance = form.save(commit=False)
    #             instance.user = request.user
    #             instance.save()
    #             return redirect('/jobs/')
    #         else:
    #             print("Form Error: ",form.errors)
    # else:
    #     return redirect("/")
    # data={
    #     'form':form
    # }
    return render(request,"add_jobs.html",data)

def editjob(request,id):    
    if request.user.is_authenticated:
        if not request.user.profile.is_job == True:
            return redirect("/")    
    usr = Job.objects.get(job_id=id) 
    cat = Category.objects.all()   
    skill = skil.objects.all()
    form = EDIT_DESC()

    # print(usr.skills_req.all(),"+++++++++++skillreq")
    if request.method == "POST":
        form = EDIT_DESC(request.POST, instance=usr)
        if form.is_valid():
            job_desc = form.cleaned_data['job_des']
            comp_desc = form.cleaned_data['company_desc']
        
        
        job_title = request.POST.get("job_title")
        company = request.POST.get('company')
        job_type = request.POST.get('job_type')
        category = request.POST.get('category')
        cat_id = Category.objects.get(id=category)
        exp_required = request.POST.get('exp_required')
        skills_required = request.POST.getlist('skills_req')
        min_salary = request.POST.get('min_salary')
        max_salary = request.POST.get('max_salary')
        location = request.POST.get('location')
        job_image = request.FILES.get("job_image", None)
        url = request.POST.get('url')

        if job_image :
            usr.job_image = job_image

        if skills_required:
            usr.skills_req.clear()

        usr.job_title=job_title
        usr.company=company
        usr.job_type=job_type
        usr.category=cat_id
        usr.exp_required=exp_required
        usr.job_des=job_desc
        usr.min_salary=min_salary
        usr.max_salary=max_salary
        usr.location=location
        usr.company_desc=comp_desc
        usr.url=url
        
        for skk in range(len(skills_required)):
            skill_data = skil.objects.get(data=skills_required[skk])
            usr.skills_req.add(skill_data)


        # print(job_title,company,job_type,category,exp_required,skills_required,job_des,min_salary,max_salary,location,company_desc,job_image,url,"+==================title company")
        usr.save()
        return redirect("/jobprofile/")
    else:
        form = EDIT_DESC(instance=usr)
    data={
       'title':'Learnkoods',
       'usr':usr,
       'cat':cat,
       'skill':skill,
       'form':form
    }
    # if request.user.is_authenticated:
    #     if not request.user.profile.is_job == True:
    #         return redirect("/")
    #     job = Job.objects.get(job_id=id)
    #     form = EDITJOB()
    #     if request.method == "POST":
    #         form = EDITJOB(request.POST, instance=job)
    #         if form.is_valid():    
    #             form.save()
    #             return redirect('/jobs/')
    #         else:
    #             form = EDITJOB(instance = job)
    #             print("Form Error: ",form.errors)
    # else:
    #     return redirect("/")
    # data={
    #     'title':'Learnkoods',
    #     'form':form,
    #     "job":job
    # }
    return render(request,"edit_job.html",data)

def delete_job(request, id):
    delt = Job.objects.get(job_id = id)
    delt.delete()
    return redirect('/jobprofile/')

def Course(request):
    if request.user.is_authenticated:
        usr = request.user
        profile = Profile.objects.get(user= usr)
        if profile.is_course ==True:
            userr = User.objects.get(username = usr)
            userr.is_staff = True
            userr.save()
            group = Group.objects.filter(name='Add_Course').first()
            group.user_set.add(usr)
            permissions = Permission.objects.filter(content_type__app_label='courses')
            for permission in permissions.all():
                group.permissions.add(permission)
        else:
            messages.error(request,"Not Permitted")
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

def Add_course(request):
    if not request.user.profile.is_course == True:
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


def signUp(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        
        if form.is_valid():  
            username = form.cleaned_data['username']
            
            # Check if the username already exists
            if User.objects.filter(username=username).exists():
                form.add_error(None, 'Username already exists.')
            else:
                # Save the user data to the database
                form.save()        
            messages.success(request,"Registered Successfully")
            return redirect("/sign-in")
       
            
    data={
        'title':'Sign Up',
        'form':form
    }
    return render(request,"signup.html",data)

def signIn(request):
    flag = "123"
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request,username=username,password=password)
        try:
            if user is not None:
                login(request,user)
                messages.success(request, f'Login Succesfull, Welcome {username}')
                if get_object_or_404(Profile, user = request.user):
                    p = get_object_or_404(Profile, user=request.user)

                    if p.work_at is None:
                        flag="yes"
                        print(flag,"============flag")
                        return redirect("/user-profile")
                    print(p.work_at, "============Work")
                    flag="NO"
                return redirect('/user-profile')
        except:
            messages.error(request, 'Invalid User')
    data={
        'title':'Sign In',
        'flag': flag
    }
    return render(request,"signin.html",data)

def logOut(request):
    logout(request)
    print("Logout Successfull")
    return redirect('/')

# def work_position(request):
#     inds = Industry.objects.all()
#     if request.method == "POST":
#         wor_at = request.POST.get("industry")
#         posi = request.POST.get("position")
#         indus_id = Industry.objects.get(id=posi)
#         p = Profile.objects.get(user=request.user)
#         p.work_at = wor_at
#         p.position = indus_id
#         p.save()
#         messages.success(request, "Thank You for Information")
#         return redirect("/user-profile")

#     context = {
#         "inds":inds
#     }
#     return redirect(request,context)

def ProfileUpdateView(request):
    if not request.user.is_authenticated:
        return redirect("/error-404/")
    usr = request.user
    p = Profile.objects.get(user=usr)
    pro_skill = p.skills.all()
    inds = Industry.objects.all()
    sk = skil.objects.all()
    if request.method == "POST":
        wor_at = request.POST.get("industry")
        posi = request.POST.get("position")
        res = request.FILES.get("resume", None)
        skill = request.POST.getlist("skills")
        pro_indus = Industry.objects.get(id = posi)
        if res:
            p.resume = res
            
        p.skills.clear()
        for skk in range(len(skill)):
            skill_data = skil.objects.get(data=skill[skk])
            print(skill_data,"==============Skill Data")
            p.skills.add(skill_data)

        combined_text = ""
        if res:
            reader = PdfReader(res)
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
                    combined_text += data
                else:
                    combined_text = "Unable to add"
                    messages.error(request,"User Not Found")
        
        p.resume_data = combined_text
        p.position = pro_indus
        p.work_at = wor_at 

        p.save()
        print(wor_at,posi,res,skill,"====================")
        print(type(skill),"====================type")

        messages.success(request, "Thank You for Information")
        return redirect("/user-profile")

    data={
        'title':'Learnkoods',
        'skill' :pro_skill,
        "inds":inds,
        "prof":p.work_at,
        "pro":p,
        "sk":sk
    }
    return render(request,"profile.html",data)

# class ProfileUpdateView(LoginRequiredMixin, TemplateView):
#     user_form = UserForm
#     profile_form = ProfileForm
#     template_name = 'profile.html'
#     login_url="/sign-in/"
    

#     def post(self, request):
#         post_data = request.POST or None
#         file_data = request.FILES or None
#         usr = request.user
#         p = Profile.objects.get(user= usr)
#         sk = p.skills.all()

#         user_form = UserForm(post_data, instance=request.user)
#         profile_form = ProfileForm(post_data, file_data, instance=request.user.profile)
#         try:
#             if user_form.is_valid() and profile_form.is_valid():
#                 sample= request.FILES['resume']
#                 if sample:
#                     reader = PdfReader(sample)
#                     num_pages = len(reader.pages)
#                     for i in range(num_pages):
#                         page = reader.pages[i]  
#                         text = page.extract_text()
#                     profile_form.instance.resume_data = text
                                
#                 user_form.save()
#                 profile_form.save()
#                 messages.error(request, 'Your profile is updated successfully!')
#                 return HttpResponseRedirect(reverse_lazy('profile'))
#         except Exception as e:
#             messages.error(request, "Not found")

#         context = self.get_context_data(
#                                         user_form=user_form,
#                                         profile_form=profile_form,
#                                         skill = sk
#                                     )

#         return self.render_to_response(context)     

#     def get(self, request, *args, **kwargs):
#         return self.post(request, *args, **kwargs)

def password_reset_request(request):
    rndm = random.randint(999,9999)
    request.session["otp"] = rndm
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
                f"Your OTP :{rndm}",
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
#     # Industry.objects.all().delete()
#     d = data()
#     for i in range(len(d)):
#         Industry.objects.create(name = d[i])
#         # skil.objects.create(data = d[i])
#     return HttpResponse("skill Created")

# def update_profile(request,id):
#     skills = skil.objects.all()
#     inds= Industry.objects.all()
#     print(id,"===================id")
#     user = User.objects.get(username=id)

#     profile = Profile.objects.get(user=user)
#     print(profile,"================profile")
#     num= str(profile.phone)[3::]
    
#     combined_text = ""
#     if request.method == "POST":
#         username = request.POST.get("username")
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get("last_name")
#         email = request.POST.get("email")
#         about = request.POST.get("about")
#         work_at = request.POST.get("work_at")
#         position = request.POST.get("position")
#         gender = request.POST.get("gender")
#         phone = request.POST.get("phone")
#         inst = request.POST.get("inst")
#         skill = request.POST.getlist("skills")
#         resume = request.FILES.get("resume", None)
#         image = request.FILES.get("image", None)
        
#         user.username = username
#         user.first_name = first_name
#         user.last_name = last_name
#         user.email = email
#         profile.gender = gender
#         profile.phone = phone
#         profile.work_at = work_at
#         profile.profile_desc = about
#         print("====================",position, "========================Position")
#         if not position =="Select Position":
#             pro_indus = Industry.objects.get(id = position)
#             profile.position = pro_indus
#         else:
#             profile.position = None
        
#         profile.institution = inst
#         if image or resume:
#             profile.profile_image = image
#             profile.resume = resume
#         # try:
#         #     p = Profile.objects.get(id = id)
#         #     print(p.user)
#         # except:
#         #     raise ValueError
#         if skill:
#             profile.skills.clear()
#             for i in range(len(skill)):
#                 profile.skills.add(int(skill[i]))
        
#         sample= request.FILES.get('resume',None)
#         if sample:
#             reader = PdfReader(sample)
#             num_pages = len(reader.pages)
#             for i in range(num_pages):
#                 page = reader.pages[i]  
#                 text = page.extract_text()
#                 combined_text += text
#         else:
#             if request.user:
#                 userr = request.user
#                 if userr:
#                     p = Profile.objects.get(user=userr)
#                     data = p.resume_data         
#                     combined_text += data
#                 else:
#                     combined_text = "Unable to add"
#                     messages.error(request,"User Not Found")
        
#         profile.resume_data = combined_text
#         profile.save()
#         user.save()
#         print("success")
#         return redirect("/user-profile/")
    

#     context={
#         "skill":skills,
#         "profile":profile,
#         "num":num,
#         "inds":inds,
#         "title":'Update Profile'
#     }

#     return render(request,'update_profile.html',context)



# new

def update_profile(request,id):
    lst = []
    skills = list(skil.objects.all())
    lst = [ str(t) for t in skills ]
    user = User.objects.get(username=id)
    profile = Profile.objects.get(user=user)
    inds = Industry.objects.all()
    num= str(profile.phone)[3::]

    combined_text = ""
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
        work_at = request.POST.get("work_at")
        position = request.POST.get("position")
        
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        profile.gender = gender
        profile.phone = phone
        profile.profile_desc = about
        profile.institution = inst
        profile.work_at = work_at
        pro_indus = Industry.objects.get(id = position)
        profile.position = pro_indus
        
        if image or resume:
            profile.profile_image = image
            profile.resume = resume

        if skill:
            lst2 = []
            for m in range(len(skill)):
                lst2.append(skill[m])
            for k in range(len(lst2)):
                if lst2[k] not in lst:
                    skil.objects.create(data=lst2[k])
                    lst.append(lst2[k])
            profile.skills.clear()
            for sk in range(len(skill)):
                if skill[sk] in lst:
                    skill_data = skil.objects.get(data=skill[sk])
                    profile.skills.add(skill_data)
        
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
        "profile":profile,
        "inds":inds,
        "num":num
    }

    return render(request,'update_profile.html',context)