from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from newsapi import NewsApiClient
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth import logout as django_logout
from django.views.decorators.cache import never_cache
from apidataget.forms import CustomUserCreationForm, ArticleForm
from .models import Save
import datetime
from django.contrib import messages


def index(request):
    newsapi = NewsApiClient(api_key='f7034c78f0b14f58908af1b25aa28c9a')
    top_headline = newsapi.get_top_headlines(country='in', language='en')
    return render(request, "apidataget/search.html", {'des': top_headline['articles']})


def category(request, type):
    form = ArticleForm()
    newsapi = NewsApiClient(api_key='f7034c78f0b14f58908af1b25aa28c9a')
    top_headline = newsapi.get_top_headlines(country='in', language='en', category=type)
    return render(request, "apidataget/front.html", {'des': top_headline['articles'], 'form': form, 'type': type})


def search(request):
    if request.method == 'GET':
        data = request.GET['var']
        newsapi = NewsApiClient(api_key='f7034c78f0b14f58908af1b25aa28c9a')
        all_articles = newsapi.get_everything(q=data, language='en')
        return render(request, "apidataget/front.html", {'des': all_articles['articles']})

    else:
        return HttpResponse("Search not found")



def login(request):
    if (request.method == 'POST'):
        username = request.POST['username']
        password = request.POST['password1']
        user = authenticate(request, username=username, password=password)
        if (user is not None):
            if user.is_active:
                request.session.set_expiry(86400)
                auth_login(request, user)
                return HttpResponseRedirect(reverse('home'))
        else:
            form = UserCreationForm()
            messages.warning(request,"This account doesnt exist")
            return render(request,"apidataget/login.html",{'form': form})
    else:
        form = UserCreationForm()
        return render(request, "apidataget/login.html", {'form': form})


def home(request):
    newsapi = NewsApiClient(api_key='f7034c78f0b14f58908af1b25aa28c9a')
    top_headline = newsapi.get_top_headlines(country='in', language='en')
    business=newsapi.get_top_headlines(country='in', language='en',category='business')
    sports = newsapi.get_top_headlines(country='in', language='en', category='sports')
    entertainment = newsapi.get_top_headlines(country='in', language='en', category='entertainment')
    health = newsapi.get_top_headlines(country='in', language='en', category='health')
    science = newsapi.get_top_headlines(country='in', language='en', category='science')
    technology = newsapi.get_top_headlines(country='in', language='en', category='technology')
    return render(request, "apidataget/home.html", {'top_headline':top_headline['articles'][:4],'business':business['articles']
                                                    ,'sports':sports['articles'],'entertainment':entertainment['articles']
                                                    ,'health':health['articles'],'science':science['articles'],'technology':
                                                        technology['articles']})


def logout(request):
    django_logout(request)
    return redirect('home')


@never_cache
def signup(request):
    if request.method == 'POST':
        f = CustomUserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            username = f.cleaned_data['username']
            password = f.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    request.session.set_expiry(86400)  # sets the exp. value of the session
                    auth_login(request, user)
                    return redirect('home')

    else:
        f = CustomUserCreationForm()

    return render(request,'apidataget/signup.html',{'form':f})


@login_required(login_url='/login/')
def save(request, type):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id=request.user.id)
            article = Save.objects.create(sid=user, article_title=form.cleaned_data['article_title'],
                                          article_description=form.cleaned_data['article_description'],
                                          article_image=form.cleaned_data['article_image'],
                                          article_url=form.cleaned_data['article_url'],
                                          article_time=datetime.datetime.now())
            article.save()
            messages.success(request, "Your article has been saved successfully")
            return redirect('category', type=type)

        else:
            messages.warning(request, "You have already submitted the article")
            return redirect('category', type=type)


@login_required(login_url='/login/')
def article(request):
    save_article = Save.objects.filter(sid=request.user.id,
                                       article_time__gt=datetime.datetime.now() - datetime.timedelta(29))
    now = datetime.datetime.now()
    save_article = save_article.filter(article_time__lt=now).order_by('-article_time')
    return render(request, 'apidataget/user_article.html', {'article': save_article})
