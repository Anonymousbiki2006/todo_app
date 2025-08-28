from django.shortcuts import render,redirect, HttpResponse, get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login,authenticate, logout

@login_required(login_url = "/todo/login/")
def home(request):

    queryset = todo.objects.filter(user = request.user)

    return render(request, "index.html", {"queryset" : queryset })

@login_required(login_url = "/todo/login/")
def add_task(request):

    if request.method == "POST":

        task_id_g = request.POST.get("todo_id")
        todo_title = request.POST.get("todo_title")
        todo_description = request.POST.get("todo_description")
        todo_status = request.POST.get("todo_status") == "on"

        task_id_obj, created = TaskID.objects.get_or_create(task_id = task_id_g)

        todo.objects.create(

            task_id = task_id_obj,
            user = request.user,
            todo_title = todo_title,
            todo_description = todo_description,
            todo_status = todo_status,

        )

        return redirect("/todo/")
    
    return render(request, "add_todo.html")

@login_required(login_url = "/todo/login/")
def task_detail(request, id):

    # we can do by using queryset but since we are trying to fetch only one item which is unique so iterating in the html file
    # is unnecessary
    # queryset = todo.objects.filter( task_id__task_id = id)

    context = get_object_or_404(todo, task_id__task_id = id )

    if request.method == 'POST':
        status = request.POST.get("todo_status") == "on"
        context.todo_status = status
        context.save()
        return redirect("task_detail", id = id) 

    return render(request, "task_detail.html", {"context" : context})

@login_required(login_url = "/todo/login/")
def update_task(request, id):

    todo_obj = get_object_or_404(todo, task_id__task_id = id)

    if request.method == "POST":

        todo_title = request.POST.get('todo_title')
        todo_description = request.POST.get('todo_description')

        todo_obj.todo_title = todo_title
        todo_obj.todo_description = todo_description

        todo_obj.save()

        return redirect("/todo/")

    return render(request, "task_update.html")

def delete_task(request, id):

    todo_obj = get_object_or_404(todo, task_id__task_id = id, user = request.user)

    if request.method == "POST" and todo_obj.task_id :
        todo_obj.task_id.delete() # type: ignore
    
    return redirect("home")


def login_page(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username = username).exists():
            messages.error(request, "Username doesn't exist")
        
        user = authenticate(username = username, password = password)

        if user is None:
            messages.error(request, "Incorrect password")
            return redirect("/todo/login/")
        
        else:
            login(request, user)
            return redirect('/todo/')
        
    return render(request, "login.html")

def register_page(request):

    if request.method == 'POST':

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email_id = request.POST.get('email_id')
        password = request.POST.get('password')

        if User.objects.filter(username = username).exists():
            messages.error(request,"Username exists")
            return redirect("/todo/register/")
        
        user = User.objects.create(
            
            first_name = first_name,
            last_name = last_name,
            username = username,
            email = email_id,

        )
        user.set_password(password)
        
        user.save()

        messages.success(request, "User created successfully")
        return redirect("/todo/login/")
    
    return render(request, "register.html")

@login_required
def logout_page(request):
    logout(request)
    return redirect('/todo/')