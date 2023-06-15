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
from django.core.exceptions import ObjectDoesNotExist
from notifications.models import Notification

from user.models import *
from user.serializers import *
from chat.models import Thread

# for otp_signup
import random
from django.conf import settings
from django.core.mail import send_mail

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


# ==========================================================================

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['POST'])
def signupUser(request):
    data = request.data

    try:
        user = User.objects.create(
            first_name = data['username'],
            username = data['username'],
            email = data['email'],
            password = make_password(data['password'])
        )
        # user_prof = UserProfile.objects.create(user=user, username=user.username, name=user.username)
        # user_prof.save()
        serializer = UserSerializerWithToken(user, many=False)
        return Response({'success': True,'data':serializer.data})
    # except:
    #     message = {'detail':'User with this email already exists'}
    except Exception as e:
        message = {'detiail':f'{e}'}
        return Response(message, status= status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getCurrentUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    print("user")
    print(user)

    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request, username):
    logged_user = request.user
    user = User.objects.get(username= username)
    user_profile = user.userprofile
    serializer = UserProfileSerializer(user_profile, many=False)
    

    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def following(request):
    user = request.user
    following = user.following.all()
    serializer = UserProfileSerializer(following, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request, username):
    user = request.user

    try:
        user_to_follow = User.objects.get(username=username)
        user_to_follow_profile = user_to_follow.userprofile

        if user == user_to_follow:
            return  Response("You can not follow yourself")

        if user in user_to_follow_profile.followers.all():
            user_to_follow_profile.followers.remove(user)
            user_to_follow_profile.followers_count = user_to_follow_profile.followers.count()
            user_to_follow_profile.save()
            notification = Notification.objects.filter(created_by=request.user, message='started following you...', to_user=user_to_follow_profile.user ).first()
            if notification.exists():
                notification.delete()
            return Response('User unfollowed')
        else:
            user_to_follow_profile.followers.add(user)
            user_to_follow_profile.followers_count = user_to_follow_profile.followers.count()
            user_to_follow_profile.save()
            notification = Notification.objects.create(created_by=request.user, message='started following you...', to_user=user_to_follow_profile.user )


            # if not Thread.objects.filter(sender=user, reciever=user_to_follow).exists():
            #     thread = Thread.objects.create(sender=user, reciever=user_to_follow)
            #     thread.save()

            return Response('User Followed')

    except Exception as e:
        message = {'detail': f'{e}'}
        return Response(message, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getIsFollowing(request, username):
    user = request.user
    try:
        user_to_check = User.objects.get(username=username)
        user_to_check_profile = user_to_check.userprofile
        
        if user in user_to_check_profile.followers.all():
            return Response(True)
        else:
            return Response(False)
        
    except Exception as e:
        message = {'detiail':f'{e}'}
        return Response(message, status = status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    users = User.objects.all()

    serializer = UserSerializer(users, many=True)

    return Response(serializer.data)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def searchUser(request):
    user_object = request.user
    username = request.GET.get('username')
    # username = request.data['username']
    print(username)
    username_object = User.objects.filter(username__icontains=username)
    print(username_object)



    serializer = UserSerializer(username_object, many= True)
    usr = serializer.data

    


    username_profile = []
    username_profile_list = []

    for users in username_object:
            username_profile.append(users.userprofile)

    print(username_profile)

    user_profile_ser = UserProfileSerializerWithLessDetails(username_profile, many = True)

    # for users in username_object:
    #         profile_lists = UserProfile.objects.get(user=users)
    #         print(profile_lists)
    #         serializer = UserProfileSerializer(profile_lists, many=False)
    #         print(serializer.data)
    #         username_profile_list += serializer.data
            # username_profile_list.append(serializer)
          
    # username_profile_list = list(chain(*username_profile_list))
    
    # return render(request, 'search.html', {'user_profile': user_profile, 'username_profile_list': username_profile_list})

    return Response({'user_list': user_profile_ser.data})
    # return Response({'username_profile_list': username_profile_list})



# =================== otp_signup =============================== #

@api_view(['POST'])
def send_otp(request):
    email = request.data.get('email')
    if email:
        # Generate 6 digit random OTP
        otp = str(random.randint(100000, 999999))
        message = f'Your OTP is: {otp}\n\nCopy this OTP and use it for verification.'

        # Send OTP to user email
        send_mail(
            'OTP Verification',
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        # print(otp)
        # request.session['otp'] = otp
        return Response({'success': True, 'otp': otp})
    else:
        return Response({'email not provided'})

    # return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def check_email(request):
    email = request.data.get('email')
    if email:
        if User.objects.filter(email=email).exists():
            return Response({"message": "Valid email"}, status=status.HTTP_200_OK)
        else:
            return Response({"message":"No user with this email exists!"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'message':'provide email id!'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def verify(request):


    if not request.data.get('username') or not request.data.get('email') or not request.data.get('password') or not request.data.get('password2'):
        return Response({'res':'All fields are required!'})

    elif User.objects.filter(username = request.data.get('username')).exists():
        return Response({'res':'username already taken!'})

    elif User.objects.filter(email = request.data.get('email')).exists():
        return Response({'res':'user with same email exists'})

    elif request.data.get('password') != request.data.get('password2'):
        return Response({'res':'passwd not same'})

    else:
        return Response({'res':'ok'})




@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user
    # Get the authenticated user's profile
    try:
        profile = UserProfile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

    # Check if username is already taken
    username = request.data.get('username', None)
    if username and User.objects.filter(username=username).exclude(pk=user.pk).exists():
        return Response({'message': 'Username already taken'}, status=status.HTTP_400_BAD_REQUEST)

    # Update the fields that were provided in the request
    if request.data.get("username"):
        user.username = request.data['username']
        profile.username = request.data["username"]
    if request.data.get("name"):
        profile.name = request.data["name"]
    if request.data.get("profilePic"):
        profile.profilePic = request.data["profilePic"]
    if request.data.get("bio"):
        profile.bio = request.data["bio"]

    # Save the changes
    user.save()
    profile.save()

    # Return the updated profile data
    return Response({"message": "Profile updated successfully", "data": {
        "username": profile.username,
        "name": profile.name,
        "profilePic": profile.profilePic.url if profile.profilePic else None,
        "bio": profile.bio
    }}, status=status.HTTP_200_OK)



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    current_password = request.data.get('current_password')
    new_password = request.data.get('new_password')
    confirm_new_password = request.data.get('confirm_new_password')

    # Verify current password
    if not user.check_password(current_password):
        return Response({'error': 'invalid current password'}, status=status.HTTP_400_BAD_REQUEST)

    # Verify new password and confirm new password match

    if current_password == new_password:
        return Response({'error': 'New password can not be the same as old one!'})

    if new_password != confirm_new_password:
        return Response({'error': 'New password and confirm new password do not match'}, status=status.HTTP_400_BAD_REQUEST)

    # Change password
    user.set_password(new_password)
    user.save()

    return Response({'message': 'Password changed successfully'})



@api_view(['POST'])
def reset_password(request):
    email = request.data.get('email')
    new_password = request.data.get('new_password')

    # Find the user associated with the provided email
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'error': 'User with the provided email does not exist.'}, status=404)

    if user.check_password(new_password):
        return Response({'error': 'New password cannot be the same as old one'}, status=status.HTTP_400_BAD_REQUEST)

    
    user.set_password(new_password)
    user.save()

    # message = f'Password for @{user.username} was changed successfully!',


    # Send OTP via email
    send_mail(
        'Reset Password Successful',
        f"password changed successfully for {user.username}",
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )
    return Response({'message': f'Password reset successfully. for {user.username}'})
