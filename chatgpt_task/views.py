from django.shortcuts import render

# Create your views here.
from .models import Task
from chatgpt_user.models import FrontUserBase

def dashboard(request):
    user_count = FrontUserBase.objects.count()
    task_count = Task.objects.count()

    context = { 'user_count': user_count, 'task_count': task_count }
    return render(request, 'dashboard.html',context)