from django.shortcuts import render
from rest_framework import generics,permissions
from rest_framework.exceptions import PermissionDenied
from .serializers import MenuSerializer,BookingSerializer
from . import models
from datetime import datetime,date
from .forms import BookingForm
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse,HttpResponse
from .metrics import increment_request_count
from .metrics import request_count,increment_request_count,error_count,MetricsMixin
from prometheus_client import generate_latest


# Endpoint for metrics scrape '/metrics'
def metrics_view(request):
    return HttpResponse(generate_latest(), content_type='text/plain')

# The Home webpage '/'
def home(request):
    increment_request_count('GET','/')
    return render(request, 'index.html', {})

# The About webpage '/about'
def about(request):
    increment_request_count('GET','/about/')
    return render(request, 'about.html')

# The Book webpage '/book'
@csrf_exempt
def book(request):
    increment_request_count('POST','/book/')
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
                form.save()
                cleaned_data = form.cleaned_data
                cleaned_data['BookingDate'] = datetime.date.today().strftime('%Y-%m-%d')
                print(cleaned_data)
                return render(request,'book_successful.html',{'form':cleaned_data})
        else:
            return JsonResponse(form.errors)
    today = date.today().strftime('%Y-%m-%d')
    context = {'form': form, 'today': today}
    return render(request, 'book.html', context)

# The Menu webpage '/menu'
def menu(request):
    increment_request_count('GET','/menu/')
    menu_data = models.Menu.objects.all()
    main_data = {"menu": menu_data}
    return render(request, 'menu.html', {"menu": main_data})

# The Menu Item webpage '/menu-items/<int:pk>'
def menu_item(request, pk=None): 
    if pk: 
        menu_item = models.Menu.objects.get(pk=pk) 
        increment_request_count('GET',f'/menu-items/{pk}/')
    else: 
        menu_item = "" 
    return render(request, 'menu_item.html', {"menu_item": menu_item}) 

# The bookings webpage '/bookings'
@csrf_exempt
def bookings(request):
    increment_request_count('GET','/bookings/')
    if request.method == 'POST':
        data = json.load(request)
        exist = models.Booking.objects.filter(Reservation_date=data['Reservation_date']).filter(
            Reservation_slot=data['Reservation_slot']).exists()
        if exist==False:
            booking = models.Booking(
                First_name=data['First_name'],
                Reservation_date=data['Reservation_date'],
                Reservation_slot=data['Reservation_slot'],
                No_of_guests=data['No_of_guests'],
                BookingDate=datetime.today().strftime('%Y-%m-%d'),
                Phone=data['Phone']
            )
            booking.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})
    #If the 'date' parameter is not provided, it will default to the current date.
    date= request.GET.get('date')
    if not date:
        date=datetime.today().strftime('%Y-%m-%d')

    bookings = models.Booking.objects.all().filter(Reservation_date=date)
    booking_list = [
        {
            'Reservation_date': booking.Reservation_date.strftime('%Y-%m-%d'),
            'Reservation_slot': booking.Reservation_slot
        }
        for booking in bookings
    ]

    return JsonResponse(booking_list, safe=False)

# custome class to allow authenticated user to view and admin to full access
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow authenticated users to view
        if request.method in permissions.SAFE_METHODS and request.user.is_authenticated:
            return True
        # Allow admin users full access
        return request.user and request.user.is_staff

# API endpoint 'api/menu/' to list and create menu items by staff
class MenuItemsView(MetricsMixin, generics.ListCreateAPIView):
    queryset = models.Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAdminOrReadOnly]

# API endpoint 'api/menu-items/<int:pk>' to view, update and delete menu items by staff
class SingleMenuItemView(MetricsMixin,generics.RetrieveUpdateAPIView,generics.DestroyAPIView):
    queryset=models.Menu.objects.all()
    serializer_class=MenuSerializer
    permission_classes = [IsAdminOrReadOnly]

# API endpoint 'api/reservations/' to list and create bookings by authenticated users. Admin can view all bookings.
class BookingView(MetricsMixin,generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated] 
    queryset=models.Booking.objects.all()
    def get_queryset(self):
        if self.request.user.username!='admin':
            print(self.request.user.username)
            return models.Booking.objects.filter(First_name__iexact=self.request.user.username)
        else:
            return models.Booking.objects.all()

    serializer_class = BookingSerializer

# API endpoint 'api/reservations/<int:pk>' to view, update and delete bookings by authenticated users. Admin can view/edit/delete all bookings.
class SingleBookingView(MetricsMixin,generics.RetrieveUpdateAPIView,generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated] 
    queryset=models.Booking.objects.all()
    def get_queryset(self):
        if self.request.user.username!='admin':
            print(self.request.user.username)
            return models.Booking.objects.filter(First_name__iexact=self.request.user.username)
        else:
            return models.Booking.objects.all()

    serializer_class = BookingSerializer



