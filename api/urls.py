from .views import *
from django.urls import path


app_name = 'api'

urlpatterns = [
    path('get-booking-list', BookingListAPIView.as_view(), name='get_booking_list'),
    path('get-guest-max', GuestMaxAPIView.as_view(), name='get_guest_max'),
    path('get-guest-max/<int:apartment_id>', GuestMaxApartmentAPIView.as_view(), name='get_guest_max_apartment'),
    path('get-check-in-time', CheckInTimeAPIView.as_view(), name='get_check_in_time'),
    path('get-check-out-time', CheckOutTimeAPIView.as_view(), name='get_check_out_time'),
    path('send_confirmation_code/<str:mail>', SendConfirmationCodeAPIView.as_view(), name='send_confirmation_code'),
    path('confirm_email/<str:confirmation_code>', ConfirmEmailAPIView.as_view(), name='confirm_email'),
    path('callback/', CallbackAPIView.as_view(), name="callback"),
    path('subscribe/', SubscriberAPIView.as_view(), name="subscribe"),
]