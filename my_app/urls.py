from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
    path('admin/login/', views.login),
    path('admin/logout/', views.logout),
    path('admin/', admin.site.urls),
    
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('welcome', views.welcome, name='welcome'),
    path('welcome/first_connection', views.welcome, {'first_connection':True}, name='welcome_new'),
    path('results', views.results, name='results'),
    path('csv_results', views.csv_results, name='csv_results'),
    
    path('task1/<int:start>/', views.task1, name='task1'),
    
    path('task2/part1', views.task21, name='task21'),
    path('task2/part2/<int:id_question>', views.task22, name='task22'),
    path('task2/part2/<int:id_question>/<str:answer>', views.task22, name='task22_answer'),
    path('task2/part3', views.task23, name='task23'),
    path('task2/part4', views.task24, name='task24'),
    path('task2/part5', views.task25, name='task25'),
    
    path('task3/<int:start>/', views.task3, name='task3'),

    path('task4/part1', views.task21, {'AR':False}, name='task41'),
    path('task4/part2/<int:id_question>', views.task22, {'AR':False}, name='task42'),
    path('task4/part2/<int:id_question>/<str:answer>', views.task22, {'AR':False}, name='task42_answer'),
    path('task4/part3', views.task23, {'AR':False}, name='task43'),
    path('task4/part4', views.task24, {'AR':False}, name='task44'),
]
