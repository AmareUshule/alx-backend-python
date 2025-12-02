from django.shortcuts import render

# Create your views here.from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

@login_required
def delete_user(request):
    user = request.user
    if request.method == "POST":
        username = user.username
        user.delete()  # Triggers post_delete signal
        messages.success(request, f"User {username} and all related data deleted successfully.")
        return redirect('home')  # Replace 'home' with your homepage URL name
    return render(request, 'messaging/delete_user_confirm.html')
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Message

@login_required
def inbox(request):
    """
    Display top-level messages received by the logged-in user with threaded replies.
    Uses select_related and prefetch_related for optimal queries.
    """
    # Top-level messages for this user (no parent)
    messages = (
        Message.objects.filter(receiver=request.user, parent_message__isnull=True)
        .select_related('sender', 'receiver')  # Fetch sender and receiver in one query
        .prefetch_related(
            'replies__sender',  # Fetch replies and their senders
            'replies__receiver',  # Fetch replies and their receivers
            'replies__replies'  # Prefetch nested replies (recursive)
        )
        .order_by('-timestamp')
    )

    # Build a threaded structure
    threads = [msg.get_thread() for msg in messages]

    return render(request, 'messaging/inbox.html', {'threads': threads})

