from email import message
from email.quoprimime import body_check
from django.contrib.auth.signals import user_logged_in
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q #for || && !
from django.http import HttpResponse
from django.urls import is_valid_path
from .models import Message, Room, Topic, Message, profile
from .forms import RoomForm, UserForm, MessageForm, TopicForm, NewForm, UserProfileForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required #to restrict pges

# Create your views here.

# rooms=[
#     {"id":1,"name":"web dev"},
#     {"id":2,"name":"python programming"},
#     {"id":3,"name":"dsa"},
# ]

def loginpage(request):
    page="login"
    if request.user.is_authenticated:
        return redirect("home")

    if request.method=="POST":
        username=request.POST.get('username').lower()
        password=request.POST.get('password')

        user=authenticate(request, username=username, password=password)   #chec if creentis re true
        if user is not None:
            login(request,user)
            return redirect("home")
        else:
            messages.error(request,"Username or password does not exist")
    context={"page":page}
    return render(request,'base/login_register.html',context)
    
def logoutuser(request):
    logout(request)
    #return render(request,'base/login_register.html')
    return redirect("home")

def registerpage(request):
    page="register"
    form=NewForm()
    profile=UserProfileForm()
    if request.method=="POST":
        form=NewForm(request.POST)
        profile=UserProfileForm(request.POST)
        if form.is_valid() and profile.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            prof=profile.save(commit=False)
            prof.user=user
            prof.save()
            login(request,user)
            return redirect("home")
        else:
            messages.error(request,"error occured")

    context={"page":page,"form":form ,"profile":profile}
    return render(request,'base/login_register.html',context)

def home(request):
    q=request.GET.get('q') if request.GET.get('q')!=None  else ''
    if request.user.is_authenticated:
        prof=profile.objects.get(user=request.user)
    else:
        prof=None
    topics=Topic.objects.all().order_by('-created')
    rooms=Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) 
    )
    room_count=rooms.count()
    room_messages=Message.objects.filter(
        Q(room__name__icontains=q) |
        Q(room__topic__name__icontains=q)
    )

    parameters={"rooms":rooms,"topics":topics,"q":q,"room_count":room_count,"room_messages":room_messages,"prof":prof}
    return render(request,"base/home.html",parameters)  #vribes in the orm o ictinotionry

def room(request,pk):
    room=Room.objects.get(id=pk)
    room_messages=room.message_set.all().order_by('created')
    participants=room.participants.all()
    if request.user.is_authenticated:
        prof=profile.objects.get(user=request.user)
    else:
        prof=None
    body=request.POST.get('body')
    if body != "":
        if request.method=="POST":
            message = Message.objects.create(
                user=request.user,  
                room=room,
                body=request.POST.get('body'),
            )
            room.participants.add(request.user)
            return redirect('room',pk=room.id)
    

    context={"room":room,"room_messages":room_messages,"participants":participants,"prof":prof}
    return render(request,"base/room.html",context)

@login_required(login_url="login-page")
def createRoom(request):
    form=RoomForm()
    if request.user.is_authenticated:
        prof=profile.objects.get(user=request.user)
    else:
        prof=None
    #processing info
    if request.method =="POST":
        #print(request.POST)         #request.POST store form info in form of ictionry
        form=RoomForm(request.POST)
        if form.is_valid():
            room=form.save(commit=False)
            room.host=request.user
            room.save()
            return redirect("home")
    context={'form':form,"prof":prof}
    return render(request,"base/bsform.html",context)

@login_required(login_url="login-page")
def updateRoom(request,pk):
    if request.user.is_authenticated:
        prof=profile.objects.get(user=request.user)
    else:
        prof=None

    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room) #prefilled form
    if request.user != room.host:
        return HttpResponse("Only owner can edit the room")

    if request.method =="POST":
        form=RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect("home")

    context={"form":form,"prof":prof}
    return render(request,"base/bsform.html",context)

@login_required(login_url="login-page")
def updatemsg(request,pk):
    page="editmsg"
    if request.user.is_authenticated:
        prof=profile.objects.get(user=request.user)
    else:
        prof=None
    room_message=Message.objects.get(id=pk)
    form=MessageForm(instance=room_message) #prefilled form
    if request.user != room_message.user:
        return HttpResponse("Only owner can edit the message")

    if request.method =="POST":
        form=MessageForm(request.POST, instance=room_message)
        if form.is_valid():
            form.save()
            return redirect('home')

    context={"form":form,"page":page,"prof":prof}
    return render(request,"base/login_register.html",context)

@login_required(login_url="login-page")
def updateuser(request):
    user=request.user
    prof=profile.objects.get(user=request.user)
    form=UserForm(instance=user)
    prof_form=UserProfileForm(instance=prof)
    if request.method=="POST":
        form=UserForm(request.POST,instance=request.user)
        prof_form=UserProfileForm(request.POST,request.FILES,instance=prof)
        if form.is_valid() and prof_form.is_valid():
            form.save()
            prof_form.save()
            return redirect("user-profile",pk=user.id)

    context={"form":form,"prof_form":prof_form,"prof":prof}
    return render(request,'base/update-user.html',context)

@login_required(login_url="login-page")
def deleteRoom(request,pk):
    if request.user.is_authenticated:
        prof=profile.objects.get(user=request.user)
    else:
        prof=None
    room=Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse("Only owner can edit the room")
    if request.method =="POST":
        room.delete()
        return redirect("home")
    return render(request,"base/del.html",{"obj":room,"prof":prof})



@login_required(login_url="login-page")
def deletemsg(request,pk):
    message=Message.objects.get(id=pk)
    if request.user.is_authenticated:
        prof=profile.objects.get(user=request.user)
    else:
        prof=None
    if request.user != message.user:
        return HttpResponse("Only owner can edit the room")
    if request.method =="POST":
        message.delete()
        return redirect("home")
    return render(request,"base/del.html",{"obj":message,"prof":prof})

def UserProfile(request,pk):
    if request.user.is_authenticated:
        prof=profile.objects.get(user=request.user)
    else:
        prof=None
    user=User.objects.get(id=pk)
    profp=profile.objects.get(user=user)
    rooms=user.room_set.all()
    room_messages=user.message_set.all()
    topic=Topic.objects.all()
    context={"user":user,"rooms":rooms,"room_messages":room_messages,"topics":topic,"prof":prof,"profp":profp}
    return render(request,"base/profile.html",context)



@login_required(login_url="login-page")
def addtopic(request):
    page="topic"
    if request.user.is_authenticated:
        prof=profile.objects.get(user=request.user)
    else:
        prof=None
    form=TopicForm()
    if request.method =="POST":
        form=TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")

    context={'form':form,"page":page,"prof":prof}
    return render(request,"base/login_register.html",context)

def topicpg(request):
    topics=Topic.objects.all().order_by('-created')
    if request.user.is_authenticated:
        prof=profile.objects.get(user=request.user)
    else:
        prof=None
    context={'topics':topics,"prof":prof}
    return render(request,"base/topics.html",context)