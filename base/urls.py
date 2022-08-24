#urls of base
from django.urls import path
from . import views

urlpatterns = [
    path("login/",views.loginpage,name="login-page"),
    path("logout/",views.logoutuser,name="logout"),
    path("register/",views.registerpage,name="register"),

    path('', views.home,name="home"),
    path('room/<str:pk>/',views.room,name="room"),

    path('profile/<str:pk>/',views.UserProfile,name="user-profile"),

    path("create-room/",views.createRoom,name="create-room"),
    path("update-room/<str:pk>",views.updateRoom,name="update-room"),
    path("delete-room/<str:pk>",views.deleteRoom,name="delete-room"),

    path("delete-msg/<str:pk>",views.deletemsg,name="delete-msg"),
    path("update-msg/<str:pk>",views.updatemsg,name="update-msg"),

    path("update-user/",views.updateuser,name="update-user"),

    path("add-topic/",views.addtopic,name="add-topic"),
    path("topic-list/",views.topicpg,name='topic-list')
]
