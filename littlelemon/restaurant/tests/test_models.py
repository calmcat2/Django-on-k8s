from django.test import TestCase
from restaurant.models import Menu,Booking
from datetime import date

class MenuTest(TestCase):
    def setUp(self):
        Menu.objects.create(MenuID=5,Title="Banana",Price=1,Inventory=1000).save()
        Menu.objects.create(MenuID=4,Title="Drunken Noodles",Price=10,Inventory=1).save()
        
    def test_menu(self):
        item1=Menu.objects.get(title="Banana")
        item2=Menu.objects.get(title="Drunken Noodles")
        self.assertEqual(str(item1),"Banana: 1")
        self.assertEqual(str(item2),"Drunken Noodles: 10")
        
class BookingTest(TestCase):       
    def setUp(self):
        Booking.objects.create(
            First_name="Max",
            Reservation_date=date(2024, 12, 24),  # Use `date` for DateField
            Reservation_slot=12,
            No_of_guests=3,
            Phone="432-432-3423"
        ).save()

    def test_booking(self):
        # Create a booking instance
        booking = Booking.objects.get(First_name="Max")
        # Assert that the booking was created successfully
        self.assertEqual(booking.First_name, "Max")
        self.assertEqual(booking.Reservation_date, date(2024, 12, 24))
        self.assertEqual(booking.Reservation_slot, 12)
        self.assertEqual(booking.No_of_guests, 3)
        self.assertEqual(booking.Phone, "432-432-3423")