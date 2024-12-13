from django.urls import path,include
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('',views.home,name="home"),
    path('about/', views.about, name="about"),
    path('book/', views.book, name="book"),
    path('bookings/',views.bookings,name='bookings'),
    path('menu/',views.menu, name='menu'),
   # path('reservations', views.reservations, name='reservations'), 
    path('menu-items/<int:pk>', views.menu_item,name='menu_item'),
    path('api/menu/', views.MenuItemsView.as_view()),
    path('api/menu-items/<int:pk>', views.SingleMenuItemView.as_view()),
    path('api/reservations/',views.BookingView.as_view()), 
    path('api/reservations/<int:pk>',views.SingleBookingView.as_view()), 
    path('api-token-auth/', obtain_auth_token),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
 
]
