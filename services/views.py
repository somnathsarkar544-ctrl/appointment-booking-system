from services.models import ServiceProvider
from bookings.models import TimeSlot
from datetime import datetime, timedelta, time

def generate_slots(days=5):
    start_time = time(9, 0)
    end_time = time(17, 0)
    slot_duration = 30  # in minutes

    today = datetime.now().date()

    providers = ServiceProvider.objects.all()   # get all providers

    for provider in providers:   # loop each provider
        for day in range(days):

            slot_date = today + timedelta(days=day)

            current_time = datetime.combine(slot_date, start_time)
            end_datetime = datetime.combine(slot_date, end_time)

            while current_time < end_datetime:

                start = current_time.time()
                end = (current_time + timedelta(minutes=slot_duration)).time()

                TimeSlot.objects.get_or_create(
                    provider=provider,
                    date=slot_date,
                    start_time=start,
                    end_time=end
                )

                current_time += timedelta(minutes=slot_duration)
