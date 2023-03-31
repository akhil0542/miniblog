from django.shortcuts import render, HttpResponseRedirect
from .forms import SignupForm, LoginForm, PostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Post
from django.contrib.auth.models import Group
# Create your views here.

# Home View
def home(request):
    posts = Post.objects.all()
    return render(request, 'blog/home.html', context={'posts': posts})

# About View
def about(request):
    return render(request, 'blog/about.html')

# Contact View
def contact(request):
    return render(request, 'blog/contact.html') 

# Signup View
def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='Author')
            user.groups.add(group)
            messages.success(request, 'Congratulations !! You have become an Author')
    else:        
        form = SignupForm()
    return render(request, 'blog/signup.html', context={'form': form}) 

# Login view
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Logged in Successfully !!')
                    return HttpResponseRedirect('/dashboard/')
        else:            
            form = LoginForm()
        return render(request, 'blog/login.html', context={'form': form}) 
    else:
        return HttpResponseRedirect('/dashboard/')    


# Dashboard view
def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        user = request.user
        full_name = user.get_full_name()
        groups = user.groups.all()
        return render(request, 'blog/dashboard.html', context={'posts': posts, 'full_name': full_name, 'groups': groups})
    else:
        return HttpResponseRedirect('/login/')    

# Logout view
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

# Add new post
def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                desc = form.cleaned_data['desc']
                post = Post(title=title, desc=desc)
                post.save()
                form = PostForm()
        else: 
            form = PostForm()               
        return render(request, 'blog/addpost.html', context={'form': form})
    else:
        return HttpResponseRedirect('/login/') 

# Update post
def update_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            post = Post.objects.get(pk=id)
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/dashboard/')
        else:
            post = Post.objects.get(pk=id)
            form = PostForm(instance=post)        
        return render(request, 'blog/updatepost.html', context={'form': form})
    else:
        return HttpResponseRedirect('/login/')        

# Delete post
def delete_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            post = Post.objects.get(pk=id)
            post.delete()
        return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')                 