from django.urls import path
from .views import *

urlpatterns = [
    path('get-booking-list', BookingListAPIView.as_view(), name='get_booking_list'),
    path('get-guest-max', GuestMaxAPIView.as_view(), name='get_guest_max'),
    path('get-guest-max/<int:apartment_id>', GuestMaxApartmentAPIView.as_view(), name='get_guest_max_apartment'),
    path('get-check-in-time', CheckInTimeAPIView.as_view(), name='get_check_in_time'),
    path('get-check-out-time', CheckOutTimeAPIView.as_view(), name='get_check_out_time')
]