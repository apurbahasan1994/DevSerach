from django.shortcuts import redirect, render
from django.shortcuts import HttpResponse
from . import models
from .forms import ProjectForm, CustomUserCreationForm, Profile_Update_form, SklillForm, ReviewForm, MessageForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.


def login_page(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "username does not exist")
            return render(request, 'project/login.html')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("projects")
        else:
            messages.error(request, "Username or password incorrect")
            return render(request, 'project/login.html')
    return render(request, 'project/login.html')


def logout_user(request):
    logout(request)
    return redirect('/')


def home(request):
    page = None
    if request.GET.get('page'):
        page = request.GET.get('page')
    results = 3
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    skills = models.Skill.objects.filter(name__iexact=search_query)
    profiles = models.Profile.objects.distinct().filter(
        Q(name__icontains=search_query) | Q(short_intro__icontains=search_query) | Q(skill__in=skills))
    paginator = Paginator(profiles, results)
    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages

    leftIndex = (int(page)-4)
    if leftIndex < 1:
        leftIndex = 1
    rightIndex = (int(page)+5)
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages

    custom_range = range(leftIndex, rightIndex+1)
    context = {"profiles": profiles,
               'search_text': search_query, "paginator": paginator, "page": page, "custom_range": custom_range}
    return render(request, 'project/index.html', context)


@login_required(login_url="project/login")
def create_project(request):
    projects = models.Project.objects.all()
    form = ProjectForm()
    context = {"projects": projects, "form": form}
    return render(request, 'project/project_form.html', context)


@login_required(login_url="project/login")
def submit_project(request):
    owner = request.user.profile
    form = ProjectForm()
    if request.method == "POST":
        print(request.POST.getlist('tags'))
        newtags = request.POST.get('newtags').replace(',',  " ").split()
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = owner
            project.save()
            project.tags.add(*request.POST.getlist('tags'))

            for tag in newtags:
                tag, created = models.Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('userprofile', owner.id)

    context = {"form": form}
    return render(request, "project/project_form.html", context=context)


@login_required(login_url="project/login")
def update_project(request, pk):
    project = models.Project.objects.get(id=pk)
    form = ProjectForm(instance=project)
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {"form": form}
    return render(request, "project/Update_project.html", context)


@login_required(login_url="project/login")
def delete_project(request, pk):
    project = models.Project.objects.get(id=pk)
    project.delete()
    return redirect('useraccount')


def projects(request):
    page = None
    if request.GET.get('page'):
        page = request.GET.get('page')
    results = 3
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    projects = models.Project.objects.distinct().filter(
        Q(title__icontains=search_query))
    paginator = Paginator(projects, results)
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        projects = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
    leftIndex = (int(page)-4)
    if leftIndex < 1:
        leftIndex = 1
    rightIndex = (int(page)+5)
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages

    custom_range = range(leftIndex, rightIndex+1)
    context = {"projects": projects,
               "search_query": search_query, "paginator": paginator, "custom_range": custom_range, "page": page}
    return render(request, 'project/projects.html', context)


def signup(request):
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, "Invalid fields")
    return render(request, 'project/signup.html', {"form": form})


def single_project(request, pk):
    project = models.Project.objects.get(id=pk)
    profile = project.owner
    form = ReviewForm()
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.project = project
            review.owner = profile
            review.save()
            project.voteCount
            return redirect('single_project', pk=project.id)
    project = models.Project.objects.get(id=pk)
    return render(request, 'project/single-project.html', {"project": project, "form": form})


def profile_page(request, pk):
    profile = models.Profile.objects.get(id=pk)
    top_skills = profile.skill_set.exclude(description__exact="")
    other_skills = profile.skill_set.filter(description="")
    return render(request, "project/profile.html", {"profile": profile, "top_skills": top_skills, "other_skills": other_skills})


@login_required(login_url="project/login")
def useraccount(request):
    profile = request.user.profile
    skills = profile.skill_set.all
    projects = profile.project_set.all
    return render(request, 'project/account.html', {"profile": profile, "skills": skills, "projects": projects})


@login_required(login_url='project/login')
def update_profile(request):
    profile = request.user.profile
    form = Profile_Update_form(instance=profile)
    if request.method == "POST":
        form = Profile_Update_form(
            request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('useraccount')
    return render(request, 'project/profile_form.html', {"form": form})


@login_required(login_url='project/login')
def addskill(request):
    page = "addskill"
    owner = request.user.profile
    form = SklillForm()
    if request.method == "POST":
        form = SklillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = owner
            skill.save()
            return redirect('useraccount')
    return render(request, 'project/skill_form.html', {"form": form, "page": page})


@login_required(login_url='project/login')
def deleteskill(request, pk):
    profile = request.user.profile
    skill = models.Skill.objects.get(id=pk)
    profile.skill_set.remove(skill)
    return redirect('useraccount')


@login_required(login_url='project/login')
def editskill(request, pk):
    page = 'editskill'
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SklillForm(instance=skill)
    if request.method == "POST":
        form = SklillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            return redirect('useraccount')
    return render(request, 'project/skill_form.html', {"form": form, "page": page})


@login_required(login_url='project/login')
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()
    context = {"messageRequests": messageRequests, "unreadCount": unreadCount}
    return render(request, 'project/inbox.html', context=context)


@login_required(login_url='project/login')
def view_message(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    return render(request, 'project/message.html', {"message": message})


@login_required(login_url='project/login')
def sendmessage(request, pk):
    try:
        sender = request.user.profile
    except:
        sender = None
    form = MessageForm()
    receiver = models.Profile.objects.get(id=pk)
    if request.method == "POST":
        form = MessageForm(request.POST)
        message = form.save(commit=False)
        if sender:
            message.name = sender
        message.sender = sender
        message.receiver = receiver
        message.save()
        return redirect('message')
    return render(request, 'project/message_form.html', {"form": form, 'receiver': receiver})
