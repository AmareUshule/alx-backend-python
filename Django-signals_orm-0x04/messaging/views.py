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

