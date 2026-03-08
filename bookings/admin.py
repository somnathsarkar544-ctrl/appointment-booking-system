from django.contrib import admin
from .models import TimeSlot,Appointment

# Register your models here.
admin.site.register(TimeSlot)
admin.site.register(Appointment)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('provider', 'date', 'start_time', 'end_time', 'is_booked')
    list_filter = ('provider', 'date')
    ordering = ('date', 'start_time')

