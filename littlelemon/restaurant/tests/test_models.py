from django.test import TestCase
from restaurant.models import Menu,Booking
from datetime import date
from dotenv import load_dotenv

class MenuTest(TestCase):
    def setUp(self):
        Menu.objects.create(MenuID=5,Title="Banana",Price=1,Inventory=1000).save()
        Menu.objects.create(MenuID=4,Title="Drunken Noodles",Price=10,Inventory=1).save()
        load_dotenv('.env')
    def test_menu(self):
        item=Menu.objects.query(title="Banana")
        self.assertEqual(str(item),"Banana: 1")
    def test_booking(self):
        # Create a booking instance
        booking = Booking.objects.create(
            First_name="Max",
            Reservation_date=date(2024, 12, 24),  # Use `date` for DateField
            Reservation_slot=12,
            No_of_guests=3,
            Phone="432-432-3423"
        )
        # Assert that the booking was created successfully
        self.assertEqual(booking.First_name, "Max")
        self.assertEqual(booking.Reservation_date, date(2024, 12, 24))
        self.assertEqual(booking.Reservation_slot, 12)
        self.assertEqual(booking.No_of_guests, 3)
        self.assertEqual(booking.Phone, "432-432-3423")