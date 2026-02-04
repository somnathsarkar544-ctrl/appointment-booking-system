from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import TimeSlot, Appointment
from .serializers import TimeSlotSerializer, AppointmentSerializer
from django.db import transaction, IntegrityError

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.core.mail import send_mail
from django.conf import settings

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags

# Create your views here.

class AvailableSlotsView(APIView):
    def get(self, request):
        slots = TimeSlot.objects.filter(is_booked=False)
        serializer = TimeSlotSerializer(slots, many=True)
        return Response(serializer.data)
    
class BookAppointmentView(APIView):

    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
    operation_description="Book an appointment slot",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["slot_id"],
        properties={
            "slot_id": openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description="ID of the slot to book"
            )
        }
    ),
    responses={
        200: "Booked successfully",
        400: "Slot already booked"
    }
)


    @transaction.atomic
    def post(self, request):

        slot_id = request.data.get('slot_id')

        if not slot_id:
            return Response(
                {"error": "slot_id is required"},
                status=400
            )

        try:
            slot = TimeSlot.objects.select_for_update().get(
                id=slot_id,
                is_booked=False
            )
        except TimeSlot.DoesNotExist:
            return Response(
                {"error": "Slot not available"},
                status=400
            )

        try:
            
            appointment = Appointment.objects.create(
                user=request.user,
                slot=slot,
                status='confirmed'
            )
            

            slot.is_booked = True
            slot.save()
            
            
           #Send HTML email confirmation
            html_content = render_to_string('emails/booking_conf.html', {'customer_name': request.user.get_full_name() or request.user.username, 'service_name': 'Appointment Service', 'booking_date': slot.date, 'booking_time': slot.start_time})
            text_content = strip_tags(html_content)
            email = EmailMultiAlternatives(
                subject='Appointment Confirmation',
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[request.user.email],
            )
            email.attach_alternative(html_content, "text/html")
            email.send()
         
             
            serializer = AppointmentSerializer(appointment)

            return Response(serializer.data, status=201)

        except IntegrityError:
            return Response(
                {"error": "This slot is already booked"},
                status=400
            )

class MyAppointmentsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        appointments = Appointment.objects.filter(user=request.user).order_by('-created_at')
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)

class CancelAppointmentView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
    operation_description="Cancel an appointment",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["appointment_id"],
        properties={
            "appointment_id": openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description="ID of the appointment to cancel"
            )
        }
    ),
    responses={
        200: "Cancelled successfully",
        400: "Appointment not found or cannot be cancelled"
    }
)
    


    @transaction.atomic
    def post(self, request):
        appointment_id = request.data.get('appointment_id')

        if not appointment_id:
            return Response(
                {"error": "appointment_id is required"},
                status=400
            )

        try:
            appointment = Appointment.objects.select_for_update().get(
                id=appointment_id,
                user=request.user,
                status__in=['confirmed', 'pending']
            )
        except Appointment.DoesNotExist:
            return Response(
                {"error": "Appointment not found or cannot be cancelled"},
                status=400
            )
        #free up the slot
        slot = appointment.slot
        slot.is_booked = False
        slot.save()

        booking_date = appointment.slot.date
        booking_time = appointment.slot.start_time
        service_name = "Appointment Service"
        customer_name = request.user.get_full_name() or request.user.username

        appointment.delete()
        # Send  html cancellation email
        html_content = render_to_string('emails/cancellation_conf.html', {'customer_name': customer_name, 'service_name': service_name, 'booking_date': booking_date, 'booking_time': booking_time})
        text_content = strip_tags(html_content)
        email = EmailMultiAlternatives(
            subject='Appointment Cancellation',
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[request.user.email],
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
       


        return Response(
            {"message": "Appointment cancelled successfully"},
            status=200
        )
    

@swagger_auto_schema(
    operation_description="Book an appointment for a given time slot.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'slot_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the time slot to book'),
        },
    ),
    responses={
        201: openapi.Response('Appointment booked successfully', AppointmentSerializer),
        400: 'Bad Request',
    }
)
def post(self,request):
    pass  # The actual implementation is in the BookAppointmentView class above