from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_messages, name="get-messages"),
    path('create-thread/', views.create_thread, name="create-thread"),
    path('read/', views.read_message, name="read-message"),
    path('create/', views.create_message, name="create-message"),
     path('groups/', views.get_groups, name="get-groups"),

    path('chats/', views.get_chat_list, name="get-chats"),

    path('thread/', views.create_or_get_thread, name='create_or_get_thread'),
    path('message/<thread_id>', views.create_new_message, name='create_message'),
    path('messages/', views.get_messages, name='get_messages'),
]
