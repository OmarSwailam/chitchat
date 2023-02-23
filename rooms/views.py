from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from .models import Room, RoomMessage
from .forms import RoomForm


@login_required(login_url='login')
def index(request):
    form = RoomForm()
    return render(request, "rooms/index.html", {
        'form': form
    })


def rooms(request, rooms_type):
    if rooms_type == "All":
        rooms = Room.objects.all()

    elif rooms_type == "Joined":
        rooms = request.user.rooms_joined.all()
        rooms = (rooms | request.user.rooms_created.all()).distinct()

    elif rooms_type == "Created":
        rooms = request.user.rooms_created.all()
    else:
        return JsonResponse({"error": "Invalid rooms."}, status=400)

    rooms = rooms.order_by("-created").all()
    return JsonResponse([room.serialize() for room in rooms], safe=False)


@login_required(login_url="login")
def create_room(request):
    if request.method == "POST":
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            room = form.save(commit=False)
            room.admin = request.user
            room.save()
            room.members.add(request.user)
            return redirect("index")
    if request.method == "GET":
        return redirect("index")


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = RoomMessage.objects.filter(
        room=room).order_by("created").all()
    if request.user in room.members.all() or request.user == room.admin:
        return render(request, 'rooms/room.html', {
            'room': room,
            'room_messages': room_messages
        })
    else:
        messages.error(request, 'You\'re not a member, you have to join first')
        return redirect('index')


@login_required(login_url='login')
def join_room(request, pk):
    room = Room.objects.get(id=pk)
    if request.user not in room.members.all() and request.user != room.admin:
        password = request.POST[f'password_{pk}']
        if password:
            if check_password(password, room.password):
                room.members.add(request.user)
                messages.success(request, 'Joined Successfully')
                return redirect('room', pk=pk)
            else:
                messages.error(request, 'Wrong password')
                return redirect('index')
        else:
            room.members.add(request.user)
            messages.success(request, 'Joined Successfully')
            return redirect('room', pk=pk)

    messages.info(request, 'Already a member')
    return redirect('room', pk=pk)
