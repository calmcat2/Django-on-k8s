from django.shortcuts import render
from rest_framework import generics,permissions
from rest_framework.exceptions import PermissionDenied
from .serializers import MenuSerializer,BookingSerializer
from . import models
import datetime
from .forms import BookingForm
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse

# Home page view
def home(request):
    return render(request, 'index.html', {})
# About page view
def about(request):
    return render(request, 'about.html')
# Booking page view
@csrf_exempt
def book(request):
    form = BookingForm()
    today = datetime.date.today().strftime('%Y-%m-%d')
    context = {'form': form, 'today': today}
    return render(request, 'book.html', context)
# Menu page view
def menu(request):
    menu_data = models.Menu.objects.all()
    main_data = {"menu": menu_data}
    return render(request, 'menu.html', {"menu": main_data})
# Menu item page view
def menu_item(request, pk=None): 
    if pk: 
        menu_item = models.Menu.objects.get(pk=pk) 
    else: 
        menu_item = "" 
    return render(request, 'menu_item.html', {"menu_item": menu_item}) 

# Admin permission class
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow authenticated users to view
        if request.method in permissions.SAFE_METHODS and request.user.is_authenticated:
            return True
        # Allow admin users full access
        return request.user and request.user.is_staff
# Menu API view
class MenuItemsView(generics.ListCreateAPIView):
    queryset = models.Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAdminOrReadOnly]

    def create(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied("Only admin users can create menu items.")
        return super().create(request, *args, **kwargs)
# Single menu item API view
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
# Booking API view, allows list and create (admin only)
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
# Single booking API view, allows retrieve, update and delete (user only)
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
# Reservation check view serving as a POST endpoint for web form
@method_decorator(csrf_exempt, name='dispatch')
class ReservationCheckView(generics.ListCreateAPIView):
    queryset = models.Booking.objects.all().only('Reservation_date', 'Reservation_slot')
    serializer_class = BookingSerializer
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        data = json.load(request)
        exist = self.get_queryset().filter(Reservation_date=data['Reservation_date'],
            Reservation_slot=data['Reservation_slot']).exists()
        
        if exist:
             return JsonResponse({'success': False, 'error': 'Slot already reserved'})

        form = BookingForm(data)
        if form.is_valid():
            form.save()
            cleaned_data = form.cleaned_data
            cleaned_data['BookingDate'] = datetime.date.today().strftime('%Y-%m-%d')
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    def get(self, request):
        date= request.GET.get('date')
        if not date:
            date = datetime.date.today().strftime('%Y-%m-%d')

        bookings = self.get_queryset().filter(Reservation_date=date)
        booking_list = [
            {
                'Reservation_date': booking.Reservation_date.strftime('%Y-%m-%d'),
                'Reservation_slot': booking.Reservation_slot
            }
            for booking in bookings
        ]

        return JsonResponse(booking_list, safe=False)

