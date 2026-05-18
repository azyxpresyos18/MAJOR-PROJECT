from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Client, Department, Product, Location, Schedule
import json


# ─── AUTH ──────────────────────────────────────────────────────────────────

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email    = request.POST.get('email', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return redirect('home')
        messages.error(request, 'Invalid email or password.')
    return render(request, 'core/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# ─── MAIN PAGES ────────────────────────────────────────────────────────────

@login_required
def home(request):
    ctx = {
        'total_clients':   Client.objects.count(),
        'total_products':  Product.objects.count(),
        'total_schedules': Schedule.objects.count(),
        'pending':         Schedule.objects.filter(status='pending').count(),
        'ongoing':         Schedule.objects.filter(status='ongoing').count(),
        'completed':       Schedule.objects.filter(status='completed').count(),
    }
    return render(request, 'core/home.html', ctx)


@login_required
def clients(request):
    client_list = Client.objects.prefetch_related('products', 'schedules').all()
    return render(request, 'core/clients.html', {'clients': client_list})


@login_required
def products(request):
    client_id = request.GET.get('client')
    if client_id:
        product_list = Product.objects.filter(client_id=client_id).select_related('client')
    else:
        product_list = Product.objects.select_related('client').all()
    client_list = Client.objects.all()
    return render(request, 'core/products.html', {
        'products': product_list,
        'clients': client_list,
        'selected_client': int(client_id) if client_id else None,
    })


@login_required
def departmentalize(request):
    status_filter = request.GET.get('status', '')
    schedules = Schedule.objects.select_related(
        'client', 'product', 'department', 'location'
    )
    if status_filter:
        schedules = schedules.filter(status=status_filter)

    ctx = {
        'schedules':  schedules,
        'total':      Schedule.objects.count(),
        'ongoing':    Schedule.objects.filter(status='ongoing').count(),
        'completed':  Schedule.objects.filter(status='completed').count(),
        'pending':    Schedule.objects.filter(status='pending').count(),
        'confirmed':  Schedule.objects.filter(status='confirmed').count(),
        'status_filter': status_filter,
    }
    return render(request, 'core/departmentalize.html', ctx)


@login_required
def location(request):
    locations = Location.objects.all()
    return render(request, 'core/location.html', {'locations': locations})


@login_required
def schedule(request):
    schedules  = Schedule.objects.select_related('client', 'product', 'department', 'location').order_by('scheduled_date', 'scheduled_time')
    clients    = Client.objects.all()
    products   = Product.objects.select_related('client').all()
    departments = Department.objects.all()
    locations  = Location.objects.all()

    if request.method == 'POST':
        try:
            Schedule.objects.create(
                client_id     = request.POST['client'],
                product_id    = request.POST['product'],
                department_id = request.POST['department'],
                location_id   = request.POST['location'],
                scheduled_date= request.POST['date'],
                scheduled_time= request.POST['time'],
                quantity      = request.POST.get('quantity', 1),
                assigned_to   = request.POST.get('assigned_to', ''),
                notes         = request.POST.get('notes', ''),
                status        = 'pending',
                created_by    = request.user,
            )
            messages.success(request, 'Schedule created successfully!')
        except Exception as e:
            messages.error(request, f'Error creating schedule: {e}')
        return redirect('schedule')

    ctx = {
        'schedules':   schedules,
        'clients':     clients,
        'products':    products,
        'departments': departments,
        'locations':   locations,
    }
    return render(request, 'core/schedule.html', ctx)


@login_required
@require_POST
def update_schedule_status(request, pk):
    sched = get_object_or_404(Schedule, pk=pk)
    data  = json.loads(request.body)
    sched.status = data.get('status', sched.status)
    sched.save()
    return JsonResponse({'ok': True, 'status': sched.status})


@login_required
@require_POST
def delete_schedule(request, pk):
    sched = get_object_or_404(Schedule, pk=pk)
    sched.delete()
    return JsonResponse({'ok': True})
