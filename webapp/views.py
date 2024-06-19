from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Record
from .forms import CreateUserForm, LoginForm, CreateRecordForm, UpdateRecordForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.db.models import Q  # Import Q to use OR conditions in filtering
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string

# Homepage
def home(request):
    return render(request, 'webapp/index.html')

# Register a user
def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully!")
            return redirect("my-login")
    context = {'form': form}
    return render(request, 'webapp/register.html', context=context)

# Login a user
def my_login(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect("dashboard")
    context = {'form': form}
    return render(request, 'webapp/my-login.html', context=context)

# Dashboard with search functionality
@login_required(login_url='my-login')
def dashboard(request):
    query = request.GET.get('search')
    if query:
        records_list = Record.objects.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains(query)
        ))
    else:
        records_list = Record.objects.all()

    paginator = Paginator(records_list, 5)  # Show 5 records per page
    page_number = request.GET.get('page')
    records = paginator.get_page(page_number)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {
            'records_html': render_to_string('webapp/partials/records_list.html', {'records': records}),
            'pagination_html': render_to_string('webapp/partials/pagination.html', {'records': records})
        }
        return JsonResponse(data)

    context = {'records': records, 'query': query}
    return render(request, 'webapp/dashboard.html', context=context)

# Create a record
@login_required(login_url='my-login')
def create_record(request):
    form = CreateRecordForm()
    if request.method == "POST":
        form = CreateRecordForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your record was created!")
            return redirect("dashboard")
    context = {'form': form}
    return render(request, 'webapp/create-record.html', context=context)

# Update a record
@login_required(login_url='my-login')
def update_record(request, pk):
    record = Record.objects.get(id=pk)
    form = UpdateRecordForm(instance=record)
    if request.method == 'POST':
        form = UpdateRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, "Your record was updated!")
            return redirect("dashboard")
    context = {'form': form}
    return render(request, 'webapp/update-record.html', context=context)

# View a singular record
@login_required(login_url='my-login')
def singular_record(request, pk):
    record = Record.objects.get(id=pk)
    context = {'record': record}
    return render(request, 'webapp/view-record.html', context=context)

# Delete a record
@login_required(login_url='my-login')
def delete_record(request, pk):
    record = Record.objects.get(id=pk)
    record.delete()
    messages.success(request, "Your record was deleted!")
    return redirect("dashboard")

# User logout
def user_logout(request):
    auth.logout(request)
    messages.success(request, "Logout success!")
    return redirect("my-login")

# Search records
@login_required(login_url='my-login')
def search_records(request):
    query = request.GET.get('q')
    if query:
        records_list = Record.objects.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query)
        )
    else:
        records_list = Record.objects.none()

    paginator = Paginator(records_list, 5)  # Show 5 records per page
    page_number = request.GET.get('page')
    records = paginator.get_page(page_number)

    context = {'records': records, 'query': query}
    return render(request, 'webapp/search-records.html', context=context)
