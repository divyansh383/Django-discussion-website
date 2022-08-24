from pyexpat import model
from attr import field
from django.forms import ModelForm
from .models import Room, Message, Topic, profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
class RoomForm(ModelForm):
    class Meta:
        model=Room
        fields="__all__"   #cretes  a form for every  ttribute in the class
        exclude=['host','participants']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email']

class NewForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password1','password2']


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['body']

class TopicForm(ModelForm):
    class Meta:
        model = Topic
        fields = "__all__"

class UserProfileForm(ModelForm):
    class Meta:
        model = profile
        fields = ['bio','pp']