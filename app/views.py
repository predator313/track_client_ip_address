from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import SignupForm,LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from .models import Post
from .forms import PostForm
from django.contrib.auth.models import Group #the delete permission is only for admin
#author groups member has no delete righ

# Create your views here.
#home page view
def Home(request):
    posts=Post.objects.all()
    return render(request,'app/home.html',{'posts':posts})

#about view
def About(request):
    return render(request,'app/about.html')
#contact page
def Contact(request):
    return render(request,'app/contact.html')

#for dashboard
def Dashboard(request):
    if request.user.is_authenticated:
     posts=Post.objects.all()
     return render(request,'app/dashboard.html',{'posts':posts})
    else:
        return HttpResponseRedirect('/login/')

#for signup
def Signup(request):
    if request.method=="POST":
        fm=SignupForm(request.POST)
        if fm.is_valid():
            messages.success(request,'congratulations you now become auther')
            user=fm.save()
            group=Group.objects.get(name='Author')
            user.groups.add(group)
    else:
       fm=SignupForm()
    return render(request,'app/signup.html',{'form':fm})
#for login
def Login(request):
    # if not request.user.is_authenticated:
    if not request.user.is_authenticated:
        if request.method=="POST":
            fm=LoginForm(request=request,data=request.POST)
            if fm.is_valid():
                uname=fm.cleaned_data['username']
                upass=fm.cleaned_data['password']
                user=authenticate(username=uname,password=upass)
                if user:
                    login(request,user)
                    # messages.success(request,'successfully logged in !!!')
                    return HttpResponseRedirect('/dash/')
        else:
            fm=LoginForm()
        return render(request,'app/login.html',{'form':fm})
    else:
        return HttpResponseRedirect('/dash/')
#for logout
def Logout(request):
    logout(request)
    messages.success(request,'successfully logout')
    return HttpResponseRedirect('/login/')

#for adding new post
def add_post(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            fm=PostForm(request.POST)
            if(fm.is_valid()):
                fm.save()
                fm=PostForm()
        else:
            fm=PostForm()

        return render(request,'app/addpost.html',{'form':fm})
    else:
        return HttpResponseRedirect('/login/')

#for updating post
def Update_post(request,id):
    if request.user.is_authenticated:
        if request.method=='POST':
            pi=Post.objects.get(pk=id)
            fm=PostForm(request.POST,instance=pi)
            if fm.is_valid():
                fm.save()
        else:
            pi=Post.objects.get(pk=id)
            fm=PostForm(instance=pi)
        return render(request,'app/updatepost.html',{'form':fm})
    else:
        return HttpResponseRedirect('/login/')

#for deleting post
def delete_post(request,id):
    if request.user.is_authenticated:
        if request.method=='POST':
            pi=Post.objects.get(pk=id)
            pi.delete()
            return HttpResponseRedirect('/dash/')
    else:
        return HttpResponseRedirect('/login/')


