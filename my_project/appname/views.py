from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Task, Comment
from django.contrib.auth import get_user_model
from django.http import HttpResponseForbidden, HttpResponseNotAllowed
from .forms import UserRegisterForm, TaskForm
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST

User = get_user_model()

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required
def task_list(request):
    tasks = Task.objects.filter(created_by=request.user)
    
    
    status_filter = request.GET.get('status', 'all')
    priority_filter = request.GET.get('priority', 'all')
    due_date_filter = request.GET.get('due_date', '')

    if status_filter != 'all':
        tasks = tasks.filter(status=status_filter)
    if priority_filter != 'all':
        tasks = tasks.filter(priority=priority_filter)
    if due_date_filter:
        tasks = tasks.filter(due_date=due_date_filter)

    form = TaskForm()  

    return render(request, 'task_list.html', {
        'tasks': tasks,
        'status_filter': status_filter,
        'priority_filter': priority_filter,
        'due_date_filter': due_date_filter,
        'form': form
    })

@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            return redirect('task_list')
    return redirect('task_list')

@require_POST
@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, created_by=request.user)
    task.delete()
    return redirect('task_list')

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, created_by=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'edit_task.html', {'form': form, 'task': task})