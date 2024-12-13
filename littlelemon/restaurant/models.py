from django.db import models
import datetime


class Booking(models.Model):
    First_name = models.CharField(max_length=200)
    Reservation_date = models.DateField()
    Reservation_slot = models.SmallIntegerField(default=10)
    BookingDate=models.DateField(default=datetime.date.today().strftime('%Y-%m-%d'))
    No_of_guests=models.IntegerField(blank=False)
    Phone= models.CharField(max_length=15, default='')
    class Meta:
        unique_together = ['Reservation_date', 'Reservation_slot']

    def __str__(self): 
        return f'{self.First_name}:{str(self.BookingDate)}'

class Menu(models.Model):
    MenuID=models.IntegerField(unique=True)
    Title=models.CharField(max_length=255,unique=True)
    Price=models.DecimalField(max_digits=6,decimal_places=2)
    Inventory=models.IntegerField()
    Description=models.TextField(max_length=1000, default='') 
    def __str__(self):
        return f'{self.Title}: {str(self.Price)}'


    