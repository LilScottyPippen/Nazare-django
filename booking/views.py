from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.forms import formset_factory

from .forms.booking_form import *


class BookingView(TemplateView):
    template_name = 'booking/booking.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["booking_form"] = BookingForm()
        return context

    def post(self, request):
        booking_form = BookingForm(request.POST)

        GuestFormSet = formset_factory(GuestsForm)
        formset = GuestFormSet(request.POST)

        if booking_form.is_valid() and formset.is_valid():
            booking_instance = booking_form.save()

            for guest_form in formset:
                guest_form.save(commit=False)
                guest_instance = Guest.objects.create(**guest_form.cleaned_data)
                guest_instance.booking_id = booking_instance
                guest_instance.save()
            return HttpResponse(request, status=200)
        else:
            return render(request, 'booking/booking.html', {'forms': formset})


class GuestView(View):
    def get(self, request):
        form_count = int(request.GET.get('form-count'))
        if form_count is None:
            form_count = 1
        GuestFormSet = formset_factory(GuestsForm, extra=form_count)
        formset = GuestFormSet()

        return render(request, 'booking/guest_form.html', {'forms': formset})