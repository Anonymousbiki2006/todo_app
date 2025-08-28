from django.db import models
from django.contrib.auth.models import User
    
class TaskID(models.Model):

    task_id = models.CharField(max_length = 20 )

    def __str__(self) -> str:
        return self.task_id
    
class todo(models.Model):

    task_id = models.ForeignKey(TaskID, related_name = "taskid", on_delete = models.CASCADE, null = True)
    user = models.ForeignKey(User,null = True, blank = True, on_delete= models.CASCADE)
    todo_title = models.CharField(max_length= 50)
    todo_description = models.TextField(max_length = 100)
    todo_status = models.BooleanField(default = False)

    def __str__(self) -> str:
        return self.todo_title
    