import json
from django.core import serializers
from django.db import IntegrityError, transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils.dateparse import parse_date
from django.views.decorators.http import require_http_methods
from .forms import BookingForm
from .models import Booking, Menu

def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def reservations(request):
    data = serializers.serialize('json', Booking.objects.order_by('reservation_date', 'reservation_slot'))
    return render(request, 'bookings.html', {'booking_json': json.loads(data)})

def book(request):
    return render(request, 'book.html', {'form': BookingForm()})

def menu(request):
    return render(request, 'menu.html', {'menu': {'menu': Menu.objects.all()}})

def display_menu_item(request, pk):
    return render(request, 'menu_item.html', {'menu_item': get_object_or_404(Menu, pk=pk)})

@require_http_methods(['GET', 'POST'])
def bookings(request):
    status = 200
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            if not isinstance(data, dict):
                raise ValueError
        except (ValueError, UnicodeDecodeError):
            return JsonResponse({'error': 'A JSON object is required.'}, status=400)
        form = BookingForm(data)
        if not form.is_valid():
            return JsonResponse({'errors': form.errors}, status=400)
        if not 11 <= form.cleaned_data['reservation_slot'] <= 19:
            return JsonResponse({'error': 'Choose a slot from 11 through 19.'}, status=400)
        try:
            with transaction.atomic():
                form.save()
        except IntegrityError:
            return JsonResponse({'error': 'This date and time are already booked.'}, status=409)
        status = 201
        date = form.cleaned_data['reservation_date']
    else:
        value = request.GET.get('date')
        date = None
        if value:
            try:
                date = parse_date(value)
            except ValueError:
                date = None
            if date is None:
                return JsonResponse({'error': 'Use a valid YYYY-MM-DD date.'}, status=400)
    queryset = Booking.objects.order_by('reservation_date', 'reservation_slot')
    if date:
        queryset = queryset.filter(reservation_date=date)
    return HttpResponse(serializers.serialize('json', queryset), content_type='application/json', status=status)
