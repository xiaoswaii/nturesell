from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
import json
from itertools import chain
from users.models import User, Product, Message, Comment, UserProfile, ChatRoom, Message
from django.contrib.auth.models import User as AbstractUser
import hashlib
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    # search the related name
    if 'search' in request.POST:
        searchname = request.POST["searchname"]
        if searchname:
            searchuserresult = User.objects.filter(
                user__username__contains=searchname)
        return (request, 'chat.html', locals())

    # select a person to chat
    if 'talkto' in request.POST:
        sender = request.user.username
        receiver = request.POST['receiver']
        conversation1 = Message.objects.filter(
            sent_from__username=sender, sent_to__username=receiver)
        conversation2 = Message.objects.filter(
            sent_to__username=sender, sent_from__username=receiver)
        conversation = list(chain(conversation1, conversation2))
        conversation.sort(key=lambda x: x.date)
        user2 = AbstractUser.objects.get(username=receiver)
        if UserProfile.objects.filter(user_id=request.user.pk).exists():
            avatar = UserProfile.objects.get(user_id=request.user.pk)
        if UserProfile.objects.filter(user__username=receiver).exists():
            receive = UserProfile.objects.get(user__username=receiver)
        # find the chat room
        if ChatRoom.objects.filter(user1__username=sender, user2__username=receiver).exists():
            roomName = ChatRoom.objects.get(
                user1__username=sender, user2__username=receiver).room_name
        elif ChatRoom.objects.filter(user2__username=sender, user1__username=receiver).exists():
            roomName = ChatRoom.objects.get(
                user2__username=sender, user1__username=receiver).room_name
        else:
            roomName = hashlib.sha256((sender + receiver).encode()).hexdigest()
            ChatRoom.objects.create(
                user1=request.user, user2=user2, room_name=roomName)
        return redirect('/chat/' + roomName + '/', locals())
    searchuserresult = User.objects.all()
    return render(request, 'chat.html', locals())

@login_required
def room(request, room_name):
    chatroom = ChatRoom.objects.get(room_name=room_name)
    if request.user.username == chatroom.user1.username:
        sender = request.user
        receiver = chatroom.user2
    else:
        sender = request.user
        receiver = chatroom.user1

    conversation1 = Message.objects.filter(
        sent_from__username=sender, sent_to__username=receiver)
    conversation2 = Message.objects.filter(
        sent_to__username=sender, sent_from__username=receiver)
    conversation = list(chain(conversation1, conversation2))
    conversation.sort(key=lambda x: x.date)

    if 'talk' in request.POST:
        talk = request.POST['talk']
        if talk:
            Message.objects.create(sent_from=sender,
                                sent_to=receiver, msg=talk)
            conversation1 = Message.objects.filter(
                sent_from__username=sender, sent_to__username=receiver)
            conversation2 = Message.objects.filter(
                sent_to__username=sender, sent_from__username=receiver)
            conversation = list(chain(conversation1, conversation2))
            conversation.sort(key=lambda x: x.date)

    if UserProfile.objects.filter(user_id=request.user.pk).exists():
            avatar = UserProfile.objects.get(user_id=request.user.pk)
    if UserProfile.objects.filter(user__username=receiver).exists():
            receive = UserProfile.objects.get(user__username=receiver)
    return render(request, 'chat/chatroom.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'conversation': conversation,
        'receiver' : receiver,'receive' : receive , 'avatar' : avatar})
