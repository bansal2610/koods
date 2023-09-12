"""
URL configuration for koods project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from koods import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.Home,name="home"),
    path('courses/', views.Course),
    path('course-details/<slug>', views.CourseDetails),
    path('jobs/', views.Jobs),
    path('job-details/<slug>', views.jobDetails),
    path('sign-in/', views.signIn,name="signin"),
    path('sign-up/', views.signUp,name="signup"),
    path('log-out/', views.logOut,name="logout"),
    path('accounts/', include('allauth.urls')),
    path('user-profile/', views.ProfileUpdateView,name="profile"),
    # path('user-profile/', views.ProfileUpdateView.as_view(),name="profile"),
    path('add_jobs/',views.Add_jobs,name="addjob"),
    path('add_course/',views.Add_course,name="addcourse"),
    path('forget/',views.password_reset_request,name="forget"),
    path('change_password/',views.change_pass,name="change_pass"),
    path('verify-otp/',views.verify_otp,name="verify_otp"),
    path('update-profile/<str:id>/', views.update_profile),
    path('jobprofile/',views.Jobprofile),
    path('error-404/',views.Error),
    path('test/',views.Test,name="test")
    # path('work_p/', views.work_position, name="work_prosition"),
    # path("data/",views.insert_skill),

]
urlpatterns += staticfiles_urlpatterns()
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)