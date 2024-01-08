import threading
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.forms import formset_factory, BaseFormSet
from .models.booking import *
from .forms.booking_form import *
from utils.send_mail import *


class BaseArticleFormSet(BaseFormSet):
    def clean(self):
        for form in self.forms:
            guest_name = form.cleaned_data.get('guest_name')
            guest_second_name = form.cleaned_data.get('guest_second_name')
            guest_father_name = form.cleaned_data.get('guest_father_name')

            if not is_valid_full_name(guest_name, guest_second_name, guest_father_name):
                raise forms.ValidationError("Full name is invalid")


class BookingView(TemplateView):
    template_name = 'booking/booking.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["booking_form"] = BookingForm()
        return context

    def post(self, request):
        booking_form = BookingForm(request.POST)

        GuestFormSet = formset_factory(GuestsForm, formset=BaseArticleFormSet)
        formset = GuestFormSet(request.POST)

        if booking_form.is_valid() and formset.is_valid():
            booking_instance = booking_form.save()

            self.send_mailing(booking_instance)

            for guest_form in formset:
                guest_instance = Guest.objects.create(**guest_form.cleaned_data)
                guest_instance.booking_id = booking_instance
                guest_instance.save()
            return HttpResponse("Success", 200)
        else:
            return HttpResponseBadRequest("Form is invalid", 400)

    def send_mailing(self, booking_instance):
        if booking_instance.payment_method == PAYMENT_METHOD_CHOICES[1][0]:
            threading.Thread(target=send_mail_for_admin,
                             args=('mailing/admin_callback.html', {
                                 'name': booking_instance.client_name,
                                 'phone': booking_instance.client_phone,
                                 'created': booking_instance.created_at
                             })).start()
        if booking_instance.payment_method == PAYMENT_METHOD_CHOICES[0][0]:
            threading.Thread(target=send_mail_for_client,
                             args=(booking_instance.client_mail, 'mailing/client_receipt.html', {
                                 'name': booking_instance.client_name,
                                 'check_in': booking_instance.check_in_date,
                                 'check_out': booking_instance.check_out_date,
                                 'is_paid': booking_instance.is_paid,
                                 'total_sum': booking_instance.total_sum
                             })).start()


class GuestView(View):
    def get(self, request):
        form_count = int(request.GET.get('form-count'))
        if form_count is None:
            form_count = 1

        GuestFormSet = formset_factory(GuestsForm, extra=form_count)
        formset = GuestFormSet()

        return render(request, 'booking/guest_form.html', {'forms': formset})