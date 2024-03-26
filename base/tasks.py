from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from .models import Reservation


@shared_task
def delete_pending_rows():
    threshold = timezone.now() - timedelta(minutes=20)
    # Delete "PEND" rows older than 20 minutes
    Reservation.objects.filter(time_created__lte=threshold, status="PEND").delete()
