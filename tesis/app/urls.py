from django.urls import path, re_path
from . import views
from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView
from .views import delete_task
from django.http import HttpResponsePermanentRedirect

def redirect_to_http(request):
    return HttpResponsePermanentRedirect('http://' + request.get_host() + request.path)



urlpatterns = [
	path('delete_task/<int:task_id>/', delete_task, name='delete_task'),
	path('delete_task_personal/<int:task_id>/', views.delete_task_personal, name='delete_task_personal'),
	path('',views.inicio, name = 'inicio'),
	path('registro/', views.registro, name='registro'),
	path('home/', views.home, name='home'),
	path('login/', LoginView.as_view(template_name='login.html'), name='login'),
	path('logout/', views.signout, name='logout'),
	# path('create-task/', views.create_task, name='create_task'),
    # path('tasks/', views.task_list, name='task_list'),
	path('create-task/', views.create_task, name='create_task'),
    path('tasks/', views.task_list, name='task_list'),
    path('mis-tasks/', views.mis_task, name='mis_task'),
    path('assign-tasks/', views.assign_tasks, name='assign_tasks'),
    path('asignar_task/', views.asignar_task, name='asignar_task'),
	path('remove_task/<int:id>/', views.remove_task, name='remove_task'),
	path('user_list/', views.user_list_view, name='user_list'),
	path('user_delete/<int:user_id>/', views.delete_user, name='delete_user'),
	path('profile/<int:user_id>/', views.user_profile, name='user_profile'),
	path('user-actual/', views.user_actual, name='user_actual'),
    path('export_pdf/<int:user_id>/', views.export_pdf, name='export_pdf'),
    path('secure/', redirect_to_http),
    path('create_Mytask/', views.create_personal_task, name='create_Mytask'),
    path('edit_task/<int:id>/', views.edit_task, name='edit_task'),
    path('edit_tarea_personal/<int:id>/', views.edit_tarea_personal, name='edit_tarea_personal'),
    path('user/', views.profile, name='user'),
    
    re_path(r'^.*$', views.page_not_found, name='page_not_found'),
] 




