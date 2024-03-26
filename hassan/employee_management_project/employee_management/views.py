# employee_management/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.utils import timezone
from .models import Employee, AttendanceRecord  # Assuming AttendanceRecord model is defined in models.py
from .forms import CustomUserCreationForm, LoginForm
from datetime import datetime  # Import datetime for date parsing
from .forms import EmployeeRegistrationForm

@login_required
def home(request):
    employee = Employee.objects.get(user=request.user)
    context = {
        'employee': employee
    }
    return render(request, 'home.html', context)

@login_required
def check_in(request):
    if request.method == 'POST':
        current_user = request.user
        try:
            employee = Employee.objects.get(user=current_user)
            record = AttendanceRecord.objects.create(employee=employee, date=timezone.now().date(), check_in=timezone.now().time())
            return redirect('home')
        except Employee.DoesNotExist:
            return HttpResponse("Employee record not found", status=404)
    else:
        return HttpResponse("Method not allowed", status=405)

@login_required
def check_out(request):
    if request.method == 'POST':
        current_user = request.user
        try:
            employee = Employee.objects.get(user=current_user)
            latest_record = AttendanceRecord.objects.filter(employee=employee).latest('date')
            latest_record.check_out = timezone.now().time()
            latest_record.save()
            return redirect('home')
        except (Employee.DoesNotExist, AttendanceRecord.DoesNotExist) as e:
            return HttpResponse("Error: {}".format(e), status=404)
    else:
        return HttpResponse("Method not allowed", status=405)

@login_required
def mark_off_day(request):
    if request.method == 'POST':
        off_day_str = request.POST.get('off_day')
        try:
            off_day = datetime.strptime(off_day_str, '%Y-%m-%d').date()
            current_user = request.user
            employee = Employee.objects.get(user=current_user)
            if not AttendanceRecord.objects.filter(employee=employee, date=off_day).exists():
                record = AttendanceRecord.objects.create(employee=employee, date=off_day)
                return redirect('home')
            else:
                return HttpResponse("Off day already marked", status=400)
        except (Employee.DoesNotExist, ValueError) as e:
            return HttpResponse("Error: {}".format(e), status=404)
    else:
        return HttpResponse("Method not allowed", status=405)

@login_required
def update_info(request):
    if request.method == 'POST':
        return redirect('home')
    else:
        return HttpResponse("Method not allowed", status=405)

def register_employee(request):
    if request.method == 'POST':
        form = EmployeeRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = EmployeeRegistrationForm()
    return render(request, 'register_employee.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return HttpResponse("Invalid login credentials", status=401)
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def custom_logout(request):
    logout(request)
    return redirect('home')
