from django.urls import path
from . import views

urlpatterns = [
    path('tasks', views.task_list, name='task_list'),
    path('tasks/<int:task_id>', views.task_detail, name='task_detail'),
    path('tasks/update', views.update_task, name='update_task'),
    path('tasks/complete', views.complete_task, name='complete_task'),
]
