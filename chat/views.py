from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
import json
from itertools import chain
from users.models import User, Product, Message, Comment, UserProfile, ChatRoom
from django.contrib.auth.models import User as AbstractUser
import hashlib

def index(request):
    if 'search' in request.POST:
        searchname = request.POST["searchname"]
        if searchname:
            searchuserresult = User.objects.filter(
                user__username__contains=searchname)
            return render(request, 'chat.html', locals())
        else:
            return render(request, 'chat.html', locals())

    if 'talkto' in request.POST:
        sender = request.user.username
        receiver = request.POST['receiver']
        conversation1 = Message.objects.filter(
            sent_from__username=sender, sent_to__username=receiver)
        conversation2 = Message.objects.filter(
            sent_to__username=sender, sent_from__username=receiver)
        conversation = list(chain(conversation1, conversation2))
        conversation.sort(key=lambda x: x.date)
        if UserProfile.objects.filter(user_id=request.user.pk).exists():
            avatar = UserProfile.objects.get(user_id=request.user.pk)

        user2 = AbstractUser.objects.get(username=receiver)
        
        ## find the chat room
        roomName = ""
        if ChatRoom.objects.filter(user1__username=sender, user2__username=receiver).exists():
            roomName = ChatRoom.objects.get(user1__username=sender, user2__username=receiver).room_name
        elif ChatRoom.objects.filter(user1__username=sender, user2__username=receiver).exists():
            roomName = ChatRoom.objects.get(user1__username=sender, user2__username=receiver).room_name
        else:
            roomName = hashlib.sha256((sender + receiver).encode()).hexdigest()
            ChatRoom.objects.create(user1=request.user, user2=user2, room_name=roomName)
        return redirect('/chat/' + roomName + '/', locals())
    
    if 'talking' in request.POST:
        sender=request.user.username
        sent_from=AbstractUser.objects.get(username=request.user.username)
        sent_too=request.POST['receiver']
        receiver=sent_too
        sent_to=AbstractUser.objects.get(username=sent_too)
        talk=request.POST['talk']
        if talk:
            Message.objects.create(sent_from=sent_from,
                                   sent_to=sent_to, msg=talk)
            conversation1=Message.objects.filter(
                sent_from__username=sender, sent_to__username=sent_too)
            conversation2=Message.objects.filter(
                sent_to__username=sender, sent_from__username=sent_too)
            conversation=list(chain(conversation1, conversation2))
            conversation.sort(key=lambda x: x.date)
            return render(request, 'chatroom.html', locals())
        else:
            conversation1=Message.objects.filter(
                sent_from__username=sender, sent_to__username=receiver)
            conversation2=Message.objects.filter(
                sent_to__username=sender, sent_from__username=receiver)
            conversation=list(chain(conversation1, conversation2))
            conversation.sort(key=lambda x: x.date)
            return render(request, 'chatroom.html', locals())
    searchuserresult=User.objects.all()
    return render(request, 'chat.html', locals())

def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })
