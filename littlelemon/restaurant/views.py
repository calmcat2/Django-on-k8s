from django.shortcuts import render
from rest_framework import generics,permissions
from rest_framework.exceptions import PermissionDenied
from .serializers import MenuSerializer,BookingSerializer
from . import models
from datetime import datetime,date
from .forms import BookingForm
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow authenticated users to view
        if request.method in permissions.SAFE_METHODS and request.user.is_authenticated:
            return True
        # Allow admin users full access
        return request.user and request.user.is_staff
    
# Create your views here.
def home(request):
    return render(request, 'index.html', {})

class MenuItemsView(generics.ListCreateAPIView):
    queryset = models.Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAdminOrReadOnly]

    def create(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied("Only admin users can create menu items.")
        return super().create(request, *args, **kwargs)

class SingleMenuItemView(generics.RetrieveUpdateAPIView,generics.DestroyAPIView):
    queryset=models.Menu.objects.all()
    serializer_class=MenuSerializer
    permission_classes = [IsAdminOrReadOnly]

    def update(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied("Only admin users can update menu items.")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied("Only admin users can delete menu items.")
        return super().destroy(request, *args, **kwargs)

class BookingView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated] 
    queryset=models.Booking.objects.all()
    def get_queryset(self):
        if self.request.user.username!='admin':
            print(self.request.user.username)
            return models.Booking.objects.filter(First_name__iexact=self.request.user.username)
        else:
            return models.Booking.objects.all()

    serializer_class = BookingSerializer

class SingleBookingView(generics.RetrieveUpdateAPIView,generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated] 
    queryset=models.Booking.objects.all()
    def get_queryset(self):
        if self.request.user.username!='admin':
            print(self.request.user.username)
            return models.Booking.objects.filter(First_name__iexact=self.request.user.username)
        else:
            return models.Booking.objects.all()

    serializer_class = BookingSerializer
    
def about(request):
    return render(request, 'about.html')

# def reservations(request):
#     date = request.GET.get('date',datetime.today().date())
#     bookings = models.Booking.objects.all()
#     booking_json = serializers.serialize('json', bookings)
#     return render(request, 'bookings.html',{"bookings":booking_json})

@csrf_exempt
def book(request):
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
@csrf_exempt
def bookings(request):
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

# Add your code here to create new views
def menu(request):
    menu_data = models.Menu.objects.all()
    main_data = {"menu": menu_data}
    return render(request, 'menu.html', {"menu": main_data})


def menu_item(request, pk=None): 
    if pk: 
        menu_item = models.Menu.objects.get(pk=pk) 
    else: 
        menu_item = "" 
    return render(request, 'menu_item.html', {"menu_item": menu_item}) 

