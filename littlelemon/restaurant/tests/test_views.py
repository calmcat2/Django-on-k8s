from django.test import TestCase
from restaurant.views import MenuItemsView
from restaurant.models import Menu,Booking
from django.test import Client
from ..serializers import MenuSerializer,BookingSerializer
from django.contrib.auth.models import User
import json, datetime

class MenuViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        Menu.objects.create(MenuID=5,Title="Banana",Price=1,Inventory=1000).save()
        Menu.objects.create(MenuID=4,Title="Drunken Noodles",Price=10,Inventory=1).save()
        
    def test_getmenu(self):
        self.client.force_login(self.user)
        response=self.client.get(path='/api/menu')
        self.assertEqual(response.status_code,200)
        serialized_data=MenuSerializer(Menu.objects.all(),many=True).data  
        self.assertEqual(response.data,serialized_data)

class MenusingleViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        Menu.objects.create(MenuID=5,Title="Banana",Price=1,Inventory=1000).save()
        Menu.objects.create(MenuID=4,Title="Drunken Noodles",Price=10,Inventory=1).save()
        
    def test_getExistingMenuItem(self):
        self.client.force_login(self.user)
        response=self.client.get(path='/api/menu-items/1')
        self.assertEqual(response.status_code,200)
        serialized_data=MenuSerializer(Menu.objects.get(pk=1)).data  
        self.assertEqual(response.data,serialized_data) 
    
    def test_getNonExistingMenuItem(self):
        self.client.force_login(self.user)
        response=self.client.get(path='/api/menu-items/10')
        self.assertEqual(response.status_code,404)

class BookingViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='John', password='testpassword')
        Booking.objects.create(Phone="111-111-1111",First_name="John",Reservation_date="2025-12-14",Reservation_slot=12,No_of_guests=2).save()
    
    def test_getbooking(self):
        self.client.force_login(self.user)
        response=self.client.get(path='/api/reservations')
        self.assertEqual(response.status_code,200)
        serialized_data=BookingSerializer(Booking.objects.filter(First_name__iexact=self.user.username),many=True).data  
        self.assertEqual(response.data,serialized_data)

class SingleBookingViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='John', password='testpassword')
        self.booking = Booking.objects.create(Phone="111-111-1111",First_name="John",Reservation_date="2025-12-24",Reservation_slot=10,No_of_guests=2)
        self.booking.save()
    
    def test_getselfbooking(self):
        self.client.force_login(self.user)
        response=self.client.get(path=f'/api/reservations/{self.booking.id}')
        self.assertEqual(response.status_code,200)
        serialized_data=BookingSerializer(self.booking).data  
        self.assertEqual(response.data,serialized_data)

class ReservationCheckViewTestSameDay(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='John', password='testpassword')
        self.today = datetime.date.today().strftime('%Y-%m-%d')
        self.booking = Booking.objects.create(Phone="111-111-1111",First_name="John",Reservation_date=self.today,Reservation_slot=10,No_of_guests=2)
        self.booking.save()
    
    def test_getslotsameday(self):
        response=self.client.get(path='/api/reservations-slot')
        self.assertEqual(response.status_code,200)

        expected_data_sameday = [{'Reservation_date': self.today, 'Reservation_slot': 10}]
        self.assertEqual(json.loads(response.content), expected_data_sameday)
        
class ReservationCheckViewTestOtherDay(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='John', password='testpassword')
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        self.booking = Booking.objects.create(Phone="111-111-1111",First_name="John",Reservation_date=tomorrow,Reservation_slot=10,No_of_guests=2)
        self.booking.save()
    
    def test_getslototherday(self):
        response=self.client.get(path='/api/reservations-slot')
        self.assertEqual(response.status_code,200)
        expected_data_otherslot = []
        self.assertEqual(json.loads(response.content), expected_data_otherslot)
