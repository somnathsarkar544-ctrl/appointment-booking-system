from django.urls import path
from .views import AvailableSlotsView, BookAppointmentView, MyAppointmentsView, CancelAppointmentView


urlpatterns = [
    path('slots/', AvailableSlotsView.as_view(), name='available_slots'),
    path('book/', BookAppointmentView.as_view(), name='book_appointment'),
    path('my/', MyAppointmentsView.as_view()),
    path('cancel/', CancelAppointmentView.as_view()),
]