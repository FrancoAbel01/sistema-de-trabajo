from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, authenticate
from django.contrib import messages
from .models import Task, TaskAssignment
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import RegistroForm,TaskForm
from django.core.paginator import Paginator
from . import models
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Q
from datetime import datetime, timedelta
from xhtml2pdf import pisa
from django.http import HttpResponse,HttpResponseNotFound
from django.template.loader import get_template

from .forms import PersonalTaskForm
from .models import PersonalTask
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Task

def is_admin(user):
    return user.is_staff

@login_required
@user_passes_test(is_admin)
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    print(task)
    task.delete()
    messages.success(request, 'La tarea ha sido eliminada correctamente.')
    return redirect('task_list')

def inicio(request):
    return render(request, 'inicio.html')

@login_required
@user_passes_test(is_admin)
def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            return redirect('home')
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})


# Vista para crear tareas (solo para administradores)
@login_required
@user_passes_test(is_admin)
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            try:
                task = form.save(commit=False)
                task.created_by = request.user
                task.created_at = timezone.now()
                task.save()
                messages.success(request, 'Tarea creada exitosamente.')
                return redirect('task_list')
            except Exception as e:
                messages.error(request, f'Error al crear la tarea: {e}')
    else:
        form = TaskForm()
    return render(request, 'create_task.html', {'form': form})


    
# Vista para listar todas las tareas (visible para todos los usuarios)
@login_required
def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'task_list.html', {'tasks': tasks})



@login_required
def mis_task(request):
    # Obtener todas las tareas asignadas al usuario autenticado
    user_tasks = TaskAssignment.objects.filter(user=request.user)
    personal_tasks = PersonalTask.objects.filter(user=request.user)  # Obtener tareas personales del usuario autenticado
    return render(request, 'mis_task.html', {'tasks': user_tasks, 'personal_tasks': personal_tasks})




@login_required
def asignar_task(request):
    user_assigned_tasks = TaskAssignment.objects.filter(user=request.user).values_list('task_id', flat=True)
    tasks = Task.objects.exclude(id__in=user_assigned_tasks)
    return render(request, 'asignar_task.html', {'tasks': tasks})




# Vista para que los usuarios asignen tareas a sí mismos
@login_required
def assign_tasks(request):
    if request.method == 'POST':
        task_ids = request.POST.getlist('tasks')
        tareas_asignadas = []
        tareas_duplicadas = []
        
        for task_id in task_ids:
            task = Task.objects.get(id=task_id)
            if not TaskAssignment.objects.filter(user=request.user, task=task).exists():
                TaskAssignment.objects.create(user=request.user, task=task)
                tareas_asignadas.append(task.title)
            else:
                tareas_duplicadas.append(task.title)
        
        if tareas_asignadas:
            messages.success(request, f'Tareas asignadas exitosamente: {", ".join(tareas_asignadas)}.')
        if tareas_duplicadas:
            messages.warning(request, f'Ya tienes asignadas las siguientes tareas: {", ".join(tareas_duplicadas)}.')
        
        return redirect('home')
    
    return redirect('home')



@login_required
def home(request):
    usuario = request.user
    tareas_asignadas = TaskAssignment.objects.filter(user=usuario)
    tareas_personales = PersonalTask.objects.filter(user=usuario)  # Obtener tareas personales del usuario
    return render(request, 'home.html', {'usuario': usuario, 'tareas_asignadas': tareas_asignadas, 'tareas_personales': tareas_personales})



def signout(request):
    logout(request)
    return redirect('inicio')


from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import TaskAssignment

@login_required
def remove_task(request, id):
    task_assignment = get_object_or_404(TaskAssignment, id=id)
    # Verifica si el usuario es el creador o tiene permisos
    if task_assignment.user == request.user or request.user.is_staff:
        task_title = task_assignment.task.title
        task_assignment.delete()
        messages.success(request, f'Tarea "{task_title}" eliminada exitosamente.')
    else:
        messages.error(request, 'No tienes permiso para eliminar esta tarea.')

    return redirect('mis_task')



