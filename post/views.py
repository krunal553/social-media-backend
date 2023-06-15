from contextlib import nullcontext
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from post.models import Post, PostComment
from post.serializers import PostSerializer, CreatePostSerializer
import random

from itertools import chain
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User, auth
from django.contrib.auth.hashers import make_password
from rest_framework import status

from notifications.models import Notification

# from .tempData import *

from post.models import Post, PostComment
from user.models import UserProfile
from post.serializers import PostCommentSerializer, PostSerializer

from sociobackend.utils import time_formating

# for otp_signup
import random
from django.conf import settings
from django.core.mail import send_mail


@api_view(['GET'])
def user_feed_list(request):
    paginator = PageNumberPagination()
    paginator.page_size = 5  # number of objects per page
    # paginator.page_size = request.GET.get('size')  # number of objects per page
    queryset = Post.objects.all()  # get all objects
    result_page = paginator.paginate_queryset(queryset, request)
    serializer = PostSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


# ====================================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def userFeed(request):  
    user_object = User.objects.get(username=request.user.username)
    user_profile = UserProfile.objects.get(user=request.user)

    user_following_list = []
    feed = []

    user_following = request.user.following.all()

    for users in user_following:
        user_following_list.append(users.user)
        # print(user_following_list)

    for usernames in user_following_list:
        
        feed_lists = Post.objects.filter(user=usernames).order_by('-timestamp')
        
        serializer = PostSerializer(feed_lists, many=True)
        feed += serializer.data
        # print(feed)
        # serializer.append(serializer)

    # feed_list = list(chain(feed))
    # print(feed)
    
    return Response(feed)

@api_view(['GET']) 
@permission_classes([IsAuthenticated])
def user_feed(request):
    curr_user = request.user
    following_users = curr_user.following.all().values_list('user', flat=True)
    posts = Post.objects.filter(user__in=following_users).order_by('-timestamp')

    paginator = PageNumberPagination()
    paginator.page_size = 5
    paginated_posts = paginator.paginate_queryset(posts, request)

    serializer = PostSerializer(paginated_posts, many=True)
    return Response(serializer.data)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getExplorePosts(request):
    usr = []
    for this_usr in request.user.following.all():
        usr.append(this_usr.user)

    posts = Post.objects.exclude(user=request.user).exclude(user__in=usr)
    
    # Shuffle the queryset randomly
    posts = posts.order_by('?')
    # posts = sorted(posts, key=lambda x: random.random())

    serialized_posts = PostSerializer(posts, many=True)
    
    return Response(serialized_posts.data)

@api_view(['GET'])
def getPost(request, pk):
    post = Post.objects.get(_id=pk)
    # print(post)
    serializer = PostSerializer(post, many=False)
    # print(serializer.data)

    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getCurrUserPosts(request, username):
    # user = User.objects.get(username = username)
    user = request.user
    if request.user.username == username:
        user = request.user
    else:
        user = User.objects.get(username = username)

    posts = Post.objects.filter(user=user).select_related('user').order_by('-timestamp')

    serializer = PostSerializer(posts, many=True)
    
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createPost(request):
    data = request.data
    # data['user'] = request.user.id
    # print (data)
    # data['user'] = request.user
    # print (data)
    serializer = CreatePostSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deletePost(request, post_id):
    if Post.objects.filter(user= request.user, _id = post_id).exists():
        Post.objects.filter(user= request.user, _id = post_id).delete()
        return Response(f"deleted {request.user}'s post")
    return Response("no post like that exist", status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_post(request, post_id):
    user = request.user


    # data = request.data
    # user = User.objects.get(username=data)

    try:
        post_to_like = Post.objects.get(_id = post_id)

        if user in post_to_like.likers.all():
            post_to_like.likers.remove(user)
            post_to_like.likes_count = post_to_like.likers.count()
            post_to_like.save()
            notification = Notification.objects.filter(created_by=request.user, message='liked your post', to_user=post_uploader ).first()
            if notification.exists():
                notification.delete()

            return Response('Post unliked')
        else:
            post_to_like.likers.add(user)
            post_uploader = post_to_like.user
            post_to_like.likes_count = post_to_like.likers.count()
            post_to_like.save()
            notification = Notification.objects.create(created_by=request.user, message='liked your post', to_user=post_uploader )
            return Response('Post liked')

    except Exception as e:
        message = {'detiail':f'{e}'}
        return Response(message, status = status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getIsPostLiked(request, post_id):
    user = request.user
    try:
        post_to_check = Post.objects.get(_id = post_id)

        if user in post_to_check.likers.all():
            return Response(True)
        else:
            return Response(False)
        
    except Exception as e:
        message = {'detiail':f'{e}'}
        return Response(message, status = status.HTTP_204_NO_CONTENT)



@api_view(['GET'])
def getPostComment(request, pid):
    post_comments = PostComment.objects.filter(post_id=str(pid))
    serializer = PostCommentSerializer(post_comments, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def setPostComment(request):
    data = request.data
    # data['user'] = 1
    serializer = PostCommentSerializer(data=data)

    if serializer.is_valid():
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deletePostComment(request, comment_id):
    if PostComment.objects.filter(user= request.user, id = comment_id).exists():
        PostComment.objects.filter(user= request.user, id = comment_id).delete()
        return Response(f"deleted {request.user}'s comment")
    return Response("no post comment like that exist")



