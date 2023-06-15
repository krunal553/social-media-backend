from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from user.models import UserProfile
from user.serializers import UserProfileSerializerWithLessDetails
from .serializers import MessageSerializer, ThreadSerializer, ThreadSerializerForChatList
from .models import UserMessage, Thread
from django.db.models import Q
from django.contrib.auth.models import User



@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_messages(request):
    user = request.user.userprofile
    threads = Thread.objects.filter(Q(users=user), is_group_chat=False)
    serializer = ThreadSerializer(threads, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def create_thread(request):
    user = request.user.userprofile
    recipient_id = request.data.get('recipient_id')
    is_group_chat = request.data.get('is_group_chat', False)
    if recipient_id is not None:
        try:
            recipient = UserProfile.objects.get(id=recipient_id)
            if is_group_chat:
                thread = Thread.objects.create(is_group_chat=True)
                thread.users.add(user, recipient)
            else:
                thread, created = Thread.objects.get_or_create(is_group_chat=False)
                thread.users.add(user, recipient)
            serializer = ThreadSerializer(thread, many=False)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response({'detail': 'User with that id does not exist'})
    else:
        return Response({'detail': 'Recipient id not found'})


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def create_message(request):
    sender = request.user.userprofile
    data = request.data
    thread_id = data.get('thread_id')
    if thread_id:
        message = data.get('message')
        thread = Thread.objects.get(id=thread_id)
        if thread:
            if message is not None:
                message = UserMessage.objects.create(thread=thread, sender=sender, body=message)
                message.save()
                serializer = ThreadSerializer(thread, many=False)
                return Response(serializer.data)
            else:
                return Response({'detail': 'Content for message required'})
        else:
            return Response({'detail': 'Thread not found'})
    else:
        return Response({'detail': 'Please provide thread id'})


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def read_message(request):
    thread_id = request.GET.get('thread_id')
    thread = Thread.objects.get(id=thread_id)
    messages = thread.messages.all()
    un_read = thread.messages.filter(is_seen=False)
    for msg in un_read:
        msg.is_read = True
        msg.save()
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_groups(request):
    user = request.user.userprofile
    groups = Thread.objects.filter(sender=user, is_group_chat=True)
    serializer = ThreadSerializer(groups, many=True)
    return Response(serializer.data)




# =================================================================

@api_view(['GET'])
def get_messages(request):
    # Get the current user
    user = request.user
    user_prof = UserProfile.objects.get(user=request.user)

    # Get the other user ID from the request parameters
    other_user_name = request.GET.get('user_name')

    if not other_user_name:
        return Response({'error': 'Please provide the other user ID.'}, status=status.HTTP_400_BAD_REQUEST)

    # Find the other user by ID
    other_user_prof = get_object_or_404(UserProfile, username=other_user_name)

    # Check if a thread already exists between the two users
    thread = Thread.objects.filter(users=user_prof).filter(users=other_user_prof).filter(is_one_to_one=True).first()

    if not thread:
        return Response({'error': 'No messages found between the two users.'}, status=status.HTTP_404_NOT_FOUND)

    # Get all messages from the thread
    messages = UserMessage.objects.filter(thread=thread)

    # Serialize the messages and return the response
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_new_message(request, thread_id):
    # Get the current user
    user = request.user
    user_prof = UserProfile.objects.get(user = request.user)

    # Find the thread by ID
    thread = get_object_or_404(Thread, thread_id=thread_id)

    # Check if the current user is a participant in the thread
    if not thread.users.filter(id=user_prof.id).exists():
        return Response({'error': 'You are not a participant in this thread.'}, status=status.HTTP_403_FORBIDDEN)

    # Create a new message with the current user as the sender
    message = UserMessage.objects.create(
        thread=thread,
        sender=user_prof,
        body=request.data.get('body')
    )

    serializer = MessageSerializer(message)
    return Response(serializer.data, status=status.HTTP_201_CREATED)



@api_view(['POST'])
def create_or_get_thread(request):
    # Get the current user
    user = request.user.userprofile

    # Get the user from the POST data
    # other_user_id = request.data.get('user_id')
    # other_user_id = request.GET.get('user_id')
    other_usr = User.objects.get(username= request.GET.get('user_name'))

    if not other_usr:
        return Response({'error': 'Please provide the other user ID.'}, status=status.HTTP_400_BAD_REQUEST)

    # Find the other user by ID
    # other_user = get_object_or_404(UserProfile, id=other_user_id)
    # other_user = UserProfile.objects.get(id=other_user_id)
    other_user = UserProfile.objects.get(user=other_usr)

    # Check if a thread already exists between the two users
    thread = Thread.objects.filter(users=user).filter(users=other_user).filter(is_one_to_one=True).first()

    # If a thread already exists, return it
    if thread:
        serializer = ThreadSerializer(thread)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # If a thread doesn't exist, create a new one
    else:
        thread = Thread.objects.create(is_one_to_one=True)
        thread.users.add(user)
        thread.users.add(other_user)
        serializer = ThreadSerializer(thread)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_chat_list(request):
    user = request.user.userprofile
    threads = Thread.objects.filter(users=user)
    # serializer = ThreadSerializer(threads, many=True)
    serializer = ThreadSerializerForChatList(threads, many=True, context={'request': request})
    # print(serializer.data['users'])
    return Response(serializer.data, status=status.HTTP_200_OK)