# listar usuarios
@login_required
@user_passes_test(is_admin)
def user_list_view(request):
    users = User.objects.all()
    paginator = Paginator(users, 5)  # 10 usuarios por página

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'user_list.html', {'page_obj': page_obj})






@login_required
@user_passes_test(is_admin)
def delete_user(request, user_id):
    if request.user.is_staff:  # Verifica que el usuario sea admin
        user = get_object_or_404(User, id=user_id)
        user.delete()
        messages.success(request, 'Usuario eliminado correctamente.')
    else:
        messages.error(request, 'No tienes permiso para eliminar usuarios.')
    return redirect('user_list')





@login_required
@user_passes_test(is_admin)
def user_profile(request, user_id):
    # Obtener el usuario dado el user_id
    user = get_object_or_404(User, id=user_id)
    # Obtener las tareas asignadas al usuario
    assigned_tasks = TaskAssignment.objects.filter(user=user)
    return render(request, 'profile.html', {'user': user, 'assigned_tasks': assigned_tasks})



from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

@login_required
def export_pdf(request, user_id):
    user = get_object_or_404(User, id=user_id)
    assigned_tasks = TaskAssignment.objects.filter(user=user)

    total_duration = timedelta()  # Asegurarse de importar timedelta desde datetime
    for task_assignment in assigned_tasks:
        start_time = datetime.combine(task_assignment.task.execution_date, task_assignment.task.start_time)
        end_time = datetime.combine(task_assignment.task.execution_date, task_assignment.task.end_time)
        duration = end_time - start_time
        total_duration += duration

    total_hours = total_duration.total_seconds() / 3600  # Convertir la duración total a horas

    template_path = 'profile_pdf.html'
    context = {'user': user, 'assigned_tasks': assigned_tasks, 'total_hours': total_hours}

    # Crear el PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="perfil_{user.username}.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Hubo un error al generar el PDF <pre>' + html + '</pre>')
    return response



def user_actual(request):
    usuario = request.user
    assigned_tasks = TaskAssignment.objects.filter(user=usuario)
    return render(request, 'user_actual.html', {'user': usuario, 'assigned_tasks': assigned_tasks}) 


def page_not_found(request, exception=None):
    if not request.user.is_authenticated:
        return redirect('login')
    return HttpResponseNotFound('<h1>Page not found</h1>')



@login_required
def create_personal_task(request):
    if request.method == 'POST':
        form = PersonalTaskForm(request.POST)
        if form.is_valid():
            personal_task = form.save(commit=False)
            personal_task.user = request.user
            personal_task.save()
            return redirect('mis_task')  # Asegúrate de tener esta URL configurada
    else:
        form = PersonalTaskForm()
    return render(request, 'create_Mytask.html', {'form': form})


@login_required
def delete_task_personal(request, task_id):
    task = get_object_or_404(PersonalTask, id=task_id)
    task.delete()
    messages.success(request, 'Usuario eliminado correctamente.')
    return redirect('mis_task')







from .models import Task
from .forms import TaskForm

@login_required
def edit_task(request, id):
    task = get_object_or_404(Task, id=id)
    
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, f'Tarea "{task.title}" actualizada exitosamente.')
            return redirect('mis_task')
    else:
        form = TaskForm(instance=task)
    
    return render(request, 'editar_task.html', {'form': form, 'task': task})







@login_required
def edit_tarea_personal(request, id):
    tarea = get_object_or_404(PersonalTask, id=id, user=request.user)
    
    if request.method == "POST":
        form = PersonalTaskForm(request.POST, instance=tarea)
        if form.is_valid():
            form.save()
            messages.success(request, f'Tarea "{tarea.title}" actualizada exitosamente.')
            return redirect('mis_task')
    else:
        form = PersonalTaskForm(instance=tarea)
    
    return render(request, 'editar_task_personal.html', {'form': form, 'tarea': tarea})






@login_required
def profile(request):
    usuario = request.user
    assigned_tasks = TaskAssignment.objects.filter(user=usuario)
    personal_tasks = PersonalTask.objects.filter(user=usuario)
    return render(request, 'user.html', {'usuario': usuario, 'assigned_tasks': assigned_tasks, 'personal_tasks': personal_tasks})
