from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from .models import Tutorial
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
# Create your views here.


def homepage(request):
    tutorials= Tutorial.objects.order_by('-tutorial_published')
    paginator=Paginator(tutorials,2)
    page=request.GET.get('page')
    paged_tutorials=paginator.get_page(page)

    context={"tutorials": paged_tutorials, "title": "Home","all_tutorials":tutorials}

    return render(request=request, template_name='main/home.html',context=context)

def tutorial(request,tutorial_id):
    tutorial=get_object_or_404(Tutorial,pk=tutorial_id)
    tutorials=Tutorial.objects.order_by('-tutorial_published').filter(tutorial_category=tutorial.tutorial_category)
    context={
        "tutorial":tutorial,
        "tutorials":tutorials,
        "title":"Tutorial"
            }
    return render(request,'main/tutorial.html',context)

def search_results(request):
    if request.method == 'POST':
        search=request.POST['search']
        tutorials=list(Tutorial.objects.order_by('-tutorial_published').filter(tutorial_category__icontains=search))
        tutorials_title=Tutorial.objects.order_by('-tutorial_published').filter(tutorial_title__icontains=search)
        tutorials_summary=Tutorial.objects.order_by('-tutorial_published').filter(tutorial_summary__icontains=search)
        tutorials.extend(item for item in tutorials_title if item not in tutorials)
        tutorials.extend(item for item in tutorials_summary if item not in tutorials)
        context={
            "tutorials":tutorials,
            "title":"Search"
        }
        return render(request,'main/results.html',context)

def register(request):
    if request.method == 'POST':
        username = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(email=email).exists():
            messages.error(request, f"{email} is not valid")
            return redirect('/register')

        if User.objects.filter(username=username).exists():
            messages.error(request, f"{username} already exists")
            return redirect('/register')
        else:
            user = User.objects.create_user(
                username=username, password=password, email=email)
            user.save()
            login(request, user)
            messages.success(request, f"Welcome {username} !")
            return redirect('/')

    else:
        return render(request, 'user/register.html',context={"title":"Register"})

def logout_request(request):
    logout(request)
    messages.info(request, 'Logged out successfully')
    return redirect('/')

def login_request(request):
    if request.method == 'POST':
        username=request.POST['name']
        password = request.POST['password']
        user=authenticate(username=username,password=password)
        print(user)
        if user is not None:
            login(request,user)
            messages.success(request,"Welcome Back !")
            return redirect('/')
        else:
            messages.error(request,'Invalid Credentials')

    return render(request,'user/login.html',context={"title":"Login"})

