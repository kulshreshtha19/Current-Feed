from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.http import HttpResponse
from newsapi import NewsApiClient
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login,authenticate
from django.contrib.auth import logout as django_logout
from django.views.decorators.cache import cache_control
from django.views.decorators.cache import never_cache
from apidataget.forms import UserForm,ArticleForm
from .models import Save
import datetime


def index(request):
    newsapi=NewsApiClient(api_key='f7034c78f0b14f58908af1b25aa28c9a')
    top_headline = newsapi.get_top_headlines(country='in',language='en')
    return render(request,"apidataget/search.html",{'des':top_headline['articles']})

def category(request,type):
    form=ArticleForm()
    newsapi = NewsApiClient(api_key='f7034c78f0b14f58908af1b25aa28c9a')
    top_headline = newsapi.get_top_headlines(country='in', language='en', category=type)
    return render(request, "apidataget/front.html", {'des': top_headline['articles'],'form':form})

def search(request):
    if request.method=='GET':
        data = request.GET['var']
        newsapi = NewsApiClient(api_key='f7034c78f0b14f58908af1b25aa28c9a')
        all_articles=newsapi.get_everything(q=data,language='en')
        return render(request, "apidataget/front.html", {'des': all_articles['articles']})

    else:
         return HttpResponse("Search not found")

@never_cache
def login(request):
    if(request.method=='POST'):
        username=request.POST['username']
        password=request.POST['password1']
        user=authenticate(request,username=username,password=password)
        if(user is not None):
            auth_login(request,user)
            return redirect('home')
        else:
            return HttpResponse("Please enter valid credentials")
    else:
        form=UserCreationForm()
        return render(request,"apidataget/login.html",{'form':form})

def home(request):
    return render(request,"apidataget/home.html",{})

def logout(request):
    django_logout(request)
    return redirect('home')

def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            auth_login(request, user)
            return redirect('home')

    else:
        form = UserForm()
        return render(request, 'apidataget/signup.html', {'form': form})


@login_required(login_url='/login/')
def save(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            user=User.objects.get(id=request.user.id)
            article=Save.objects.create(sid=user,article_title=form.cleaned_data['article_title'],
                                        article_description=form.cleaned_data['article_description'],
                                        article_image=form.cleaned_data['article_image'],
                                        article_url=form.cleaned_data['article_url'],article_time=datetime.datetime.now())
            article.save()
            return HttpResponse(article)

        else:
            return HttpResponse("You have already saved this article")

@login_required(login_url='/login/')
def article(request):
    save_article=Save.objects.filter(sid=request.user.id,article_time__gt=datetime.datetime.now()- datetime.timedelta(29))
    now=datetime.datetime.now()
    save_article=save_article.filter(article_time__lt=now).order_by('-article_time')
    return render(request,'apidataget/user_article.html',{'article':save_article})


