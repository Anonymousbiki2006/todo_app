from django.urls import path
from .views import *

urlpatterns = [
     
    path('', home, name = "home"),
    path('addtask/', add_task, name = "add_task" ),
    path('task_detail/<id>/', task_detail, name = "task_detail"),
    path('login/', login_page, name = "login_page"),
    path('register/', register_page, name = "register_page"),
    path('logout/', logout_page, name = "logout_page"),
    path('update/<id>/', update_task, name = "update_task"),
    path('delete/<id>/', delete_task, name = "delete_task"), # type: ignore

]
